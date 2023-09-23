from django.utils import timezone
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import math
import csv
import concurrent.futures

def abbvie_Scraping():

    datetime_start = datetime.datetime.now()
    print(f'start time is  {datetime_start}')
    headers = {'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}

    def urlList():

        hrefs = []

        for i in range(1, 200):
            href = f'https://careers.abbvie.com/api/jobs?page={i}&internal=false&atsCode=abbvie-prod-taleo%7Cagn-prod-taleo%7Callergan-prod-taleo&userId=c0f10d91-6e9b-40ab-82b7-c21fd6427ded&sessionId=47a2b2f0-acd4-'
            hrefs.append(href)

        return hrefs

    page = urlList()

    dframeList = []

    def abbvie_extract(href):

        try:
            req = requests.get(href, headers=headers)

        except Exception as e:
            req = requests.get(href)

        soup = BeautifulSoup(req.content, 'html.parser')
        job = json.loads(str(soup))
        job_d = job['jobs']
        l = len(job)

        df = pd.DataFrame(columns=['JobTitle', 'JobID', 'DatePosted', 'JobLocation', 'Company', 'JobLink', 'JobDesc', 'ApplyURL'])

        for j in range(l):

            list = (job_d[j])

            sub_d = list['data']

            title = sub_d['title']

            company = "AbbVie"

            job_id = sub_d['req_id']

            date_posted = sub_d['posted_date']

            job_location = str(sub_d['meta_data']['googlejobs']['derivedInfo']['locations'][0]['postalAddress']['addressLines']).replace("['", '').replace("']", '')

            job_link = f"https://careers.abbvie.com/abbvie/jobs/{job_id}?lang=en-us&previousLocale=en-US"

            job_desc = sub_d['description']

            apply_link = sub_d['apply_url']

            df = df.append({'JobTitle': title,
                            'JobID': job_id,
                            'DatePosted': date_posted,
                            'JobLocation': job_location,
                            'Company': company,
                            'JobLink': job_link,
                            'JobDesc': job_desc,
                            'ApplyURL': apply_link, }, ignore_index=True)

        dframeList.append(df)

    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        executor.map(abbvie_extract, page)

    abbvie_df = pd.concat(dframeList)

    print(abbvie_df)

    datetime_end = datetime.datetime.now()
    print(f'end time is  {datetime_end} ')

    timediff = math.ceil((datetime_end - datetime_start).seconds) / 60

    print(F'task complited in {timediff} minutes')
    abbvie_df.to_csv('AbbVie.csv', quoting=csv.QUOTE_ALL, encoding='utf-8', index=False)

abbvie_Scraping()