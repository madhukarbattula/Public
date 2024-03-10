# This Python code explores Pandas DataReader APIs to download economic data 
# for India and the United States from 2011 to 2020. Specifically, it retrieves 
# merchandise import data and GDP from the World Bank and FRED for both 
# countries. The data is processed into Pandas DataFrames, with the imports 
# values in billion dollars. This forms a foundational step for further 
# analysis, comparing economic indicators between India and the US over the 
# specified period; thereby, we save the output data in a *.csv file and, 
# also, we plot and save the two visualizations as *.png files.

import os
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import pandas_datareader.data as web
from pandas_datareader import wb

import requests

# Get the current working directory
os.getcwd()

# Change the current working directory
cwd = r'C:\Users\madhu\OneDrive\Desktop\STC SPI'
os.chdir(cwd)

# Merchandise Import data of US (World Bank)
indicator1 = 'TM.VAL.MRCH.CD.WT'
country1 = 'US'
df_ctry1_imp_wb = wb.download(indicator=indicator1, country=country1, 
                              start=2011, end=2020).reset_index()

df_ctry1_imp_wb = df_ctry1_imp_wb.rename(columns=
                                         {'country': 'Country', 'year': 'Year', 
                                          'TM.VAL.MRCH.CD.WT':'Imports ($Bn)'})
df_ctry1_imp_wb['Imports ($Bn)'] /= 1e9
df_ctry1_imp_wb['Year'] = df_ctry1_imp_wb['Year'].astype('int64')

# Merchandise Import data of India (World Bank)
indicator2 = 'TM.VAL.MRCH.CD.WT'
country2 = 'IN'
df_ctry2_imp_wb = wb.download(indicator=indicator2, 
                              country=country2, 
                              start=2011, end=2020).reset_index()

df_ctry2_imp_wb = df_ctry2_imp_wb.rename(columns=
                                         {'country': 'Country', 'year': 'Year', 
                                          'TM.VAL.MRCH.CD.WT':'Imports ($Bn)'})
df_ctry2_imp_wb['Imports ($Bn)'] /= 1e9
df_ctry2_imp_wb['Year'] = df_ctry2_imp_wb['Year'].astype('int64')

# US GDP Quarterly data (FRED)
start = datetime.date(year=2011, month=1, day=1)
end = datetime.date(year=2020, month=12, day=31)
series_ctry1 = 'GDP'
source_ctry1 = 'fred'

df_ctry1_gdp_qtr_fred = web.DataReader(series_ctry1, source_ctry1, start, 
                                       end).reset_index()

df_ctry1_gdp_qtr_fred = df_ctry1_gdp_qtr_fred.rename(columns
                                                     ={'DATE': 'Date', 
                                                       'GDP': 'GDP ($Bn)'})
df_ctry1_gdp_qtr_fred.insert(0, 'Country', 'United States')
df_ctry1_gdp_qtr_fred['Date'] = pd.to_datetime(df_ctry1_gdp_qtr_fred['Date'])
df_ctry1_gdp_qtr_fred['Year'] = df_ctry1_gdp_qtr_fred['Date'].dt.year
df_ctry1_gdp_qtr_fred['Quarter'] = df_ctry1_gdp_qtr_fred['Date'].dt.quarter
df_ctry1_gdp_qtr_fred = df_ctry1_gdp_qtr_fred.drop('Date', axis=1)
df_ctry1_gdp_qtr_fred = df_ctry1_gdp_qtr_fred[['Country', 'Year', 'Quarter', 
                                               'GDP ($Bn)']]

df_ctry1_gdp_yr_fred = df_ctry1_gdp_qtr_fred\
    .groupby(['Country', 'Year'], as_index=False)['GDP ($Bn)'].mean()

# India GDP Annual data (FRED)
start = datetime.date(year=2011, month=1, day=1)
end = datetime.date(year=2020, month=12, day=31)
series_ctry2 = 'MKTGDPINA646NWDB'
source_ctry2 = 'fred'

df_ctry2_gdp_yr_fred = web.DataReader(series_ctry2, 
                                      source_ctry2, start, end).reset_index()
df_ctry2_gdp_yr_fred = df_ctry2_gdp_yr_fred.rename(columns={
    'DATE': 'Date', 'MKTGDPINA646NWDB': 'GDP ($Bn)'})
df_ctry2_gdp_yr_fred.insert(0, 'Country', 'India')
df_ctry2_gdp_yr_fred['Date'] = pd.to_datetime(df_ctry2_gdp_yr_fred['Date'])
df_ctry2_gdp_yr_fred['Year'] = df_ctry2_gdp_yr_fred['Date'].dt.year
df_ctry2_gdp_yr_fred['GDP ($Bn)'] = df_ctry2_gdp_yr_fred['GDP ($Bn)'] / 1e9
df_ctry2_gdp_yr_fred['Year'] = df_ctry2_gdp_yr_fred['Year'].astype('int64')
df_ctry2_gdp_yr_fred = df_ctry2_gdp_yr_fred.drop('Date', axis=1)
df_ctry2_gdp_yr_fred = df_ctry2_gdp_yr_fred[['Country', 'Year', 'GDP ($Bn)']]

# Adjust the data so that all four are at the same frequency and then 
# merge them together into one long (tidy) format dataframe.

df_ctry1_merged = pd.merge(df_ctry1_gdp_yr_fred, df_ctry1_imp_wb, 
                           on=['Country', 'Year'])

df_ctry2_merged = pd.merge(df_ctry2_gdp_yr_fred, df_ctry2_imp_wb, 
                           on=['Country', 'Year'])

df_ctry1_ctry2_wide = pd.concat([df_ctry1_merged, df_ctry2_merged], 
                                ignore_index=True)

df_ctry1_ctry2_long = pd.melt(df_ctry1_ctry2_wide, id_vars=
                              ['Country', 'Year'], value_vars=None, 
                              var_name='Indicator', value_name='Value')

# Clean up column names and values so that the data is consistent and clear, 
# so that the dataframe is saved as a file named WBG Data.csv.

df_ctry1_ctry2_long.to_csv('WBG Data.csv', index=False)

print("The file is saved as 'WBG Data.csv' in the current working directory,"
      , cwd)

# Load the WBG Data.csv into a dataframe for plotting visualizations
df_wbg = pd.read_csv('WBG Data.csv')

df_india = df_wbg[df_wbg['Country'] == 'India']
df_us = df_wbg[df_wbg['Country'] == 'United States']

# Plotting GDP data
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 2)
sns.lineplot(x='Year', y='Value', hue='Country', 
             data=df_wbg[df_wbg['Indicator'] == 'GDP ($Bn)'])
plt.title('GDP ($Bn)')

plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
plt.xticks(rotation=45)
plt.legend(loc='upper left')

# Save GDP visualization as PNG
plt.savefig('US_India_GDP_comparison.png', dpi=300, bbox_inches='tight')

plt.tight_layout()
plt.show()

# Plotting imports data
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
sns.barplot(x='Year', y='Value', hue='Country', 
            data=df_wbg[df_wbg['Indicator'] == 'Imports ($Bn)'])
plt.title('Merchandise Imports ($Bn)')
plt.xticks(rotation=45)
plt.legend(loc='upper left')

# Save imports visualization as PNG
plt.savefig('US_India_imports_comparison.png', dpi=300, bbox_inches='tight')

plt.tight_layout()
plt.show()