import requests
from bs4 import BeautifulSoup
import pandas as pd
# external lib : pip install requests
# external lib : pip install beautifulsoup4
# external lib : pip install pandas
# Street names from: https://geographic.org/streetview/singapore/index.html

url = 'https://geographic.org/streetview/singapore/index.html'
page = requests.get(url)

soup = BeautifulSoup(page.content)

list_names = []
for li in soup.find_all('li'):
    names = soup.find('a', alt=True)
    text = names.getText()
    list_names.append(li.getText().split('\n')[0])

df = pd.DataFrame(list_names)
df.to_csv('streetname.csv', index=False, header=False)

# print(df)