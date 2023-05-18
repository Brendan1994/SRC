import streamlit as st
import pandas as pd
#import requests as rq
from datetime import datetime
#import re
#from lxml import html
import pip
pip.main(["install", "openpyxl"])

#set wide mode
st.set_page_config(layout="wide")

#Page title
st.title("Latton TT Series") 

#Create list of dataframes - 1 html table per df
#df = pd.read_html("https://www.swindon-rc.co.uk/index.php/component/content/article/104",header=0)
    #We are now creating a df using an excel spreadsheet
df = pd.read_excel("Results Archive 11-5-23.xlsx")
df = df[['Position','Start Number','Name','Club','Split Time','Time']]

#Add 'Week' column to each df
#f = rq.get("https://www.swindon-rc.co.uk/index.php/component/content/article/104")
#f = open('2022_Time_Trial_Results.html','r')
    #Iterate over the DataFrame, where the 'Name' column is date define 'date' variable and append this variable into a new 'Date' column
for index, row in df.iterrows():
    if type(row['Name']) == pd._libs.tslibs.timestamps.Timestamp:
        date = row['Name']
        df.at[index,'type'] = 'date'
    df.at[index,'Date'] = date

    #Add new column with the day of the race
#df['Day'] = df['Date'].dt.day_name()

    #Remove dates from rows
df = df[df.type != 'date']
st.dataframe(df)
#df['Date'] = pd.to_datetime(df['Date'])
#df['Time'] = pd.to_datetime(df['Time'])

    #Filter DataFrame for races that took place on a Thursday or on NYD
#df = df.loc[(df['Day']=='Thursday') | (df['Date'].dt.day == 1) & (df['Date'].dt.month == 1)]

#Week = []

#lines = f.text.readlines()


#for line in lines:
#    if re.search('<strong style="color: #666666; font-family: Arial, Helvetica, sans-serif; font-size: 16px;">',line):
#        line = re.sub('<(.*?)\>','',line)
#        line = re.sub('&nbsp;',' ',line)
#        line = re.sub("New Year's Day ",'1 January ',line)
        #print(line)
#        try:
#            d = datetime.strptime(line.strip(),'%d %B %Y')
            #print(d)
#            Week.append(d.date())
#        except:
#            continue
  
#Append df's into single df
#df1 = pd.DataFrame()

#for idx,a in enumerate(df):
#    df[idx]['Week'] = Week[idx]
#    df1 = pd.concat([df[idx],df1])

##Remove index column
#df.set_index('Position',inplace=True)

##Sort Values by Week desc, Position asc
#df.sort_values(by=["Date","Time"], ascending=[False, True], inplace=True)

##Unique list of racers names
#Names = df.Name.drop_duplicates()
#Names.sort_values(ascending=True, inplace=True)

##Unique list of Weeks
#Date = df.Date.drop_duplicates()
#Date.sort_values(ascending=False, inplace=True)

##Present text
#Racer = st.multiselect("Enter your name to filter the results",list(Names))
#Date = st.multiselect("Enter date to filter the results",list(Date))

##Filter df by input
#if (Racer and Date):
#    rslt_df1 = df[df['Date'].isin(Date)]
#    rslt_df = rslt_df1[rslt_df1['Name'].isin(Racer)]
#elif Racer:
#    rslt_df = df[df['Name'].isin(Racer)]
#elif Date:
#    rslt_df = df[df['Date'].isin(Date)]
#else:
#    rslt_df = df

#Present filtered df
#st.dataframe(rslt_df)
