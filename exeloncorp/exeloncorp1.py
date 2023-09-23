from html import entities
import math
from itsdangerous import json
import pandas as pd
import requests
import datetime

from sqlalchemy import column

start_time = datetime.datetime.now()

url='https://jobs.exeloncorp.com/search/jobs.json?current_page=1&per_page=1000'
req = requests.get(url=url)

response = req.json()




print(list(response))
dict_list = []
#print(response['entries'])
for item in response['entries']:
    title = item['title']
    street = item['location']['street']
    country = item['location']['country']
    
    dict={
        'title':title,
        'street':street,
        'country':country
    }
    print(dict)
    dict_list.append(dict)
    
end_time = datetime.datetime.now()
timedifrns = math.ceil((end_time - start_time).seconds) / 60

df = pd.DataFrame(columns=dict.keys)
print(dict.keys)

print(timedifrns)





