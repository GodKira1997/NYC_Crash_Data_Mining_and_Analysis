# -*- coding: utf-8 -*-
"""PROJECT_Kallurwar_Panchidi.py
prerequisites: Read readme.md to install the prerequisities for this program
to execute.
description: This program performs exploratory data analysis and mining on
the New Yrok City Crash Dataset. The analysis focuses on 'Bronx' borough for
the 2019 and 2020
language: python3
Author: Anurag Kallurwar, ak6491
Author: Vishal Panchidi, vp8760
# **Importing Libraries**
"""

import sys
import os
import warnings
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap

"""# **Reading Data**"""
print("\n=====================================================================")
print("Reading Data")
if len(sys.argv) < 2:
    print("Missing Argument!")
    print("Usage: PROJECT_Kallurwar_Panchidi.py <filename.csv>")
    sys.exit()
file_name = sys.argv[1].strip()
if not os.path.isfile(os.getcwd() + "\\" + file_name):
    print("Please put " + file_name + " in the execution folder!")
    sys.exit()
# file_name = 'file.csv'
crash_df = pd.read_csv(file_name, low_memory=False)
print(crash_df.head(10))
print(crash_df.columns)

"""# **Data Preparation**

## Filtering Borough = 'BRONX'
"""
print("\n=====================================================================")
print("Data Preparation")
print("\nFiltering Data for Borough = 'BRONX'")
bronx_df = crash_df
bronx_df = bronx_df[bronx_df['BOROUGH'] == 'BRONX']
bronx_data_count = bronx_df.shape[0]
print("Number of data in bronx_df:", bronx_data_count)

"""## Filtering Data for years 2019 and 2020"""
print("\nFiltering Data for years 2019 and 2020")
with pd.option_context('mode.chained_assignment', None):
    bronx_df['CRASH DATE'] = pd.to_datetime(bronx_df['CRASH DATE'], format="%m/%d/%Y")

# Filter data between January 2019 and December 2020
start_date = pd.to_datetime('2019-01-01')
end_date = pd.to_datetime('2020-12-31')
bronx_df = bronx_df[(bronx_df['CRASH DATE'] >= start_date) & (bronx_df['CRASH DATE'] <= end_date)]

bronx_data_count = bronx_df.shape[0]
print("Number of data in bronx_df:", bronx_data_count)

"""## Checking Data Quality"""
print("\nChecking Data Quality")
print("Data Description: ")
print(bronx_df[["LATITUDE","LONGITUDE"]].describe())

def checking_NaN(table):
    for column in table.columns:
        null_values = table[f"{column}"].isnull().sum()
        print(f"{column} - {null_values}")
print("\nMissing Data: ")
checking_NaN(bronx_df)

duplicates = bronx_df[bronx_df.duplicated(subset=["COLLISION_ID"])]
print("Number of Duplicate Collision_ID: " + str(len(duplicates)))

duplicates = bronx_df[bronx_df.duplicated(subset=bronx_df.columns.difference(["COLLISION_ID"]), keep=False)]
print("Number of Duplicate Accident Information: " + str(len(duplicates)))

"""## Seperate Dataframes for seperate months"""
print("\nSeperate Dataframes for seperate months")
# Filter combined summer months (June and July)
bronx_june_july_2019 = bronx_df[((bronx_df['CRASH DATE'].dt.year == 2019) & ((bronx_df['CRASH DATE'].dt.month == 6) | (bronx_df['CRASH DATE'].dt.month == 7)))]
bronx_june_july_2020 = bronx_df[((bronx_df['CRASH DATE'].dt.year == 2020) & ((bronx_df['CRASH DATE'].dt.month == 6) | (bronx_df['CRASH DATE'].dt.month == 7)))]

# Filter individual June and July months
bronx_june_2019 = bronx_df[((bronx_df['CRASH DATE'].dt.year == 2019) & ((bronx_df['CRASH DATE'].dt.month == 6) ))]
bronx_july_2019 = bronx_df[((bronx_df['CRASH DATE'].dt.year == 2019) & ((bronx_df['CRASH DATE'].dt.month == 7) ))]
bronx_june_2020 = bronx_df[((bronx_df['CRASH DATE'].dt.year == 2020) & ((bronx_df['CRASH DATE'].dt.month == 6) ))]
bronx_july_2020 = bronx_df[((bronx_df['CRASH DATE'].dt.year == 2020) & ((bronx_df['CRASH DATE'].dt.month == 7) ))]

"""# **Data Analysis**

## Summer 2019 vs Summer 2020

### Daily accidents in summer of 2019 and summer of 2020
"""
print("\n=====================================================================")
print("Data Analysis")
print("\nSummer 2019 vs Summer 2020")
print("Plotting Daily accidents in summer of 2019 and summer of 2020")
df = bronx_df.copy()

# Set 'CRASH DATE' as the index for easier manipulation
df.set_index('CRASH DATE', inplace=True)

# Resample to get daily accident counts
daily_accidents = df.resample('D').size()

# Summer 2019
start_date_summer_2019 = pd.to_datetime('2019-06-01')
end_date_summer_2019 = pd.to_datetime('2019-07-31')

# Summer 2020
start_date_summer_2020 = pd.to_datetime('2020-06-01')
end_date_summer_2020 = pd.to_datetime('2020-07-31')

plt.figure(figsize=(12, 6))
sns.lineplot(x=daily_accidents.index, y=daily_accidents.values, label='Daily Accidents')

plt.axvspan(start_date_summer_2019, end_date_summer_2019, color='green', alpha=0.3, label='Summer 2019')
plt.axvspan(start_date_summer_2020, end_date_summer_2020, color='red', alpha=0.3, label='Summer 2020')

plt.xlabel('Date')
plt.ylabel('Number of Accidents')
plt.title('Summer 2019 vs Summer 2020')
plt.legend()
plt.show()

"""### Heat Map of summer of 2019 in the area"""
print("Heat Map of summer of 2019 in the area saved as HTML")
# Create a copy of the DataFrames to avoid modifying the original
df_2019_copy = bronx_june_july_2019.copy()

# Dropna to remove rows with missing latitude or longitude
df_2019_copy = df_2019_copy.dropna(subset=['LATITUDE', 'LONGITUDE'])

center_lat, center_lon = df_2019_copy['LATITUDE'].mean(), df_2019_copy['LONGITUDE'].mean()
heatmap_2019 = folium.Map(location=[center_lat, center_lon], tiles='OpenStreetMap', zoom_start=13)
accidents_2019 = [[row['LATITUDE'], row['LONGITUDE']] for index, row in df_2019_copy.iterrows()]

# Add the HeatMap layer to the map
HeatMap(accidents_2019, min_opacity=0.1, blur=15).add_to(heatmap_2019)

heatmap_2019
heatmap_2019.save("summer_2019.html")

"""### Heat Map of summer of 2020 in the area"""
print("Heat Map of summer of 2020 in the area saved as HTML")
# Create a copy of the DataFrames to avoid modifying the original
df_2020_copy = bronx_june_july_2020.copy()

# Dropna to remove rows with missing latitude or longitude
df_2020_copy = df_2020_copy.dropna(subset=['LATITUDE', 'LONGITUDE'])

center_lat, center_lon = df_2020_copy['LATITUDE'].mean(), df_2020_copy['LONGITUDE'].mean()
heatmap_2020 = folium.Map(location=[center_lat, center_lon], tiles='OpenStreetMap', zoom_start=13)
accidents_2020 = [[row['LATITUDE'], row['LONGITUDE']] for index, row in df_2020_copy.iterrows()]

# Add the HeatMap layer to the map
HeatMap(accidents_2020, min_opacity=0.1, blur=15).add_to(heatmap_2020)

heatmap_2020
heatmap_2020.save("summer_2020.html")

"""### Fatal accidents in summer of 2019 and summer of 2020"""
print("Plotting Fatal accidents in summer of 2019 and summer of 2020")
# Calculating
count_accident_killed_2019 = bronx_june_july_2019[bronx_june_july_2019['NUMBER OF PERSONS KILLED'] > 0].shape[0]
count_accident_injured_2019 =  bronx_june_july_2019[(bronx_june_july_2019['NUMBER OF PERSONS INJURED'] > 0) & (bronx_june_july_2019['NUMBER OF PERSONS KILLED'] == 0)].shape[0]
count_accident_no_injury_2019 = len(bronx_june_july_2019) - count_accident_killed_2019 - count_accident_injured_2019

count_accident_killed_2020 = bronx_june_july_2020[bronx_june_july_2020['NUMBER OF PERSONS KILLED'] > 0].shape[0]
count_accident_injured_2020 =  bronx_june_july_2020[(bronx_june_july_2020['NUMBER OF PERSONS INJURED'] > 0) & (bronx_june_july_2020['NUMBER OF PERSONS KILLED'] == 0)].shape[0]
count_accident_no_injury_2020 = len(bronx_june_july_2020) - count_accident_killed_2020 - count_accident_injured_2020

labels = ['Fatal Accidents', 'Fatal Accidents (Just Injured)', 'Non-Fatal Accidents']
sizes_2019 = [count_accident_killed_2019, count_accident_injured_2019, count_accident_no_injury_2019]
sizes_2020 = [count_accident_killed_2020, count_accident_injured_2020, count_accident_no_injury_2020]

# Set up subplots
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

axes[0].pie(sizes_2019, labels=labels, autopct='%1.1f%%', colors = ['#940b13','#ec382b','#fc9576'], startangle=90)
axes[0].set_title('Summer 2019 - Total Accidents: {}'.format(len(bronx_june_july_2019)))

axes[1].pie(sizes_2020, labels=labels, autopct='%1.1f%%', colors = ['#940b13','#ec382b','#fc9576'], startangle=90)
axes[1].set_title('Summer 2020 - Total Accidents: {}'.format(len(bronx_june_july_2020)))

plt.suptitle("Fatal Accidents")
plt.tight_layout()
plt.show()

"""### People involved in accidents in summer of 2019 and summer of 2020"""
print("Plotting People involved in accidents in summer of 2019 and summer of 2020")
columns_persons_involved = ['NUMBER OF PEDESTRIANS KILLED', 'NUMBER OF CYCLIST KILLED', 'NUMBER OF MOTORIST KILLED']
columns_persons_involved2 = ['NUMBER OF PEDESTRIANS INJURED', 'NUMBER OF CYCLIST INJURED', 'NUMBER OF MOTORIST INJURED']

# Calculate the total killed for each summer
total_killed_summer_2019 = bronx_june_july_2019[columns_persons_involved].sum().to_frame().T
total_killed_summer_2019['Summer'] = '2019'
total_killed_summer_2020 = bronx_june_july_2020[columns_persons_involved].sum().to_frame().T
total_killed_summer_2020['Summer'] = '2020'
combined_killed = pd.concat([total_killed_summer_2019, total_killed_summer_2020], ignore_index=True)

# Calculate the total injured for each summer
total_injured_summer_2019 = bronx_june_july_2019[columns_persons_involved2].sum().to_frame().T
total_injured_summer_2019['Summer'] = '2019'
total_injured_summer_2020 = bronx_june_july_2020[columns_persons_involved2].sum().to_frame().T
total_injured_summer_2020['Summer'] = '2020'
combined_injured = pd.concat([total_injured_summer_2019, total_injured_summer_2020], ignore_index=True)

# Set up subplots
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Plot stacked bars
sns.barplot(data=combined_killed, x='Summer', y='NUMBER OF PEDESTRIANS KILLED', color='#fc9576', label='Pedestrians', ax=axes[0])
sns.barplot(data=combined_killed, x='Summer', y='NUMBER OF CYCLIST KILLED', color='#ec382b', bottom=combined_killed[['NUMBER OF PEDESTRIANS KILLED']].sum(axis=1), label='Cyclists', ax=axes[0])
sns.barplot(data=combined_killed, x='Summer', y='NUMBER OF MOTORIST KILLED', color='#940b13', bottom=combined_killed[['NUMBER OF PEDESTRIANS KILLED', 'NUMBER OF CYCLIST KILLED']].sum(axis=1), label='Motorists', ax=axes[0])
axes[0].set_title('Total Fatalities in Summer')
axes[0].set_xlabel('Year')
axes[0].set_ylabel('Total Fatalities')
axes[0].legend(title='Fatalities Category')

sns.barplot(data=combined_injured, x='Summer', y='NUMBER OF PEDESTRIANS INJURED', color='#fc9576', label='Pedestrians', ax=axes[1])
sns.barplot(data=combined_injured, x='Summer', y='NUMBER OF CYCLIST INJURED', color='#ec382b', bottom=combined_injured[['NUMBER OF PEDESTRIANS INJURED']].sum(axis=1), label='Cyclists', ax=axes[1])
sns.barplot(data=combined_injured, x='Summer', y='NUMBER OF MOTORIST INJURED', color='#940b13', bottom=combined_injured[['NUMBER OF PEDESTRIANS INJURED', 'NUMBER OF CYCLIST INJURED']].sum(axis=1), label='Motorists', ax=axes[1])
axes[1].set_title('Total Injured in Summer')
axes[1].set_xlabel('Year')
axes[1].set_ylabel('Total Injured')
axes[1].legend(title='Fatalities Category')

plt.suptitle('Persons Involved in Summer 2019 vs. Summer 2020')
plt.legend(title='Innjured Category')
plt.show()

"""### Contributing Factors to accidents in summer of 2019"""
print("Plotting Contributing Factors to accidents in summer of 2019")
# Create a copy of the DataFrame to avoid modifying the original
df_2019_copy = bronx_june_july_2019.copy()

# Group by contributing factors and count the number of accidents
mask = df_2019_copy['CONTRIBUTING FACTOR VEHICLE 1'] == 'Unspecified'
df_2019_copy = df_2019_copy[~mask]
contributing_factors_2019 = df_2019_copy['CONTRIBUTING FACTOR VEHICLE 1'].value_counts().reset_index(name='Accident Count')
# print(contributing_factors_2019)

# Plotting
plt.figure(figsize=(14, 6))
sns.barplot(x='CONTRIBUTING FACTOR VEHICLE 1', y='Accident Count',
            data=contributing_factors_2019, hue='CONTRIBUTING FACTOR VEHICLE 1', palette='muted')
plt.title('Top Contributing Factors to Traffic Accidents in the Bronx (Summer 2019)')
plt.xlabel('Contributing Factor')
plt.ylabel('Number of Accidents')
plt.xticks(rotation=45, ha='right')
plt.show()

"""### Contributing Factors to accidents in summer of 2020"""
print("Plotting Contributing Factors to accidents in summer of 2020")
# Create a copy of the DataFrame to avoid modifying the original
df_2020_copy = bronx_june_july_2020.copy()

# Group by contributing factors and count the number of accidents
mask = df_2020_copy['CONTRIBUTING FACTOR VEHICLE 1'] == 'Unspecified'
df_2020_copy = df_2020_copy[~mask]
contributing_factors_2020 = df_2020_copy['CONTRIBUTING FACTOR VEHICLE 1'].value_counts().reset_index(name='Accident Count')

# Plotting
plt.figure(figsize=(14, 6))
sns.barplot(x='CONTRIBUTING FACTOR VEHICLE 1', y='Accident Count',
            data=contributing_factors_2020, hue='CONTRIBUTING FACTOR VEHICLE 1', palette='muted')
plt.title('Top Contributing Factors to Traffic Accidents in the Bronx (Summer 2020)')
plt.xlabel('Contributing Factor')
plt.ylabel('Number of Accidents')
plt.xticks(rotation=45, ha='right')
plt.show() #Remove unspecified, there is no point

"""## June 2019 vs June 2020

### Accidents in June 2019 and June 2020
"""
print("\nJune 2019 vs June 2020")
print("Plotting Accidents in June 2019 and June 2020")
total_accidents_june_2019 = len(bronx_june_2019.copy())
total_accidents_june_2020 = len(bronx_june_2020.copy())

# Plotting
plt.figure(figsize=(6, 6))
sns.barplot(x=["June 2019", "June 2020"], y=[total_accidents_june_2019, total_accidents_june_2020], hue=["June 2019", "June 2020"], palette='Blues')
plt.title('Accidents in June 2019 and June 2020')
plt.xlabel('Month', )
plt.ylabel('Number of Accidents')
plt.show() #Remove unspecified, there is no point

"""### Heat Map for accidents in June 2019"""
print("Heat Map for accidents in June 2019 saved as HTML")
df_2019_copy = bronx_june_2019.copy()

# Dropna to remove rows with missing latitude or longitude
df_2019_copy = df_2019_copy.dropna(subset=['LATITUDE', 'LONGITUDE'])

center_lat, center_lon = df_2019_copy['LATITUDE'].mean(), df_2019_copy['LONGITUDE'].mean()
heatmap_2019 = folium.Map(location=[center_lat, center_lon], tiles='OpenStreetMap', zoom_start=13)
accidents_2019 = [[row['LATITUDE'], row['LONGITUDE']] for index, row in df_2019_copy.iterrows()]

# Add the HeatMap layer to the map
HeatMap(accidents_2019, min_opacity=0.1, blur=15).add_to(heatmap_2019)
heatmap_2019
heatmap_2019.save("june_2019.html")

"""### Heat Map for accidents in June 2020"""
print("Heat Map for accidents in June 2020 saved as HTML")
df_2020_copy = bronx_june_2020.copy()

# Dropna to remove rows with missing latitude or longitude
df_2020_copy = df_2020_copy.dropna(subset=['LATITUDE', 'LONGITUDE'])

center_lat, center_lon = df_2020_copy['LATITUDE'].mean(), df_2020_copy['LONGITUDE'].mean()
heatmap_2020 = folium.Map(location=[center_lat, center_lon], tiles='OpenStreetMap', zoom_start=13)
accidents_2020 = [[row['LATITUDE'], row['LONGITUDE']] for index, row in df_2020_copy.iterrows()]

# Add the HeatMap layer to the map
HeatMap(accidents_2020, min_opacity=0.1, blur=15).add_to(heatmap_2020)
heatmap_2020
heatmap_2020.save("june_2020.html")


"""## July 2019 vs July 2020

### Accidents in July 2019 and July 2020
"""
print("\nJuly 2019 vs July 2020")
print("Plotting Accidents in July 2019 and July 2020")
total_accidents_july_2019 = len(bronx_july_2019.copy())
total_accidents_july_2020 = len(bronx_july_2020.copy())

# Plotting
plt.figure(figsize=(6, 6))
sns.barplot(x=["July 2019", "July 2020"], y=[total_accidents_july_2019, total_accidents_july_2020], hue=["July 2019", "July 2020"], palette='Blues')
plt.title('Accidents in July 2019 and July 2020')
plt.xlabel('Month', )
plt.ylabel('Number of Accidents')
plt.show() #Remove unspecified, there is no point

"""### Heat Map for accidents in July 2019"""
print("Heat Map for accidents in July 2019 saved as HTML")
df_2019_copy = bronx_july_2019.copy()

# Dropna to remove rows with missing latitude or longitude
df_2019_copy = df_2019_copy.dropna(subset=['LATITUDE', 'LONGITUDE'])

center_lat, center_lon = df_2019_copy['LATITUDE'].mean(), df_2019_copy['LONGITUDE'].mean()
heatmap_2019 = folium.Map(location=[center_lat, center_lon], tiles='OpenStreetMap', zoom_start=13)
accidents_2019 = [[row['LATITUDE'], row['LONGITUDE']] for index, row in df_2019_copy.iterrows()]

# Add the HeatMap layer to the map
HeatMap(accidents_2019, min_opacity=0.1, blur=15).add_to(heatmap_2019)
heatmap_2019
heatmap_2019.save("july_2019.html")

"""### Heat Map for accidents in July 2020"""
print("Heat Map for accidents in July 2020 saved as HTML")
df_2020_copy = bronx_july_2020.copy()

# Dropna to remove rows with missing latitude or longitude
df_2020_copy = df_2020_copy.dropna(subset=['LATITUDE', 'LONGITUDE'])

center_lat, center_lon = df_2020_copy['LATITUDE'].mean(), df_2020_copy['LONGITUDE'].mean()
heatmap_2020 = folium.Map(location=[center_lat, center_lon], tiles='OpenStreetMap', zoom_start=13)
accidents_2020 = [[row['LATITUDE'], row['LONGITUDE']] for index, row in df_2020_copy.iterrows()]

# Add the HeatMap layer to the map
HeatMap(accidents_2020, min_opacity=0.1, blur=15).add_to(heatmap_2020)
heatmap_2020
heatmap_2020.save("july_2020.html")


"""## 100 consecutive days had the most accidents (For the year of January 2019 to October of 2020)"""
print("\nPlotting 100 consecutive days had the most accidents (For the year of "
      "January 2019 to October of 2020)")
df =  bronx_df.copy()

# Filter data between January 2019 and October 2020
start_date = pd.to_datetime('2019-01-01')
end_date = pd.to_datetime('2020-10-31')
df = df[(df['CRASH DATE'] >= start_date) & (df['CRASH DATE'] <= end_date)]

# Set 'CRASH DATE' as the index for easier manipulation
df.set_index('CRASH DATE', inplace=True)

# Resample to get daily accident counts
daily_accidents = df.resample('D').size()

# Find the 100 consecutive days with the most accidents
top_100_days = daily_accidents.rolling(window=100).sum().idxmax()
start_date = top_100_days - pd.DateOffset(days=100)
end_date = top_100_days

print("The 100 consecutive days with most accidents")
print(f"Start Date: {start_date.strftime('%Y-%m-%d')}")
print(f"End Date: {end_date.strftime('%Y-%m-%d')}")
# Plot the line graph
plt.figure(figsize=(12, 6))
sns.lineplot(x=daily_accidents.index, y=daily_accidents.values, label='Daily Accidents')

# Highlight the portion corresponding to the top 100 consecutive days
plt.axvspan(start_date, end_date, color='red', alpha=0.3, label='Top 100 Days')

# Set plot labels and title
plt.xlabel('Date')
plt.ylabel('Number of Accidents')
plt.title('Daily Number of Accidents (Jan 2019 - Oct 2020) with Top 100 Consecutive Days Highlighted')
plt.legend()
plt.show()

"""## Accidents every day of the week"""
print("\nPlotting Accidents every day of the week")
df = bronx_df.copy()

# Extract the day of the week
df['Day of Week'] = df['CRASH DATE'].dt.day_name()

# Count the number of accidents for each day of the week
accidents_by_day = df['Day of Week'].value_counts()

# Plot the bar graph
plt.figure(figsize=(10, 6))
sns.barplot(x=accidents_by_day.index, y=accidents_by_day.values, order=[
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
    'Sunday'], hue=accidents_by_day.index, palette="viridis")

# Set plot labels and title
plt.xlabel('Day of the Week')
plt.ylabel('Number of Accidents')
plt.title('Number of Accidents by Day of the Week in the Bronx')
plt.show()

# Print the day with the most accidents
most_accidents_day = accidents_by_day.idxmax()
print(f"The day with the most accidents is {most_accidents_day} with {accidents_by_day[most_accidents_day]} accidents.")

"""## Accidents every hour of day"""
print("\nPlotting Accidents every hour of day")
df = bronx_df.copy()

# Convert 'CRASH DATE' to datetime
df['CRASH TIME'] = pd.to_datetime(df['CRASH TIME'], format="%H:%M")

# Extract the hour of the day
df['Hour of Day'] = df['CRASH TIME'].dt.hour

# Count the number of accidents for each hour of the day
accidents_by_hour = df['Hour of Day'].value_counts().sort_index()

# Plot the bar graph
plt.figure(figsize=(12, 6))
sns.barplot(x=accidents_by_hour.index, y=accidents_by_hour.values, hue=accidents_by_hour.index, palette="viridis")

# Set plot labels and title
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Accidents')
plt.title('Number of Accidents by Hour of the Day')
plt.show()

# Print the hour with the most accidents
most_accidents_hour = accidents_by_hour.idxmax()
print(f"The hour with the most accidents is {most_accidents_hour}:00 with {accidents_by_hour[most_accidents_hour]} accidents.")

"""## 12 days in 2020 with the most accidents"""
print("\nPlotting 12 days in 2020 with the most accidents")
df = bronx_df.copy()

# Filter data for year 2020
start_date = pd.to_datetime('2020-01-01')
end_date = pd.to_datetime('2020-12-31')
df = df[(bronx_df['CRASH DATE'] >= start_date) & (df['CRASH DATE'] <= end_date)]

# Set 'CRASH DATE' as the index for easier manipulation
df.set_index('CRASH DATE', inplace=True)

# Resample to get daily accident counts
daily_accidents = df.resample('D').size()

# Find the 12 consecutive days with the most accidents
top_12_days = daily_accidents.nlargest(12)

print("The top 12 days with most accidents")
print(top_12_days)

# Plot
plt.figure(figsize=(12, 6))
default_palette = sns.color_palette("viridis", as_cmap=True)
sns.barplot(x=top_12_days.index, y=top_12_days.values, label='Accidents',
            hue=top_12_days.index, palette="viridis")
plt.xlabel('Date')
plt.ylabel('Number of Accidents')
plt.xticks(rotation=45, ha='right')
plt.title('In 2020, top 12 days with the most accidents')
plt.show()