# -*- coding: utf-8 -*-
from account.models import ScrapingLog
from django.utils import timezone
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import math
import csv
import concurrent.futures
    

def boing_scraping():
    datetime_start = datetime.datetime.now()
    print(f'start time is  {datetime_start}' )
    
    def joblist():
        hrefs= []
        num = 40 #- asigning the number of pages to be scraped / 15 records are scraped in each itteration.
        for n in range(1,num+1):

            href = f'https://jobs.boeing.com/search-jobs?glat=27.674999237060547&glon=85.31199645996094/search-jobs/results&p={n}'
            hrefs.append(href)   
        return hrefs 
    
    jobs=joblist()
        
    dframeList = []   
    def boing_extract(href):
        
        headers = {'user_agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
        try:
            page = requests.get(href, headers=headers)
        except Exception as e:  
            page = requests.get(href)
        soup = BeautifulSoup(page.content, 'html.parser')
        block = soup.find( id = 'search-results-list')
        
        block2 = block.find_all('li')
        
        df = pd.DataFrame(columns=['jobTitle','jobID','jobDesc','jobLocation','postedDate','jobUrl','applyUrl'])
        for li in block2:
            
            title = li.find( 'h3').get_text()

            location = li.find('span', class_='job-location job-info').get_text()
            
            job_date =li.find('span', class_='job-date-posted job-info').get_text()
            
            link =li.find('a')
    
            if link.has_attr('href'):
                url = ('https://jobs.boeing.com/'+link['href'])
            #print(url)
            else :
                url = 'not found'
        
            try:
                j_details = requests.get(url, headers = headers)
                
            except Exception as e:  
                j_details = requests.get(url)
                
            soup = BeautifulSoup(j_details.content, 'html.parser')
            block1= soup.find('div', class_ ='ats-description')
    
            J_desc = (block1.find_all('p')[3].get_text())+(block1.find_all('p')[4].get_text())
            #print(J_desc)
    
    
            block10 = block1.find('span', class_='job-id job-info').get_text()
            job_id = (block10.replace("Job ID ", ""))
            #print(job_id)
            
            block11 = soup.find('div', class_ ="job-btn-wrap job-btn-wrap--bottom")
            apply_url = block11.find('a').get('href')
            #print(apply_url)
            
        
            df = df.append({'jobTitle':title,
                                  'jobID':job_id,
                                  'jobDesc':J_desc,
                                  'jobLocation':location,
                                  'postedDate':job_date,
                                  'jobUrl':url,
                                  'applyUrl':apply_url,}, ignore_index=True)
           
        dframeList.append(df)
        
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        executor.map(boing_extract, jobs)
    
    Boing_df = pd.concat(dframeList)   
    
    
    
        
    datetime_end = datetime.datetime.now()
    print(f'end time is  {datetime_end} ')
    
    timediff = math.ceil((datetime_end-datetime_start).seconds)/60

    print(F'task complited in {timediff} minutes')
    
    return Boing_df.to_csv(quoting=csv.QUOTE_ALL, encoding='utf-8', index=False)

