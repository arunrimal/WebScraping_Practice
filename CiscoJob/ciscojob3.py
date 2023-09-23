from matplotlib.backend_bases import LocationEvent
from matplotlib.pyplot import table
import pandas as pd
import requests 
from bs4 import BeautifulSoup 
url = "https://jobs.cisco.com/jobs/SearchJobs/"

r = requests.get(url)
htmlcontent = r.text

soup = BeautifulSoup(htmlcontent, 'html.parser')

table = soup.find('table', attrs = {'class':'table_basic-1 table_striped', 'summary' :'Search Results'}) #.text.strip()

df = pd.DataFrame(columns=['Job Title', 'Area of Interest', 'Job Type', 'Location', 'Alternate Location'])

for row in table.tbody.find_all('tr'):
    columns = row.find_all('td')
    #print(columns)    

    if(columns !=[]):
        job_title = columns[0].text.strip()
        area_of_interest = columns[1].text.strip()
        job_type = columns[2].text.strip()
        loc = columns[3].text
        alt_loc = columns[4].text

        df = df.append({'Job Title':job_title , 'Area of Interest':area_of_interest, 'Job Type': job_type, 'Location':loc,
        'Alternate Location':alt_loc}, ignore_index=True)          


#print(df)
df.to_csv('ciscojob.csv',index=False, encoding='utf-8')
# Extracting Job Title, Area of Interest, Job Type, Location, Alternate Location




