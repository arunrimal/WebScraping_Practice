import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://themes.woocommerce.com/storefront/product-category/clothing/page/1'

r= requests.get(url)
#print(r.text)

page = BeautifulSoup(r.text,'html.parser')
#print(page)

items = page.find_all('ul',class_='products')
#print(items)
header = ['Product Name','Price','Link']
df = pd.DataFrame(columns=header)

for item in items:
    product_name= item.find('h2').text
    price= item.find('span').text
    product_link= item.find('a').get('href')
   # df.append[product_name,price,product_link]
print(product_link)