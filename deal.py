import json
import os
import re
import test2
import urllib.parse
import urllib.request
###get
response = urllib.request.urlopen('http://192.168.31.101:8080/task/ei/get')
html = response.read()  
print(html.decode('utf-8'))
###  

###post
url = 'http://127.0.0.1:8080/test/index.jsp'  
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' 
headers = {'Content-Type': 'application/json'} 
values = {  
    'name': 'abc',  
    'password': '123'  
}  
data = urllib.parse.urlencode(values)  
# that params output from urlencode is encoded to bytes before it is sent to urlopen as data  
data = data.encode('utf-8')  
req = urllib.request.Request(url, data)  
response = urllib.request.urlopen(req)  
  
html = response.read()  
print(html.decode('utf-8'))  
###
test2.search()
f=open(r"C:\Users\Administrator\EV_download\Engineering_Village_detailed_3-19-2018_5272473.txt","r")
lines=f.readlines()
dict={}
dict2={}
dict2['taskid']='asdsafasasfsafsafa'
record=1
list=[]
for count in range(len(lines)):
    if record>2:
        break
    if re.match('<RECORD %d>'%(record+1),lines[count]):
        record=record+1
        list.append(dict)
        dict={}
    if lines[count]=='\n':
        continue
    if re.match('<RECORD %d>'%record,lines[count]):
        continue
    i=lines[count].find(':')
    j=len(lines[count])
    dict[lines[count][:i]]=lines[count][i+1:j-1]
dict2['data']=list

#jso = json.dumps(dict)
#print(dict2)
print(json.dumps(dict2))
# Notice comma to avoid automatic newline added by Python
f.close() 

