import requests
import urllib.request
import time
import numpy as np
import pandas as pd
import csv
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

#canada data
url = 'https://virihealth.com/'

response = requests.get(url)
tree = BeautifulSoup(response.text,"lxml")

table_tag = tree.find('table',id='igsv-12-1C59nxtgcnwGyo6lgypsgN18duxmwWigjeVdKY58t0mU') #select("table")[7]
tab_data = [[item.text for item in row_data.select("th,td")]
                for row_data in table_tag.select("tr")]

df1 = pd.DataFrame(tab_data,columns=tab_data[0])
df1 = df1.iloc[1:,:]
df1['Date'] = df1['Date'] + '-2020' 
df1['date_time'] = pd.to_datetime(df1['Date'],format='%d-%b-%Y')  
df1.to_csv('./data_canada_covid_mar_19.csv') 

df_by_day = df1.groupby(['date_time'])['#'].count().reset_index() 
df_by_day['cumsum'] = df_by_day['#'].cumsum() 

df_by_day[df_by_day['cumsum']>99].set_index('date_time')['cumsum'].plot()

plt.yscale('log')

plt.title('log plot of cumulative covid cases canada - since 100th case')


###world date

url1 = 'https://www.worldometers.info/coronavirus/#countries'


response = requests.get(url1)
tree = BeautifulSoup(response.text,"lxml")
table_tag = tree.find('table',id='main_table_countries_today') 
tab_data = [[item.text for item in row_data.select("th,td")]
                for row_data in table_tag.select("tr")]

df2 = pd.DataFrame(tab_data,columns=tab_data[0])
df2 = df2.iloc[1:,:]