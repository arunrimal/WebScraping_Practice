from lib2to3.pgen2.token import NEWLINE
from operator import index
from os import sep
from tkinter.ttk import Separator
from matplotlib.pyplot import text
import pandas as pd
import requests
from bs4 import BeautifulSoup

df = pd.DataFrame(columns=['Job Title','Company','Location','Skills'])

for page in range(1,21):
    url = f"https://merojob.com/category/it-telecommunication/?page={page}"

    page = requests.get(url)

    #print(url)

    #print(page.text)

    soup = BeautifulSoup(page.text,'html.parser')
    #soup = BeautifulSoup(requests.get(url, cookies=cookies).content, "html.parser")
    #soup.prettify
    

    result = soup.find_all('div', {'class':'col-8 col-lg-9 col-md-9 pl-3 pl-md-0 text-left'})
    for row in result:
        job_title = row.find('a').text.strip()
        com_name = row.find('h3',{'class':'h6'}).text.strip()
        try:
            loc = row.find('div',{'class':'location font-12'}).text.strip()
        except AttributeError as err:
            loc='none'
        try:
            key_skills = row.find('span',{'itemprop':'skills'}).text.replace('\n', ',')[1:]
            #key_skills=key_skills.replace('\n', ',')
        except AttributeError as err:
            key_skills='none'
        #key_skills = getattr(list.find('span',{'itemprop':'skills'}, 'text', None))
        #for ele in key_skills:
        #   k_skl = key_skills.span.text
        #data = [job_title,com_name,loc,key_skills]
       # print(data)
        df=df.append({'Job Title':job_title,'Company':com_name,'Location':loc,'Skills':key_skills},ignore_index=True)
        
    continue
#print(df)

#print(df)
#print(key_skills)
df.to_csv('merojob.csv',index=False,encoding='utf-8')

