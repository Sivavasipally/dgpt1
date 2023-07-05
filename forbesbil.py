import requests
import pandas as pd

#r = requests.get('https://www.forbes.com/ajax/list/data?year=2017&uri=billionaires&type=person')
url = 'https://www.forbes.com/billionaires/page-data/index/page-data.json'
r = requests.get(url,verify=False)
datadic = []
data = r.json()
for item in data['result']['pageContext']['tableData']:
    datadic.append(item)

df = pd.DataFrame(datadic)
df.to_csv('forbes.csv',index=False)
