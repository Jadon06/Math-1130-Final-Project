import Data_Extraction_and_cleaning as data
import Post_Pandemic_Data as pdd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

all_data = [pdd.Data_2015, pdd.Data_2016, pdd.Data_2017, pdd.Data_2018, pdd.Data_2019, 
            pdd.Data_2020, pdd.Data_2021, pdd.Data_2022]

all_dfs = []
for yearly_data in all_data:
    yearly_data.get_data()
    yearly_data.find_dataset()
    df = yearly_data.create_dataframe()
    all_dfs.append(df)

#for df in all_dfs:
 #   print(list(df.columns))
all_cleaned_dfs = []
# Manually check each dataframe column from 2015-2019 to clean and adjust them since the column names from 2015-2019 are slightly different
# 2015
new_column_names = ['NOC_CNP', 'NOC_TITLE', 'PROV', 'ER_CODE', 'ER_NAME', 'LOW_WAGE', 'MEDIAN_WAGE', 'HIGH_WAGE',
                     'DATA_SOURCE', 'REFERENCE_PERIOD', 'REVISION_DATE', 'ANNUAL_WAGE_FLAG']
all_dfs[0].dropna(subset=["Low_Wage_Salaire_Minium","Median_Wage_Salaire_Median","High_Wage_Salaire_Maximal"])
all_dfs[0].drop(["Data_Source_F", "NOC_Title_F", "Wage_Comment_E", "Wage_Comment_F"], axis=1, inplace=True)
new_df_2015 = all_dfs[0][all_dfs[0]["Annual_Wage_Flag_Salaire_annuel"] != 0].copy()
new_df_2015.rename(columns = dict(zip(new_df_2015.columns, new_column_names)), inplace=True)
new_df_2015["Year"] = "2015"
all_cleaned_dfs.append(new_df_2015)
# 2016
all_dfs[1].dropna(subset=["Low_Wage_Salaire_Minium","Median_Wage_Salaire_Median","High_Wage_Salaire_Maximal"])
all_dfs[1].drop(["Data_Source_F", "Titre_CNP", "Wage_Comment_E", "Wage_Comment_F", "Annual_Wage"],axis=1, inplace=True)
new_df_2016 = all_dfs[1][all_dfs[1]["Annual_Wage_Flag_Salaire_annuel"] != 0].copy()
new_df_2016.rename(columns = dict(zip(new_df_2016.columns, new_column_names)), inplace=True)
new_df_2016["Year"] = "2016"
new_df_2016["MEDIAN_WAGE"] = new_df_2016["MEDIAN_WAGE"]*2080 # Estimate the annual median salary by multiplying the median horuly rate by the estimated number of hours worked per year, formula = 8hrs/day x number of weekdays in a yr(260)
all_cleaned_dfs.append(new_df_2016)
# 2017
all_dfs[2].dropna(subset=['Low Wage_Salaire Minium','Median wage_Salaire Median', 'High Wage_Salaire maximal'])
all_dfs[2].drop(['Titre CNP', 'Source de donnees', 'Wage_Comment_E', 'Wage_Comment_F'], axis=1, inplace=True)
new_df_2017 = all_dfs[2][all_dfs[2]['Annual Wage Flag_Salaire annuel'] != 0].copy()
new_df_2017.rename(columns = dict(zip(new_df_2017.columns, new_column_names)), inplace=True)
new_df_2017["Year"] = "2017"
all_cleaned_dfs.append(new_df_2017)
# 2018
all_dfs[3].dropna(subset=['Low Wage_Salaire Minium','Median wage_Salaire Median', 'High Wage_Salaire maximal'])
all_dfs[3].drop(['Titre CNP', 'Source de donnees', 'Wage_Comment', 'Commentaire_Salaire'], axis=1, inplace=True)
new_df_2018 = all_dfs[3][all_dfs[3]['Annual Wage Flag_Salaire annuel'] != 0].copy()
new_order = ['NOC_CNP', 'NOC Title', 'Prov', 'ER Code_Code RE', 'ER Name_Nom RE', 'Low Wage_Salaire Minium', 
             'Median wage_Salaire Median', 'High Wage_Salaire maximal', 'Data Source', 'Reference Period_Periode de reference', 
             'Revision Date_Date revision', 'Annual Wage Flag_Salaire annuel']
new_df_2018_reordered = new_df_2018
new_df_2018_reordered.rename(columns = dict(zip(new_df_2018.columns, new_column_names)), inplace=True)
new_df_2018["Year"] = "2018"
all_cleaned_dfs.append(new_df_2018)
# 2019
all_dfs[4].dropna(subset=["Low_Wage_Salaire_Minium","Median_Wage_Salaire_Median","High_Wage_Salaire_Maximal"])
all_dfs[4].drop(["Data_Source_F", "Titre_CNP", "Wage_Comment_E", "Wage_Comment_F1"],axis=1, inplace=True)
new_df_2019 = all_dfs[4][all_dfs[4]["Annual_Wage_Flag_Salaire_annuel"] != 0].copy()
new_df_2019.rename(columns = dict(zip(new_df_2019.columns, new_column_names)), inplace=True)
new_df_2019["Year"] = "2019"
all_cleaned_dfs.append(new_df_2019)

year = 2020
for i in range(5, len(all_data)):
    all_dfs[i].dropna(subset=["Low_Wage_Salaire_Minium","Median_Wage_Salaire_Median","High_Wage_Salaire_Maximal"])
    all_dfs[i].drop(["Data_Source_F", "Titre_CNP", "Wage_Comment_E", "Wage_Comment_F"],axis=1, inplace=True)
    if "Average_Wage_Salaire_Moyen" in list(all_dfs[i]):
        all_dfs[i].drop(["Average_Wage_Salaire_Moyen"], axis = 1, inplace=True)
    new_df = all_dfs[i][all_dfs[i]["Annual_Wage_Flag_Salaire_annuel"] != 0].copy()
    new_df.rename(columns = dict(zip(new_df.columns, new_column_names)), inplace=True)
    new_df["Year"] = str(year)
    all_cleaned_dfs.append(new_df)
    year+=1

pdd.cleaned_2023_df["Year"] = "2023"
pdd.cleaned_2024_df["Year"] = "2024"
pdd.cleaned_2023_df.drop(["AVERAGE_WAGE"], axis=1, inplace=True)
pdd.cleaned_2024_df.drop(["AVERAGE_WAGE"], axis=1, inplace=True)
all_cleaned_dfs.append(pdd.cleaned_2023_df)
all_cleaned_dfs.append(pdd.cleaned_2024_df)

final_df = pd.DataFrame()

for dataframe in all_cleaned_dfs:
    final_df = pd.concat([final_df, dataframe], ignore_index=True)
#print(final_df)

mapping = {
    "Newfoundland and Labrador": "NL",
    "Prince Edward Island": "PE",
    "Nova Scotia": "NS",
    "New Brunswick": "NB",
    "QuÃ©bec": "QC",
    "Ontario": "ON",
    "Manitoba": "MB",
    "Saskatchewan": "SK",
    "Alberta": "AB",
    "British Columbia": "BC",
    "Yukon Territory": "YT",
    "Northwest Territories": "NT",
    "Nunavut": "NU",
    "National": "NAT",
    "CA": "CA" 
}

final_df["PROV"] = final_df["PROV"].replace(mapping)

x_values = list(final_df["Year"].unique())
NewLab = list(final_df[final_df["PROV"] == "NL"].groupby("Year")["MEDIAN_WAGE"].median())
PrinceEd = list(final_df[final_df["PROV"] == "PE"].groupby("Year")["MEDIAN_WAGE"].median())
NovaScotia = list(final_df[final_df["PROV"] == "NS"].groupby("Year")["MEDIAN_WAGE"].median())
NewBruns = list(final_df[final_df["PROV"] == "NB"].groupby("Year")["MEDIAN_WAGE"].median())
Quebec = list(final_df[final_df["PROV"] == "QC"].groupby("Year")["MEDIAN_WAGE"].median())
Ont = list(final_df[final_df["PROV"] == "ON"].groupby("Year")["MEDIAN_WAGE"].median())
Manitoba = list(final_df[final_df["PROV"] == "MB"].groupby("Year")["MEDIAN_WAGE"].median())
Sask = list(final_df[final_df["PROV"] == "SK"].groupby("Year")["MEDIAN_WAGE"].median())
Alb = list(final_df[final_df["PROV"] == "AB"].groupby("Year")["MEDIAN_WAGE"].median())
BritCol = list(final_df[final_df["PROV"] == "BC"].groupby("Year")["MEDIAN_WAGE"].median())
YukTerr = list(final_df[final_df["PROV"] == "YT"].groupby("Year")["MEDIAN_WAGE"].median())
NorthETerr = list(final_df[final_df["PROV"] == "NT"].groupby("Year")["MEDIAN_WAGE"].median())
Nunavut = list(final_df[final_df["PROV"] == "NU"].groupby("Year")["MEDIAN_WAGE"].median())

provinces = [NewLab, PrinceEd, NovaScotia, NewBruns, Quebec, Ont, Manitoba, Sask, Alb,
             BritCol, YukTerr, NorthETerr, Nunavut]

for province in provinces:
    if len(province) < len(x_values):
        for i in range(len(province), len(x_values)):
            province.append(np.nan)

sns.lineplot(x=x_values, y=NewLab, color='orange', label="Newfoundland & Labrador")
sns.lineplot(x=x_values, y=PrinceEd, color='green', label="Prince Edward Island")
sns.lineplot(x=x_values, y=NovaScotia, color='purple', label="Nova Scotia")
sns.lineplot(x=x_values, y=NewBruns, color='yellow', label="New Brunswick")
sns.lineplot(x=x_values, y=Quebec, color='blue', label="Newfoundland & Labrador")
sns.lineplot(x=x_values, y=Ont, color='red', label="Ontario")
sns.lineplot(x=x_values, y=Manitoba, color='brown', label="Manitoba")
sns.lineplot(x=x_values, y=Sask, color='olive', label="Saskatchewan")
sns.lineplot(x=x_values, y=Alb, color='black', label="Alberta")
sns.lineplot(x=x_values, y=BritCol, color='cyan', label="British Columbia")
#sns.lineplot(x=x_values, y=YukTerr, color='pink', label="Yukon Territories")
#sns.lineplot(x=x_values, y=NorthETerr, color='lightsteelblue', label="North East Territories")
#sns.lineplot(x=x_values, y=Nunavut, color='maroon', label="Nunavut")
plt.xlabel("Year")
plt.ylabel("Median Annual Wages")
plt.title("Median Wages by Year for each Province")
plt.legend()
plt.show()