from bs4 import BeautifulSoup
import requests
import csv
from time import sleep
from random import randint
from datetime import datetime
from selenium import webdriver
import time
import pandas as pd
import re
import numpy as np
import html5lib

def get_url(position, location):
    position = position.replace(' ','-')
    template = 'https://www.naukri.com/{}-jobs-in-{}'
    url = template.format(position, location)
    return url

def get_data(j,datax,sou):
    for jobs in j:
        title = jobs.find(class_='title').text
        Company = jobs.find(class_='subTitle').text
        Salary = jobs.find(class_='salary').text
        try:
            Experience = jobs.find(class_='experience').text
        except AttributeError:
            Experience = ''
        tags = []
        for k in jobs.findAll(class_='fleft fs12 grey-text lh16 dot'):
            tags.append(k.text)
        date = jobs.findAll(class_='fleft fw500')
        date = [i.text for i in date]
        #print(title,Company,Salary,Experience,tags,date)
        datax = datax.append({"Title":title,"Company":Company,"Salary":Salary,"Experience":Experience,"Requirements":tags,"Posted":date},ignore_index=True)
    #print(datax)
    href = sou.findAll('a',class_="fright",href=True)[0].get('href')
    url = "https://www.naukri.com"+href
    return url,datax   

def scrape(url):
    driver = webdriver.Chrome("C:\\Users\\Shivakumar\\Downloads\\chromedriver.exe")
    driver.get(url)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source,'html5lib')
    #print(soup.prettify())
    driver.close()
    print('1')
    return soup

def main(title,location):

    url = get_url(title,location)
    data = pd.DataFrame(columns=['Title','Company','Salary','Experience','Requirements','Posted'])
    for i in range(2):
        soup = scrape(url)
        j = soup.findAll('article',class_ = 'jobTuple')
        url,datax = get_data(j,data,soup)
        #print(datax)
        data = data.append(datax,ignore_index=True)
    return data
# def main(title,location):

#   url = get_url(title,location)
#   data = pd.DataFrame(columns=['Title','Company','Salary','Experience','Requirements','Posted'])
#   for i in range(1):
#     soup = scrape(url)
#     j = soup.findAll('article',class_ = 'jobTuple')
#     url,datax = get_data(j,data,soup)
#     #print(datax)
#     data = data.append(datax,ignore_index=True)
#   return data


def final_df(final_df):
  Company = final_df['Company'].values.tolist()
  sals = final_df['Salary'].values.tolist()
  sals = list(filter(lambda x : x!='Not disclosed',sals))
  sals = [i.split(' - ') for i in sals]
  #print(sals)
  sals = [(i[0],i[1].replace(' PA.','')) for i in sals]
 # print(sals)
  sals  = [[int(i[0].replace(',','')), 1.5*int(i[0].replace(',','')) if re.search("[a-zA-Z]",i[1]) else int(i[1].replace(',',''))] for i in sals]
 # print(sals)
  sals  = np.array(sals)
  #print(sals)
  title = final_df['Title'].values.tolist()
  exp = list(filter(lambda x: x!='',final_df['Experience'].values.tolist()))
  exp = [i.replace(' Yrs','') for i in exp]
  exp = [[int(i.split('-')[0]),int(i.split('-')[1])] for i in exp]
  exp = np.array(exp) 
  req =final_df['Requirements'].values.tolist()
  requirements = []
  for i in req:
    for j in i:
      requirements.append(j.lower().strip())
  date = final_df['Posted'].values.tolist()
  days_ago = []
  for i in date:
    for j in i:
      if re.search('[1-9]',j):
        j = j.replace('+','')
        j = j.split(' ')[0]
        days_ago.append(int(j))
  values = {"Company":Company,"Salary":sals,"Title":title,"Experience":exp,"Requirements":requirements,"Date":days_ago}
  return values

# data = main('accountant','bangalore')
# print(data)
# df = final_df(data)
# print(df)


