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


datetime_start = datetime.datetime.now()
print(f'start time is  {datetime_start}')
    
view_name = "company.Company_Location"
table_name = "company.Historical_log_data"
stateid = "122395D0-8860-48C2-9E57-A27C8369924E" ### Parameter to be passed
company_name = "VERISK ANALYTICS ISO,NJ" ### Parameter to be passed

sysdate = datetime.datetime.now().strftime("%Y-%m-%d")

cnxn = pyodbc.connect("Driver={SQL Server};"
                        "Server=oasis-data.database.windows.net;"
                        "Database=OasisTransaction;"
                        "uid=Shristi;pwd=Shri$ti0asis!")


#query = "select  a.detailsID,a.companyID,a.locationID,b.cityID,b.stateID,b.countryID,a.companyName_stateabbreviation,b.cityName,b.cityAbbreviation,b.stateName,b.stateAbbreviation,b.countryName,b.countryAbbreviation,b.zipCode,b.latitude,b.longitude,Updated_Flag,lastpulldate,datatype from company.Company_Location a inner join [company].Historical_log_data b on a.detailsID = b.detailsID and a.companyID = b.companyID and a.locationID = b.locationID and a.stateid = '" + stateid + "' and b.Updated_Flag = 'N' and b.lastpulldate < cast(DATEADD(year, -1, GETDATE()) as date) and a.companyName_stateabbreviation = '" + company_name +"';"
#print(query)

query =  "exec import.Yellow_page '" + company_name + "', '" + stateid + "' , 'SELECT'"
df_query = pd.read_sql_query(query, cnxn)
#print(df_query)

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
    
    for retry in range(10):
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
                    locality = ''.join(raw_locality).replace(',\xa0', '').strip() if raw_locality else None
                    locality, locality_parts = locality.split(',')
                    _, region, zipcode = locality_parts.split(' ')
                    
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
                
                dataframe_merged = pd.merge(dframeList.assign(companyName_stateabbreviation = dframeList['companyName_stateabbreviation'].str.upper()), 
                                            df_query.assign(companyName_stateabbreviation = df_query['companyName_stateabbreviation'].str.upper()), 
                                            how="inner", on=["companyName_stateabbreviation"])
                
                dataframe_merged.fillna("",inplace=True)
                dataframe_merged['data_source'] = "Yellow Page"
                dataframe_merged['inserted_datetime'] = sysdate
                
                #print(dataframe_merged)
                
                ################################################################
                # INSERTING/ UPDATING RECORDS
                ################################################################
                
                cols = ",".join([str(i) for i in dataframe_merged.columns.tolist()])
                                
                for i,row in dataframe_merged.iterrows():
                    companyName_stateabbreviation = row['companyName_stateabbreviation']
                    
                    transaction_db_delete = "DELETE FROM import.tblYellowpages WHERE companyName_stateabbreviation = " + "'" + companyName_stateabbreviation + "';"
                    sql = "INSERT INTO import.tblYellowpages (" +cols + ") VALUES " + str(tuple(row)) + ";"
                    #s_update = "UPDATE company.Historical_log_data SET Updated_Flag ='Y', lastpulldate = SYSDATETIME()  WHERE companyName_stateabbreviation = " + "'" + companyName_stateabbreviation + "';"
                    s_update =  "exec import.Yellow_page '" + company_name + "', '" + stateid + "' , 'UPDATE'"

                    cursor=cnxn.cursor()
                    cursor.execute(transaction_db_delete)
                    cursor.execute(sql)
                    cursor.execute(s_update)
                    cnxn.commit()
                    
                ################################################################
                    
                jobCount=dataframe_merged.shape[0]
                print(jobCount)
                
                datetime_end = datetime.datetime.now()
                print(f'end time is  {datetime_end} ')
                 
                timediff = math.ceil((datetime_end - datetime_start).seconds) / 60
                
                print(F'task complited in {timediff} minutes')
                
                ################################################################
                # Email
                ################################################################
                
                
                azure_logic_app_endpoint = "https://prod-04.centralus.logic.azure.com:443/workflows/2239b377ec954a4dbca2f52329a5524c/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=BQMAYnHI3O8HnaO2I2jlrgLvY4NT1LjvHDDdvRAtffs"

                payload = {

                        "Severity": "Moderate",
                        "Module": "Module",
                        "Subject": "Subject",
                        "Message": "Scraped record count from Yellow Page for " + str(keyword) + " " + str(place) + " is: " + str(jobCount),
                        "EmailTo": 'sdongol@devfinity.io'

                    }

                headers = {
                        'Content-Type': 'application/json'
                    }

                r = req.post(azure_logic_app_endpoint, data=json.dumps(payload), headers=headers)
                
                cursor.execute(r)
                
                ################################################################
                ################################################################
                
                return

                #return dataframe_merged.to_csv('dataframe_merged_table.csv', encoding="utf-8", index=False)
                       
            elif response.status_code == 404:
                print("Could not find a location matching", place)
                break
            else:
                print("Failed to process page")
                return []
            
              
        except:
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
    
