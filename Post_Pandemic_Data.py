import Data_Extraction_and_cleaning as data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

Data_2023 = data.WagesInfo(data.wages_url, 2023)
Data_2024 = data.WagesInfo(data.wages_url, 2024)
Data_2022 = data.WagesInfo(data.wages_url, 2022)
Data_2021 = data.WagesInfo(data.wages_url, 2021)
Data_2020 = data.WagesInfo(data.wages_url, 2020)
Data_2019 = data.WagesInfo(data.wages_url, 2019)
Data_2018 = data.WagesInfo(data.wages_url, 2018)
Data_2017 = data.WagesInfo(data.wages_url, 2017)
Data_2016 = data.WagesInfo(data.wages_url, 2016)
Data_2015 = data.WagesInfo(data.wages_url, 2015)

post_pandemic_data = [Data_2023, Data_2024]

post_pandemic_dfs = []
for yearly_data in post_pandemic_data:
    yearly_data.get_data()
    yearly_data.find_dataset()
    df = yearly_data.create_dataframe()
    post_pandemic_dfs.append(df)

# Manually remove all french columns in the 2023 dataframe and rename other columns
columns_to_remove_2023 = ['NOC_TITLE_FRA', 'Nom_RE', 'Data_Source_F', 'Wage_Comment_F', 'Wage_Comment_E']
for column in columns_to_remove_2023:
    post_pandemic_dfs[0].drop(column, axis = 1, inplace = True)

new_column_names = ['NOC_CNP', 'NOC_TITLE', 'PROV', 'ER_CODE', 'ER_NAME', 'LOW_WAGE', 'MEDIAN_WAGE', 'HIGH_WAGE', 'AVERAGE_WAGE',
                     'DATA_SOURCE', 'REFERENCE_PERIOD', 'REVISION_DATE', 'ANNUAL_WAGE_FLAG']
post_pandemic_dfs[0].rename(columns = dict(zip(list(post_pandemic_dfs[0].columns), new_column_names)), inplace=True)

# Manually remove all french columns in the 2024 dataframe and rename other columns
columns_to_remove_2024 = ['NOC_Title_fra', 'Nom_RE', 'Data_Source_F', 'Quartile1_Wage_Salaire_Quartile1', 
                          'Quartile3_Wage_Salaire_Quartile3','Wage_Comment_E', 
                          'Wage_Comment_F', 'Non_WageBen_pct']
for column in columns_to_remove_2024:
    post_pandemic_dfs[1].drop(column, axis = 1, inplace=True)

post_pandemic_dfs[1].rename(columns = dict(zip(list(post_pandemic_dfs[1].columns), new_column_names)), inplace=True)

# Remove all rows where annual wage flag has a value of 0
cleaned_2023_df = post_pandemic_dfs[0][post_pandemic_dfs[0]['ANNUAL_WAGE_FLAG']!= 0]
cleaned_2024_df = post_pandemic_dfs[1][post_pandemic_dfs[1]['ANNUAL_WAGE_FLAG']!= 0]

# Remove all rows where all four wage categories are NaN
columns_to_check = ['LOW_WAGE', 'MEDIAN_WAGE', 'HIGH_WAGE', 'AVERAGE_WAGE']
cleaned_2023_df = cleaned_2023_df.dropna(subset=columns_to_check, how = 'all')
cleaned_2024_df = cleaned_2024_df.dropna(subset=columns_to_check, how = 'all')

# visualize data by province
combined_df = pd.concat([cleaned_2023_df, cleaned_2024_df], ignore_index=True)
combined_df.fillna({'AVERAGE_WAGE' : 0}, inplace=True)
combined_df.dropna(subset=['PROV'], inplace=True)

x_values = list(combined_df['PROV'].unique())
y_values_prov = list(combined_df.groupby('PROV')['AVERAGE_WAGE'].mean())
plt.bar(x_values, y_values_prov)
plt.title("Mean of Average Wages Across 2023-2024 by Province")
plt.show()

# visualize wage spread based on NOC_TITLE
titles = list(combined_df['NOC_TITLE'].unique())
y_values_titles = list(combined_df.groupby('NOC_TITLE')['AVERAGE_WAGE'].mean())
plt.bar(titles, y_values_titles)
plt.title("Mean of Average Wages Across 2023-2024 by Job Categories")
plt.xticks(rotation=45)
plt.show()

# compare the change in CPI from 2023-2024
# CPI is essentially the cost of a basket of goods
Detailed_CPI_breakdown = pd.read_csv(r"C:\Users\aycja\Math 1130 Final Project\1810000501-noSymbol.csv", skiprows=10, on_bad_lines="skip", nrows=15)
Detailed_CPI_breakdown_df = pd.DataFrame(Detailed_CPI_breakdown.head(15))
new_column_names_CPI = ['Products and product groups', '2020', '2021', '2022', '2023', '2024']
Detailed_CPI_breakdown_df.rename(columns=dict(zip(list(Detailed_CPI_breakdown_df.columns), new_column_names_CPI)), inplace=True)

wages_quartile_25 = combined_df['AVERAGE_WAGE'].quantile(0.25)
wages_quartile_50 = combined_df['AVERAGE_WAGE'].quantile(0.50)
wages_quartile_75 = combined_df['AVERAGE_WAGE'].quantile(0.75)

quartile1_2023 = cleaned_2023_df[cleaned_2023_df['AVERAGE_WAGE'] <= wages_quartile_25]['AVERAGE_WAGE'].mean()
quartile2_2023 = cleaned_2023_df[(wages_quartile_25 < cleaned_2023_df['AVERAGE_WAGE']) &
                        (cleaned_2023_df['AVERAGE_WAGE'] <= wages_quartile_50)]['AVERAGE_WAGE'].mean()
quartile3_2023 = cleaned_2023_df[(wages_quartile_50 < cleaned_2023_df['AVERAGE_WAGE']) &
                        (cleaned_2023_df['AVERAGE_WAGE'] <= wages_quartile_75)]['AVERAGE_WAGE'].mean()
quartile4_2023 = cleaned_2023_df[cleaned_2023_df['AVERAGE_WAGE'] > wages_quartile_75]['AVERAGE_WAGE'].mean()

quartile1_2024 = cleaned_2024_df[cleaned_2024_df['AVERAGE_WAGE'] <= wages_quartile_25]['AVERAGE_WAGE'].mean()
quartile2_2024 = cleaned_2024_df[(wages_quartile_25 < cleaned_2024_df['AVERAGE_WAGE']) &
                        (cleaned_2024_df['AVERAGE_WAGE'] <= wages_quartile_50)]['AVERAGE_WAGE'].mean()
quartile3_2024 = cleaned_2024_df[(wages_quartile_50 < cleaned_2024_df['AVERAGE_WAGE']) &
                        (cleaned_2024_df['AVERAGE_WAGE'] <= wages_quartile_75)]['AVERAGE_WAGE'].mean()
quartile4_2024 = cleaned_2024_df[cleaned_2024_df['AVERAGE_WAGE'] > wages_quartile_75]['AVERAGE_WAGE'].mean()

quartiles = ['Q1', 'Q2', 'Q3', 'Q4']
values1 = [quartile1_2023, quartile2_2023, quartile3_2023, quartile4_2023]
values2 = [quartile1_2024, quartile2_2024, quartile3_2024, quartile4_2024]
plt.scatter(quartiles, values1, c='green', label='2023 Quartiles')
plt.scatter(quartiles, values2, c='blue', label='2024 Quartiles')
plt.legend()
plt.title("Quality of Life Based on Quartile Income")
plt.show()