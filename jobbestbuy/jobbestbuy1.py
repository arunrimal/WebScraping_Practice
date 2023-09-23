from matplotlib.backend_bases import LocationEvent
import requests 
from bs4 import BeautifulSoup 

url = 'https://jobs.bestbuy.com/bby?id=all_jobs&spa=1&s=req_id_num'

r= requests.get(url)
soup = BeautifulSoup(r.text , 'html.parser')

#print(r.status_code)

#print(soup.prettify)

ul_link = soup.find('section', {'class':'flex-grow page sp-scroll'})
print(ul_link)

