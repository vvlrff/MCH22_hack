#!/usr/bin/env python
# coding: utf-8

# In[1]:


import glob
import json

listJSONFiles = glob.glob('./*.json')


# In[2]:


listJSONFiles


# In[3]:


listDict = []
for i in range(len(listJSONFiles)):
    listDictVar = []
    with open(listJSONFiles[i], 'r') as file:
        listDictVar.append(json.load(file))
    listDict.append(listDictVar[0])
print(listDict)


# In[4]:


with open('ZippedJSON.json', 'w') as file:
    file.write(json.dumps(listDict,indent=1))


# In[ ]:




