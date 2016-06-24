# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 08:05:47 2016

@author: austin
"""

from bs4 import BeautifulSoup as bs
import urllib2
import pandas as pd

def getPlaneData(yearStart, yearEnd):
    number = yearEnd - yearStart + 1
    fs = pd.DataFrame()
    for y in range(number):        
        firstLink = 'http://www.aviation-safety.net/database/dblist.php?Year=' + str(yearStart)
        yearStart +=1
        
        #get list of all links for current year
        req = urllib2.Request(firstLink)
        req.add_unredirected_header('User-Agent', 'Custom User-Agent')
        #get HTML of link        
        html =urllib2.urlopen(req).read()
        #make the HTML a soup
        soup= bs(html)
        #pull out all links in the html file and subset the data that starts with database        
        list = []
        for link in soup.find_all('a', href=True):
           list.append(link['href'])
        content = [x for x in list if  x.startswith('/database/r')]
        #main loop through all links just extracted gets html content of each link and extract the table in each file
        for a in content: 
            link = 'http://www.aviation-safety.net' + a
            req = urllib2.Request(link)
            req.add_unredirected_header('User-Agent', 'Custom User-Agent')
            html2 =urllib2.urlopen(req).read()
            table = bs(html2)
            try:
                tab= table.find_all('table')[0]
                records = []
                for tr in tab.findAll("tr"):
                    trs = tr.findAll("td")    
                    th = tr.findAll("th")
                    record = []
                    record.append(trs[0].text)
                    try:
                        record.append(trs[1].text)
                    except:
                        continue
                        record.append(th[0].text)
                    records.append(record)
                df = pd.DataFrame(data=records)
            except:
                pass
            df.set_index(df[0],inplace=True)
            df = pd.DataFrame(df.ix[:,1])
            df = pd.DataFrame.transpose(df)
            fs=fs.append(df)
    return pd.DataFrame(fs)