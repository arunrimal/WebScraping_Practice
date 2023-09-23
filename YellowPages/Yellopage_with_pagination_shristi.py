#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import html
import pandas as pd
import datetime
import math
import unicodecsv as csv
import argparse
import time
from django.shortcuts import render
import pyodbc, yaml, os
from azure.storage.blob import BlobClient
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
file_path = os.path.join(BASE_DIR, 'config/config.yaml')

datetime_start = datetime.datetime.now()
print(f'start time is  {datetime_start}')
    
    
def parse_listing(keyword, place):

    url = "https://www.yellowpages.com/search?search_terms={0}&geo_location_terms={1}".format(keyword, place)

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
    
    # Adding retries
    for retry in range(1):
        #try:
        response = requests.get(url, verify=False, headers=headers)
        if response.status_code == 200:
            parser = html.fromstring(response.text)
            base_url = "https://www.yellowpages.com"
            parser.make_links_absolute(base_url)
            
            """ Code to get the pagination. 
                Logic: Total number of block from class pagination divided by 30
            """
                
            XPATH_pagination = "//div[@class='pagination']//span//text()"
            listings_pagination = parser.xpath(XPATH_pagination)
            listings_pagination = listings_pagination[0]
            num_str_pagination = listings_pagination.split(" ")
            num_str_pagination = num_str_pagination[3]
            num_str_pagination = math.ceil(int(num_str_pagination)/30)
            #print(num_str_pagination)
            
            try:
                for url_pagination in range(1, (num_str_pagination+1)):
                #for url_pagination in range(1, (num_str_pagination+1)):
                    url_with_pagination = "https://www.yellowpages.com/search?search_terms="+str(keyword)+"&geo_location_terms="+str(place)+"&page="+str(url_pagination)
                    response_pagination = requests.get(url_with_pagination, verify=False, headers=headers)
                    
                    print("retrieving ", url_with_pagination)
                    print("parsing page")
                    
                    if response_pagination.status_code == 200:
                        parser_pagination = html.fromstring(response_pagination.text)
                        # making links absolute
                        base_url = "https://www.yellowpages.com"
                        parser_pagination.make_links_absolute(base_url)
                    
                        XPATH_LISTINGS = "//div[@class='search-results organic']//div[@class='v-card']"
                        listings = parser_pagination.xpath(XPATH_LISTINGS)
                        
                       
                        for results in listings:
                            XPATH_BUSINESS_NAME = ".//a[@class='business-name']//text()"
                            XPATH_BUSSINESS_PAGE = ".//a[@class='business-name']//@href"
                            XPATH_TELEPHONE = ".//div[@class='phones phone primary']//text()"
                            XPATH_ADDRESS = ".//div[@class='info']//div//p[@itemprop='address']"
                            XPATH_STREET = ".//div[@class='street-address']//text()"
                            XPATH_LOCALITY = ".//div[@class='locality']//text()"
                            XPATH_REGION = ".//div[@class='info']//div//p[@itemprop='address']//span[@itemprop='addressRegion']//text()"
                            XPATH_ZIP_CODE = ".//div[@class='info']//div//p[@itemprop='address']//span[@itemprop='postalCode']//text()"
                            XPATH_RANK = ".//div[@class='info']//h2[@class='n']/text()"
                            XPATH_CATEGORIES = ".//div[@class='info']//div[contains(@class,'info-section')]//div[@class='categories']//text()"
                            XPATH_WEBSITE = ".//div[@class='info']//div[contains(@class,'info-section')]//div[@class='links']//a[contains(@class,'website')]/@href"
                            XPATH_RATING = ".//div[@class='info']//div[contains(@class,'info-section')]//div[contains(@class,'result-rating')]//span//text()"
                            
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
                            
                            business_name = ''.join(raw_business_name).strip() if raw_business_name else None
                            telephone = ''.join(raw_business_telephone).strip() if raw_business_telephone else None
                            business_page = ''.join(raw_business_page).strip() if raw_business_page else None
                            rank = ''.join(raw_rank).replace('.\xa0', '') if raw_rank else None
                            category = ','.join(raw_categories).strip() if raw_categories else None
                            website = ''.join(raw_website).strip() if raw_website else None
                            rating = ''.join(raw_rating).replace("(", "").replace(")", "").strip() if raw_rating else None
                            address = ''.join(raw_address).strip() if raw_website else None
                            street = ''.join(raw_street).strip() if raw_street else None
                            
                            ### Extracting data for locality ###
                            locality_raw = ''.join(raw_locality).replace(',\xa0', '').strip() if raw_locality else None
                            locality_split = locality_raw.split(',') if raw_locality else None
                            locality = locality_split[0] if locality_split else None
                            
                            ### Extracting data for region ###
                            region_raw = locality_split[1] if locality_split else None
                            region_split = region_raw.split(' ') if raw_locality else None
                            region = region_split[1] if region_split else None
                            
                            ### Extracting data for zipcode ###
                            zipcode = region_split[2] if region_split else None
                            #print (zipcode)
                            companyName_stateabbreviation = (business_name + ',' + region) if region else None
                            
                            time.sleep(1)
                            #print(business_name,telephone, business_page, rank)
                            
                            
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
                                    'companyName_stateabbreviation': companyName_stateabbreviation , 
                                    }, ignore_index=True)
                            #print(dframeList)
                        dframeList.append(dframeList) 
                        print(dframeList)
                        
                datetime_end = datetime.datetime.now()
                print(f'end time is  {datetime_end} ')
                
                timediff = math.ceil((datetime_end - datetime_start).seconds) / 60
                
                print(F'task complited in {timediff} minutes')
                return dframeList.to_csv('Yellowpage.csv', quoting=csv.QUOTE_ALL , encoding="utf-8", index=False)
        
            except:
                "Error in the pagination block"
    
        elif response.status_code == 404:
            print("Could not find a location matching", place)
            break
        else:
            print("Failed to process page")
            return []



    



if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument('keyword', help='Search Keyword')
    argparser.add_argument('place', help='Place Name')
    args = argparser.parse_args()
    keyword = args.keyword
    place = args.place

    scraped_data = parse_listing(keyword, place) 
    
    

