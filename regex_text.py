# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 09:18:49 2017

@author: RAM
"""

import pandas as pd
import urllib2
from bs4 import BeautifulSoup
import re
import numpy as np

#read files
def read_excel():
    xl = pd.ExcelFile("output phase 1.xlsx")
    df = xl.parse("Sheet1")
    df = df.iloc[:, :-3]
    return df

#cds text extraction
def re_extraction(df):

    list1=[]
    list2=[]
    list3=[]
    list4=[]
    df=df.dropna(axis=0, how='any')
    
    df = df[df["CDS TEXT"] != "N.A"]

    for row in df["CDS TEXT"]:
    #cds transaction
        if row.find("Receive quarterly")>=0 or row.find("receive quarterly")>=0:
            list1.append("Sell")
        elif row.find("pay quarterly")>=0 or row.find("Pay quarterly")>=0 :
            list1.append("Buy")
        else:
            list1.append(" ")

    #underlying    
        m = re.search('upon default of (.+?),', row)
        if m:
            list2.append(m.group(1))  
        else:
                list2.append("")

    #exact underlying pattern
        m1=re.search("amount of (.+?)(,)",row)
        m2=re.search("amount of (.+?) and",row)
        m3=re.search("amount of (.+?)($)",row)
        m10=re.search("amount of (.+?)(%)",row)
        if m1:
            list3.append(m1.group(1))
        elif m2:
            list3.append(m2.group(1))
        elif m3:
            list3.append(m3.group(1))
        elif m10:
            list3.append(m10.group(1))
        else:
            list3.append("")
        
        m4=re.search("pay (.+?),",row)
        if m4:
            list4.append(m4.group(1))
        else:
            list4.append("")


    df['CDS underlying'] = pd.Series(list2).values
    df['counter party'] = pd.Series(list4).values
    df['CDS Exact underlying'] = pd.Series(list3).values
    df['CDS Transaction'] = pd.Series(list1).values
    return df

# write data frame to excel
def writer_excel(df):
    writer = pd.ExcelWriter('output1.xlsx')
    df.to_excel(writer,'Sheet1')
    writer.save()
    
if __name__ == "__main__":
    df=read_excel()
    df=re_extraction(df)
    writer_excel(df)