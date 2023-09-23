import sys
s= sys.path.append("..")
print(s)

#from pyazure.views import get_job_source_data 
#sys.path.append(r"C:\Users\Dell\Desktop\WebScraping\pyazure1")
from WebScraping.pyazure1.views import get_job_source_data 
#from account.models import ScrapingLog
import csv
import os

from django.utils import timezone

def greenhouse_scraping():
    """Scraps the Greenhouse data.

    Retrieves the source url from [Import].[GreenhouseSourceTable] and scraps job data from the
    respective urls and stores it into Pandas Dataframe and Logs the information into ScrapingLog.

    Args:
      None

    Returns:
      A csv consisting of Greenhouse job data.
    """
    import json, datetime
    import pandas as pd
    import requests as req
    import concurrent.futures

    start_time = datetime.datetime.now()
   

    #importing data from azure oasis transactional db
    JobBoardURL_list, CompanyUUID_list = get_job_source_data('[Import].[GreenhouseSourceTable]')
    datasets = []
    # scraping data from the web and appending to dataframe
    def get_greenhouse_data(*JobBoardURLAndId):
        print(JobBoardURLAndId)
        #print(JobBoardURLAndId[1])
        resp = req.get(JobBoardURLAndId[0])
        response = json.loads(resp.text)
        res_jobs = response['jobs']
        for j in res_jobs:
            datasets.append([
                str(JobBoardURLAndId[1]),
                j['absolute_url'],
                j['location']['name'],
                j['internal_job_id'],
                j['id'],
                j['updated_at'],
                j['title'],
                j['content'],
            ])
            


    
 
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(get_greenhouse_data, JobBoardURL_list, CompanyUUID_list)

    #creating a dataframe for our data
    my_df = pd.DataFrame(columns = ['company_uuid', 'absolute_url', 'locationName', 'internal_job_id', 'id', 'updated_at', 'title', 'content'], data = datasets)
    print(my_df)
    end_time = datetime.datetime.now()
    time_taken_minutes = ((end_time - start_time).seconds) / 60
    print(f'Finished in {time_taken_minutes} minutes')

    #ScrapingLog(source='Greenhouse',
    #    time_taken_minutes=time_taken_minutes,
    #    rows_affected=len(my_df),
    #    scrap_date=timezone.now(),
    #    status=True).save()

    #return my_df.to_csv(index=False, quoting=csv.QUOTE_ALL, encoding='utf-8')

greenhouse_scraping()