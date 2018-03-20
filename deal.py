import json
import os
import re

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
print(dict2)
#print(json.dumps(str))
# Notice comma to avoid automatic newline added by Python
f.close() 

