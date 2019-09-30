import  re
import urllib.request
import urllib.parse
import urllib.error
import datetime
import  json
from bs4 import BeautifulSoup
url = "http://localhost/"
# url = "http://103.91.144.230/ftpdata/Movies/%203D_MOVIE/";
with open('mimeType.json') as f:
    mime = json.load(f)

dataSet = []

def process(url):

    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request, timeout=2).read()
        print(response)
    except:
        print("404 => ", url)
        return

    get = BeautifulSoup(response, "html.parser")
    response = get.find("pre")
    # print(get.find("a").attrs["href"])
    # exit();
    response = re.sub(r"\n$","", str(response).replace("<pre>", "").replace("</pre>", ""))

    rawData = (response.splitlines())
    for data in rawData:
        if data.__contains__("../") or data.__contains__("./"):
            continue
        ancher = BeautifulSoup(data, "html.parser")
        ancher = ancher.find("a")
        data = data.replace(str(ancher), "")
        data = re.sub(r"^[\s\t\r]+","", data)
        data = re.sub(r"[\s]+[\s]+",",",data)
        info = re.split(",", data)
        dir = {}
        try:
            f = ancher.attrs["href"]
            ex = f.split('.')[-1];
            if mime.get(ex) == None:
                ex = ex.lower()
            dir["path"] = url+f
            dir["name"] = ancher.text
            dir["type"] = {"extension" : ex, "description" : mime.get(ex)}
        except:
            dir["path"] = None
        try:

            date = datetime.datetime.strptime(info[0], '%d-%b-%Y %H:%M')
            dir["year"] = date.year
            dir["month"] = date.month
            dir["date"] = info[0]
        except:
            dir["year"] = None
            dir["month"] = None
            dir["date"] = None
        try:
            if info[1] == '-':
                info[2] = None
            dir["size"] = info[1]
        except:
            dir["size"] = None

        if dir.get("size") != None :

            print("file => ",dir.get("path"))
            dataSet.append(dir)
            file = open("dataSet.json", "w+")
            file.write(json.dumps(dataSet))
            file.close()
        else:

            print("dir => ",dir.get("path"))
            process(dir.get("path"))

process(url)
file = open("dataSet.json", "w+")
file.write(json.dumps(dataSet))
file.close()
print(dataSet)
