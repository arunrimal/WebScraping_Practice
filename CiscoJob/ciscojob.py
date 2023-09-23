from matplotlib.backend_bases import LocationEvent
import requests 
from bs4 import BeautifulSoup 
url = "https://jobs.cisco.com/jobs/SearchJobs/"

r = requests.get(url)
htmlcontent = r.text
#print(htmlcontent[10000:16000])

soup = BeautifulSoup(htmlcontent, 'html.parser')
#print(soup)
#print(soup.prettify)

#title = soup.title
#print(title)

result = soup.find('table', attrs = {'class':'table_basic-1 table_striped', 'summary' :'Search Results'}) #.text.strip()
#print(len(result))
#print(result)
result_body = result.find('tbody')
#print(len(result_body))
#list_content = result_body.contents
#print(result_body)

print(result_body.contents[1])

result_row = result_body.find_all('tr')

print(result_row)

#result_row = result_body.find_all('tr')
#print(len(result_row))
#print(result_row[0:2])
