from asyncio import base_events
from telnetlib import STATUS
from bs4 import BeautifulSoup
from flask_sqlalchemy import Pagination
import requests
import math
import pandas as pd
from sqlalchemy import false




def get_url(k, pl):
    url_list=[]
    base_link = "https://www.yellowpages.com"

    dframeList = []
    
    dframeList = pd.DataFrame(columns=['page_rank', 'business_name', 'telephone', 'business_page', 'category', 'website', 'rating', 'street', 'locality']) #, 'region', 'zipcode_yellowpage', 'listing_url', 'companyName_stateabbreviation'])
    

    def pagination(k,pl,p):
        
        url1= "https://www.yellowpages.com/search?search_terms={}&geo_location_terms={}&page={}".format(k,pl,p)

        p=0     
        
        #base_url = "https://www.yellowpages.com"
        #url1= "https://www.yellowpages.com/search?search_terms={}&geo_location_terms={}&page={}".format('Amazon','New York, NY',p)
        print(url1)
        soup=requests.get(url1)
        data = BeautifulSoup(soup.text,'html.parser')
        info_pagination = data.find('div', class_='pagination')
        #info =info_pagination.find('span').text
        info2= info_pagination.find('span').text.split()

        #print(info)
        #print(type(info))
        print(info2)
        #print(info3)
        #print(info[10:13])
        #print(round(int(info[-3:])/int(info[10:13])))
        p= math.ceil(int(info2[3])/int(info2[1][-2:]))
        print(p)

        return p
    
    


    for page in range(1, pagination(k, pl, 1)+1):
        url= "https://www.yellowpages.com/search?search_terms={}&geo_location_terms={}&page={}".format(k, pl, page)
        print(url)
        url_list.append(url)

        #resp=requests.get(url=url)
    #print(url_list)
    for url in url_list:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        #print(soup)
        products = soup.find('div',class_ ='search-results organic').find_all('div',class_='v-card')
        print('this is total product',len(products))
        for item in products:
            name_raw = item.find('a',class_='business-name')
            name = name_raw.text if name_raw else None
            
            business_page_raw = item.find('a',class_='business-name')
            business_page = base_link + business_page_raw['href'] if business_page_raw else None
            
            telephone_raw = item.find('div',class_='phones phone primary')
            telephone = telephone_raw.text if telephone_raw else None

            categories_raw = item.find('div', class_='categories')
            categories = categories_raw.get_text(", ") if categories_raw else None

            rank_raw =item.find('h2', class_='n')
            rank = rank_raw.text[:2] if rank_raw else None

            website_raw = item.find('a',class_='track-visit-website')
            website = website_raw['href'] if website_raw else None

            rating_raw = item.find('div', class_ = 'ratings')
            rating = rating_raw.text[:2].replace('(','').replace('BB','') if rating_raw else None

            street_raw= item.find('div', class_='street-address')
            street = street_raw.text if street_raw else None

            locality_raw= item.find('div', class_='locality')
            locality = locality_raw.text if locality_raw else None

            #name = item.find('a',class_='business-name').text
            #name = item.find('a',class_='business-name').text
            #name = item.find('a',class_='business-name').text
            item={
                'page_rank':rank , 
                'business_name': name, 
                'telephone': telephone, 
                'business_page':business_page , 
                'category':categories , 
                'website': website,
                'rating': rating, 
                #'company_address':, 
                'street': street, 
                'locality':locality
            }
            dframeList=dframeList.append(item, ignore_index=false)
            #print(name,'  ',business_page,'  ',telephone,'  ',categories,)    
            #print('   ',rank, '  ',website, '  ', rating,'  ',street,'  ',locality)
            #print(categories)
    print(dframeList)
#print('Total Products: ', len(products))

        

    

get_url('Vietnamese Restaurants', "New York, NY")
#def pagination(4)