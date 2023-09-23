from decimal import ROUND_UP
import string
from telnetlib import STATUS
from bs4 import BeautifulSoup
import requests
import soupsieve
import math

def pagination(page):
        p=0
        page_list=[0]
        list_href=[]
        info = ''
        base_url = "https://www.yellowpages.com"
        url1= "https://www.yellowpages.com/search?search_terms={}&geo_location_terms={}&page={}".format('Amazon','New York, NY',p)
        print(url1)
        soup=requests.get(url1)
        data = BeautifulSoup(soup.text,'html.parser')
        info_pagination = data.find('div', class_='pagination')
        info =info_pagination.find('span').text
        info2= info_pagination.find('span').text.split()
        #info3= info_pagination.find('span').text.split()
        
        #for item in info:
                #if(item.find('a')):
                        #ref = item.find('a')['href']
                        #print(base_url + ref)
                        #print(['href'])
        #print(info)
        print(type(info))
        print(info2)
        print(info2.pop())
        print(info2)
        #print(info3)
        #print(info[10:13])
        #print(round(int(info[-3:])/int(info[10:13])))
        #print(math.ceil(int(info2[3])/int(info2[1][-2:])))

        #info_str= info[-2].find('a')['data-analytics']
        #info_str= info[-2].text
        #print(info_str)

        #for item in info:
                #try:
                #        link = item.find('a')['href']
                #except AttributeError as err:
                #        link = 'none'
                #print(link)
        
        #for atag in info:
                #if(atag.find('a')['href']):
                        #if(atag not in list_href):
                        #        list_href.append(atag)
                        #print(list_href)
                        
        return p
        

pagination(0)
