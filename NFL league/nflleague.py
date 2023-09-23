from bs4 import BeautifulSoup
import pandas as pd
import requests

# geting the html
url = 'https://www.nfl.com/standings/league/2021/REG'

page = requests.get(url)

soup = BeautifulSoup(page.text, 'lxml')
soup

# geting the table

table = soup.find('table', {'summary':'Standings - Detailed View'})

# geting the headers of the table
# first create the empty list 
Header = []

for i in table.find_all('th'):
    title = i.text.strip()
    Header.append(title)

#print(Header)

df = pd.DataFrame(columns=Header)

for row in table.find_all('tr')[1:]:
    data = row.find_all('td') # finds all the the data in each row
    row_data = [td.text.strip() for td in data] # gets only text from each td s 
    length = len(df)
    df.loc[length]=row_data
print(row_data)
#print(df)
#df.to_csv('NFLleague.csv',index=False, encoding='utf-8')
