import csv
from matplotlib.backend_bases import LocationEvent
from matplotlib.pyplot import table
import requests 
from bs4 import BeautifulSoup 
url = "https://jobs.cisco.com/jobs/SearchJobs/"

r = requests.get(url)
htmlcontent = r.text

soup = BeautifulSoup(htmlcontent, 'html.parser')
#print(soup)
#print(soup.prettify)

#title = soup.title
#print(title)

table = soup.find('table', attrs = {'class':'table_basic-1 table_striped', 'summary' :'Search Results'}) #.text.strip()
#print(table)
row_list= [] 
for tr in table.find_all('tr')[1:]: # first <th> is excluded because it contains table header
        #job_title = rows.find('td', {'scope':'row', 'data-th':'Job Title', 'scope':'row'}).text
        #job_url = rows.find('td', 'a'['href'])
        data = tr.find_all('td')
        row_data = [td.text.strip() for td in data]
        row_list.append(row_data) 
#print(row_list[0])

data_header = ['Job Title', 'Area of Interest', 'Job Type', 'Location', 'Alternate Location']

with open('ciscojob2.csv','w',newline='') as csvfile:
  write = csv.writer(csvfile)
  write.writerow(data_header)
  for i in range (0,len(row_list)):
      write.writerow(row_list[i])

  

        


# Extracting Job Title, Area of Interest, Job Type, Location, Alternate Location




