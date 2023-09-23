import string
from telnetlib import STATUS
from bs4 import BeautifulSoup
import requests
import soupsieve

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
        info =info_pagination.find_all('li')
        
        for item in info:
                if(item.find('a')):
                        ref = item.find('a')['href']
                        print(base_url + ref)
                        #print(['href'])
        print(info)

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
