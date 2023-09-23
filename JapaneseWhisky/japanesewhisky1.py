import pandas as pd
import requests
from bs4 import BeautifulSoup 

base_url = 'https://www.thewhiskyexchange.com/'


url = 'https://www.thewhiskyexchange.com/c/35/japanese-whisky'
r = requests.get(url)
soup = BeautifulSoup(r.text,'html.parser')
products=soup.find_all('li',class_='product-grid__item')
links = []
for item in products:
    #print(item.find('a')['href'])
    links.append(base_url + item.find('a')['href'])

wiskey_list=[]

for link in links:
    r = requests.get(link)
    soup = BeautifulSoup(r.text,'html.parser')
    Product = soup.find('h1',class_='product-main__name').text.strip().replace('\n',' ')
    Price = soup.find('p',class_='product-action__price').text.strip()
    try:
        Review = soup.find('p',class_='review-overview__content').text.strip().replace('\n','').replace('\xa0',' ')
    except AttributeError as err:
        Review='none'
    
    wiskey = {
        'Product': Product,
        'Price': Price,
        'Review': Review
         }
    wiskey_list.append(wiskey)

df= pd.DataFrame(wiskey_list)
print(df)

df.to_csv('wiskey.csv',sep=',',mode='w',encoding='utf-8')
