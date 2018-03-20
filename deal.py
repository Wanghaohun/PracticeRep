import json
import os
import re
f=open(r"C:\Users\Administrator\EV_download\Engineering_Village_detailed_3-19-2018_5272473.txt","r")
lines=f.readlines()
dict={}
dict2={}
dict2['taskid']='asdsafasasfsafsafa'
for count in range(len(lines)):
    if re.match('<RECORD 2>',lines[count]):
        break
    if lines[count]=='\n':
        continue
    if re.match('<RECORD 1>',lines[count]):
        continue
    i=lines[count].find(':')
    j=len(lines[count])
    dict[lines[count][:i]]=lines[count][i+1:j-1]
dict2['data']=dict

#jso = json.dumps(dict)
print(dict2)
#print(json.dumps(str))
# Notice comma to avoid automatic newline added by Python
f.close() 

