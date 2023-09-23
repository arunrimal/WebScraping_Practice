from matplotlib.backend_bases import LocationEvent
import requests 
from bs4 import BeautifulSoup 
url = "https://jobs.cisco.com/jobs/SearchJobs/"

r = requests.get(url)
htmlcontent = r.text

soup = BeautifulSoup(htmlcontent, 'html.parser')


result = soup.find('table', attrs = {'class':'table_basic-1 table_striped', 'summary' :'Search Results'}) #.text.strip()

result_body = result.find('tbody')
#print(len(result_body))
#print(result_body[1:100])
result_row = result_body.find_all('tr')
#print(len(result_row))
#print(result_row)

for result_row in result_body:
   job_title = result_row.find('a')
   print(job_title)
    #job_url
    #area_of_interest
    #loc
    #alternate_loc


#first_row = result_row[0]
#print(first_row)



# Extracting Job Title, Area of Interest, Job Type, Location, Alternate Location




