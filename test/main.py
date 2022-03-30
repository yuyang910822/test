import jsonpath
import requests

url = 'http://10.8.12.157:8080/api/maps/4949fcd8-767d-42f2-985b-d301ce410199/markers?versionId=efeeee81-8924-4bf4-b9b8-593395d9e8c1'

data = requests.get(url).json()
print(data)
for i in jsonpath.jsonpath(data,'$..aliases'):

    if i[0][0] == 'P':
        print(i[0])
