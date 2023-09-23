import requests
#import pandas as pd
from bs4 import BeautifulSoup
from csv import writer
with open('MetLife.csv', 'a', encoding='utf8', newline='') as f:
    thewriter = writer(f)
    header = ['JobTitle', 'Location', 'DatePosted']
    thewriter.writerow(header)
req = requests.get("https://jobs.metlife.com/search/?createNewAlert=false&q=&locationsearch=")
soup = BeautifulSoup(req.content, "html.parser")
lists = soup.find_all('tr', class_="data-row clickable")
with open('MetLife.csv', 'a', encoding='utf8', newline='') as fi:
    thewriter1 = writer(fi)
    for list in lists:
            title = getattr(list.find('a', class_= 'jobTitle-link'), 'text', None)
            date_posted = (list.find('span', class_="jobDate visible-phone").text.replace('\t', '').replace('\n', '').replace(' ','')).replace(',',', ')
            location = (getattr(list.find('span', class_="jobLocation"), 'text', None).replace('\n', '').replace(' ','')).replace(',',', ')
            data = [title, location, date_posted]
            thewriter1.writerow(data)
            print(data)
lists1 = soup.find_all('span', class_='paginationLabel')
z = int(str(lists1).replace('</b></span>','')[-4:-3])
#print(z)
for i in range(1,z+1):
    u = str(i*100)
    url = "https://jobs.metlife.com/search/?q=&sortColumn=referencedate&sortDirection=desc&startrow="+u
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    lists1 = soup.find_all('tr', class_="data-row clickable")
    with open('MetLife.csv', 'a', encoding='utf8', newline='') as fi:
        thewriter1 = writer(fi)
        for list in lists1:
            title1 = getattr(list.find('a', class_='jobTitle-link'), 'text', None)
            date_posted1 = (list.find('span', class_="jobDate visible-phone").text.replace('\t', '').replace('\n','').replace(' ','')).replace(',',', ')
            location1 = (getattr(list.find('span', class_="jobLocation"), 'text', None).replace('\n', '').replace(' ', '')).replace(',',', ')
            data1 = [title1, location1, date_posted1]
            thewriter1.writerow(data1)
            print(data1)