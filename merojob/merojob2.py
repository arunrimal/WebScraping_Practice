import requests
#import pandas as pd
from bs4 import BeautifulSoup
from csv import writer
#with open('MeroJobDotCom.csv', 'a', encoding='utf8', newline='') as f:
#    thewriter = writer(f)
#    header = ['JobTitle', 'CompanyName', 'Location', 'KeySkills']
#    thewriter.writerow(header)
#for i in range(1,18):
#    x=i
#    y=str(x)
url = "https://merojob.com/category/it-telecommunication/?page=" + '1'
    #print(url)
req = requests.get(url)
soup = BeautifulSoup(req.content, "html.parser")
lists = soup.find('div', class_="card mt-3 hover-shadow")
   # with open('MeroJobDotCom.csv', 'a', encoding='utf8', newline='') as fi:
       # thewriter1 = writer(fi)
        #for list in lists:
title = lists.find('h1', class_="text-primary font-weight-bold media-heading h4").text.replace('\n', '')
company = lists.find('h3', class_="h6").text.replace('\n', '')
                #company = list.find('span', class_="text-dark")
location = lists.find('span', class_="text-muted").text.replace('\n', '')
skills = (getattr(lists.find('span', attrs={'itemprop': 'skills'}), 'text', None))
s = str(skills)
               # if (s!= "None"):
               #     key_skills = s.replace('\n', ', ')[2:]
               # else:
               #     key_skills = s
               # data = [title, company, location, key_skills]
               # thewriter1.writerow(data)
               # print(data)
print(s)
        #continue