import requests
import urllib.request
import time
import numpy as np
import pandas as pd
import csv
from bs4 import BeautifulSoup


url = 'https://virihealth.com/'


outfile = open("table_data.csv","w",newline='')
writer = csv.writer(outfile)

response = requests.get(url)
tree = BeautifulSoup(response.text,"lxml")
table_tag = tree.select("table")[8]
tab_data = [[item.text for item in row_data.select("th,td")]
                for row_data in table_tag.select("tr")]

for data in tab_data:
    writer.writerow(data)
    print(' '.join(data))


df1 = pd.DataFrame(tab_data,columns=tab_data[0])
df1 = df1.iloc[1:,:]
df1['Date'] = df1['Date'] + '-2020' 
df1['date_time'] = pd.to_datetime(df1['Date'],format='%d-%b-%Y')  
df1.to_csv('./data_canada_covid_mar_19.csv') 

df_by_day = df1.groupby(['date_time'])['#'].count().reset_index() 
df_by_day['cumsum'] = df_by_day['#'].cumsum() 

df_by_day[df_by_day['cumsum']>99].set_index('date_time')['cumsum'].plot()

plt.yscale('log')

plt.title('log linear plot of cumulative covid cases canada')

