from __future__ import absolute_import, unicode_literals
import requests as req
#from .models import AzureLogicAppEmail, ScrapingLog
import json
import requests
from lxml import html
import pandas as pd
import datetime
import math
import pyodbc
import argparse

def parse_listing(keyword, place):

    url = "https://www.yellowpages.com/search?search_terms={0}&geo_location_terms={1}".format(keyword, place)

    print("retrieving ", url)

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Host': 'www.yellowpages.com',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
               }
    
    dframeList = []
    
    dframeList = pd.DataFrame(columns=['page_rank', 'business_name', 'telephone', 'business_page', 'category', 'website', 'rating', 'company_address', 'street', 'locality', 'region', 'zipcode_yellowpage', 'listing_url', 'companyName_stateabbreviation'])
    
    for retry in range(2):
        try:
            response = requests.get(url, verify=False, headers=headers)
            print("parsing page")
            if response.status_code == 200:
                parser = html.fromstring(response.text)
                # making links absolute
                base_url = "https://www.yellowpages.com"
                parser.make_links_absolute(base_url)

                XPATH_LISTINGS = "//div[@class='search-results organic']//div[@class='v-card']"
                listings = parser.xpath(XPATH_LISTINGS)
                print(listings)  
                print(len(listings))

                for results in listings:
                    XPATH_BUSINESS_NAME = ".//a[@class='business-name']//text()"
                    XPATH_BUSSINESS_PAGE = ".//a[@class='business-name']//@href"
                    XPATH_TELEPHONE = ".//div[@class='phones phone primary']//text()"
                    XPATH_ADDRESS = ".//div[@class='info']//div//p[@itemprop='adr']"      ###########
                    XPATH_STREET = ".//div[@class='street-address']//text()"
                    XPATH_LOCALITY = ".//div[@class='locality']//text()"
                    XPATH_REGION = ".//div[@class='info']//div//p[@itemprop='address']//span[@itemprop='addressRegion']//text()"
                    XPATH_ZIP_CODE = ".//div[@class='info']//div//p[@itemprop='address']//span[@itemprop='postalCode']//text()"
                    XPATH_RANK = ".//div[@class='info']//h2[@class='n']/text()"
                    XPATH_CATEGORIES = ".//div[@class='info']//div[contains(@class,'info-section')]//div[@class='categories']//text()"
                    XPATH_WEBSITE = ".//div[@class='info']//div[contains(@class,'info-section')]//div[@class='links']//a[contains(@class,'website')]/@href"
                    XPATH_RATING = ".//div[@class='info']//div[contains(@class,'info-section')]//div[contains(@class,'result-rating')]//span//text()"

                    #print(XPATH_ADDRESS)


                    raw_business_name = results.xpath(XPATH_BUSINESS_NAME)
                    raw_business_telephone = results.xpath(XPATH_TELEPHONE)
                    raw_business_page = results.xpath(XPATH_BUSSINESS_PAGE)
                    raw_categories = results.xpath(XPATH_CATEGORIES)
                    raw_website = results.xpath(XPATH_WEBSITE)
                    raw_rating = results.xpath(XPATH_RATING)
                    raw_address = results.xpath(XPATH_ADDRESS)
                    raw_street = results.xpath(XPATH_STREET)
                    raw_locality = results.xpath(XPATH_LOCALITY)
                    raw_region = results.xpath(XPATH_REGION)
                    raw_zip_code = results.xpath(XPATH_ZIP_CODE)
                    raw_rank = results.xpath(XPATH_RANK)

                    #print(raw_business_name)
                    #print(raw_business_telephone)
                    #print(raw_business_page)
                    #print(raw_categories)
                    #print(raw_website)
                    #print(raw_rating)
                    #print(raw_address)
                    #print(raw_street)
                    #print(raw_locality)
                    #print(raw_rank)

                    business_name = ''.join(raw_business_name).strip() if raw_business_name else None
                    telephone = ''.join(raw_business_telephone).strip() if raw_business_telephone else None
                    business_page = ''.join(raw_business_page).strip() if raw_business_page else None
                    rank = ''.join(raw_rank).replace('.\xa0', '') if raw_rank else None
                    category = ','.join(raw_categories).strip() if raw_categories else None
                    website = ''.join(raw_website).strip() if raw_website else None
                    rating = ''.join(raw_rating).replace("(", "").replace(")", "").strip() if raw_rating else None
                    address = ''.join(raw_address).strip() if raw_website else None
                    street = ''.join(raw_street).strip() if raw_street else None
                    locality = ''.join(raw_locality).replace(',\xa0', '').strip() if raw_locality else None
                    locality, locality_parts = locality.split(',')
                    _, region, zipcode = locality_parts.split(' ')

                    #print(business_name)
                    #print(telephone)
                    #print(business_page)
                    #print(category)
                    #print(website)
                    #print(rating)
                    #print(address)
                    #print(street)
                    #print(locality)
                    #print(rank)
                    
                    dframeList = dframeList.append({
                            'business_name': business_name,
                            'telephone': telephone,
                            'business_page': business_page,
                            'page_rank': rank,
                            'category': category,
                            'website': website,
                            'rating': rating,
                            'company_address': address,
                            'street': street,
                            'locality': locality,
                            'region': region,
                            'zipcode_yellowpage': zipcode,
                            'listing_url': response.url, 
                            'companyName_stateabbreviation': business_name + ',' + region , 
                            }, ignore_index=True)

                dframeList.append(dframeList)    
                
                #dataframe_merged = pd.merge(dframeList.assign(companyName_stateabbreviation = dframeList['companyName_stateabbreviation'].str.upper()), 
                #                            df_query.assign(companyName_stateabbreviation = df_query['companyName_stateabbreviation'].str.upper()), 
                #                            how="inner", on=["companyName_stateabbreviation"])
                
                #dataframe_merged.fillna("",inplace=True)
                #dataframe_merged['data_source'] = "Yellow Page"
                #dataframe_merged['inserted_datetime'] = sysdate
                
                print(dframeList)
        except:
            print("Failed to process page")
            return []

#parse_listing(keyword, place)
parse_listing('Amazon', 'New York, NY')