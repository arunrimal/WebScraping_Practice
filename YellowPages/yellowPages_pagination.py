from ast import Break
from telnetlib import STATUS
from bs4 import BeautifulSoup
import requests
import soupsieve

def pagination(page):
        p=0
        page_list=[0]
        info = ''
        for i in page_list:
            url1= "https://www.yellowpages.com/search?search_terms={}&geo_location_terms={}&page={}".format('Amazon','New York, NY',page_list[i])
            print(url1)

            soup=requests.get(url1)
            data = BeautifulSoup(soup.text,'html.parser')
            info = str(data.find('div', class_='search-term').h1.text)
            print(info)
            if(info !='No results found for Amazon in New'):
                print(info)
                          
                print('Total pages: ',p)
                p +=1
                print('this is page no: ', page)
                print(page_list)
                page = page+1
                page_list.append(page)
                pass
            else:
                #print("pagination continue..")
                page_list.clear
                print('Pagination ends here: ',page_list)
                
                break
                #pass    
        
        return p
        
        

pagination(0)
#data = BeautifulSoup(soup.text,'html.parser')
#info = data.find('div', class_='pagination').text