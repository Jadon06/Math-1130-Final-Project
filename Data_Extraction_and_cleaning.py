import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import ssl, certifi, pandas as pd
import urllib.request
from io import StringIO

wages_url = 'https://open.canada.ca/data/en/dataset/adad580f-76b0-4502-bd05-20c125de9116'

class WagesInfo:
    def __init__(self, link, year):
        self.link = link
        self.year = year

    def get_data(self):
        page = requests.get(self.link)
        self.all_wages = BeautifulSoup(page.text, 'html.parser')
    
    def find_dataset(self):
        domain = 'https://open.canada.ca'
        dataset_url = ''
        url_tags = self.all_wages.find_all('a', class_='heading resource-heading')
        for tag in url_tags:
            title = tag.get('title')
            link = tag.get('href')
            if title.split(' ')[0].strip() == str(self.year):
                dataset_url += link
        
        page = requests.get(domain+dataset_url)
        dataset = BeautifulSoup(page.text, 'html.parser')
        full_set_link = dataset.find('a', class_='btn btn-primary resource-url-analytics')
        self.csv_link = ''
        if full_set_link:
            link = full_set_link.get('href')
            self.csv_link += link
        #print(self.csv_link)
        
    def create_dataframe(self):
        page = requests.get(self.csv_link, verify=certifi.where())
        csv_data = StringIO(page.text)
        data = pd.read_csv(csv_data)
        self.df = pd.DataFrame(data)
        return self.df

    def clean_headers(self):
        renamed_headers = [
            "Annual_Wage_Flag",              
            "Average_Wage",                  
            "Data_Source_E",
            "Data_Source_F",
            "ER_Code_Code_RE",
            "ER_Name",
            "High_Wage",                     
            "Low_Wage",                     
            "Median_Wage",                   
            "NOC_CNP",
            "NOC_Title_eng",
            "NOC_Title_French",              
            "ER_Name",                      
            "Non_WageBen_pct",
            "Quartile1_Wage",                
            "Quartile3_Wage",                
            "Reference_Period",
            "Revision_Date",                 
            "Wage_Comment_E",
            "Wage_Comment_French",          
            "_id",
            "prov"
            ]
        
        self.df = self.df.rename(columns={'ï»¿NOC_CNP_2006' : 'NOC_CNP', 'Low_Wage_Salaire_Minium' : 'Minimum_Wage_Salary', 'Median_Wage_Salaire_Median' : 'Median_Wage_Salary', 'High_Wage_Salaire_Maximal' : 'Maximum_Wage_Salary'})
        self.df.drop(['NOC_Title_F', 'Data_Source_F', 'Wage_Comment_F'], axis=1, inplace=True)
        return self.df

    def Display(self):
        print(self.df)