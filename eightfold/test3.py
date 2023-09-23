def eightFoldScrapping():
    import requests as req
    import json
    import pandas as pd
    import datetime,concurrent.futures
    import math
    import csv
    # domain name for the api call . 
    start_time = datetime.datetime.now()

    domainName=['nationwide','prudential']
    dataset=[]
    # Main Function for scrapping from Source ATS. Parameters to be passed is domain i.e 'nationwide' and 'prudential' for now 

    def eightFoldScrapper(domain):


        # Currently only 60 records are scrapped from one source  as we reach the request limit .
        for i in range(1,7):

            # Main Api Urls 
            Apiurl=f'https://nationwide.eightfold.ai/api/apply/v2/jobs?domain={domain}.com&start={i}0&num=100'
            # Main Url call gets 10 id per request.

            mainResp = req.get(Apiurl)

            if mainResp.status_code !=404:
                MainresponseJson=json.loads(mainResp.text)
                MainpositionJson=MainresponseJson['positions']
                # Itterating through the jobs details and  appending in dataframe
                for jobs in MainpositionJson:
                    jobID=jobs['id']
                    jobAtsID=jobs['ats_job_id']
                    companyname=MainresponseJson['branding']['companyName']
                    jobTitle=jobs['name']
                    createdDate = datetime.datetime.fromtimestamp(jobs['t_create'])
                    updatedDate = datetime.datetime.fromtimestamp(jobs['t_update'])
                    # Details page request 
                    detailUrl=f'https://nationwide.eightfold.ai/api/apply/v2/jobs/{jobID}?domain={domain}.com'
                    detailsResp = req.get(detailUrl)
                    DetailsresponceJson=json.loads(detailsResp.text)

                    # Finding the details of the page request 
                    #jobDescription=DetailsresponceJson['job_description']
                    jobDescription=DetailsresponceJson['job_description'].replace('"', '')
                    applyUrl=DetailsresponceJson['apply_redirect_url']
                    jobLocation=DetailsresponceJson['location']
                    jobDepartment=DetailsresponceJson['department']

                    # Appending in data frame the details of the page request 
                    dataset.append([jobID,jobAtsID,jobTitle,jobLocation,jobDescription,applyUrl,companyname,jobDepartment,detailUrl,createdDate,updatedDate])


    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        executor.map(eightFoldScrapper,domainName)
        
    # Creating data frame and appending dataset
    JobDataFrame = pd.DataFrame(columns = ['id','jobAtsID', 'jobTitle', 'jobLocation', 'jobDescription', 'applyUrl', 'company_name', 'jobDepartment', 'apiUrl','createdDate','updatedDate'],data=dataset)

    jobCount=JobDataFrame.shape[0]
    end_time = datetime.datetime.now()
    print(f'Finished in {jobCount} records in {math.ceil((end_time - start_time).seconds) / 60} minutes')
    global timedifrns
    timedifrns = math.ceil((end_time - start_time).seconds) / 60
        #return JobDataFrame

    return(print(timedifrns,len(JobDataFrame),jobCount))

    #ScrapingLog(source='EightFold',
    #            time_taken_minutes=timedifrns,
    #            rows_affected=len(JobDataFrame),
    #            scrap_date=timezone.now(),
    #            status=True).save()

    #return JobDataFrame.to_csv(encoding="utf-8", quoting=csv.QUOTE_ALL, index=False)

eightFoldScrapping()