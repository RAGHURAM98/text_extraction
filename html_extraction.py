# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 12:59:33 2017

@author: RAM
"""

import pandas as pd
import urllib2
from bs4 import BeautifulSoup
import re
import numpy as np

#xl = pd.ExcelFile("ssss.xlsx")
xl = pd.ExcelFile("Input.xlsx")
c=0
df = xl.parse("CompleteListFilingsAllInfo")
#df = xl.parse("Sheet1")
#df = df.iloc[:,:-1].values

list1=[]
list2=[]
list3=[]
list4=[]
for row in df["URL"]:
    
    page = urllib2.urlopen(row)
#page=open("forcast.txt","r").read()
    soup = BeautifulSoup(page, "html.parser") 
    spans = soup.find_all('font')

    plist = []

    for span in spans:
        plist.append(span.string)

    all_text = "Credit Default Swap"
    #l=plist.index(all_text)
    if all_text in plist:
        l=plist.index(all_text)
        list1.append(plist[l+1])
        list2.append(plist[l+2])
        list3.append(plist[l+3])
        list4.append(plist[l+4])

    else:
        list1.append("N.A")
        list2.append("N.A")
        list3.append("N.A")
        list4.append("N.A")
        
    c=c+1
    print (c)
    

df['CDS TEXT'] = pd.Series(list1).values
df['Expiration Period'] = pd.Series(list2).values
df['Notational Amount'] = pd.Series(list3).values
df['Unrealiased appreciation'] = pd.Series(list4).values


writer = pd.ExcelWriter('output.xlsx')
df.to_excel(writer,'Sheet1')
#df2.to_excel(writer,'Sheet2')
writer.save()