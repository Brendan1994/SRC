import streamlit as st
import pandas as pd
import requests as rq
from datetime import datetime
#import re
#from lxml import html
import pip
pip.main(["install", "openpyxl"])

#set wide mode
st.set_page_config(layout="wide")

#Page title
st.title("Latton TT Series") 

#Historical data fed into df from an excel spreadsheet
df = pd.read_excel("Results Archive 01-6-23.xlsx")
df = df[['Position','Start Number','Name','Club','Split Time','Time']]

    #Iterate over the DataFrame, where the 'Name' column is date define 'date' variable and append this variable into a new 'Date' column
for index, row in df.iterrows():
    if type(row['Name']) == pd._libs.tslibs.timestamps.Timestamp:
        date = row['Name']
        df.at[index,'type'] = 'date'
    df.at[index,'Date'] = date
    
    #Add new column with the day of the race
df['Day'] = df['Date'].dt.day_name()

    #Remove dates from rows
df = df[df.type != 'date']


    #Filter DataFrame for races that took place on a Thursday or on NYD
df = df.loc[(df['Day']=='Thursday') | (df['Date'].dt.day == 1) & (df['Date'].dt.month == 1)]


#Create list of dataframes - 1 html table per df
df = pd.read_html("http://test2.swindon-rc.co.uk/?page_id=240",header=0)


#Add 'Week' column to each df
f = rq.get("http://test2.swindon-rc.co.uk/?page_id=240")
#f = open('2022_Time_Trial_Results.html','r')

Week = []

#lines = f.text.readlines()
lines = f.text.splitlines()     #ChatGPT suggests using splitlines() rather than readlines()


for line in lines:
#    if re.search('<strong style="color: #666666; font-family: Arial, Helvetica, sans-serif; font-size: 16px;">',line):     --This was for the old website which is no longer being updated
    if re.search('<p class="has-black-color has-text-color has-medium-font-size">',line):
        line = re.sub('<(.*?)\>','',line)
        line = re.sub('&nbsp;',' ',line)
        line = re.sub("New Year's Day ",'1 January ',line)
        #print(line)
        try:
            d = datetime.strptime(line.strip(),'%d %B %Y')
            #print(d)
            Week.append(d.date())
        except:
            continue
Week  
#Append df's into single df
#df1 = pd.DataFrame()

#for idx,a in enumerate(df):
#    df[idx]['Week'] = Week[idx]
#    df1 = pd.concat([df[idx],df1])

#Drop 'Type' and 'Day' columns
df = df[['Position','Start Number','Name','Club','Split Time','Time','Date']]

#Remove index column
df.set_index('Position',inplace=True)

#Convert datetime64[ns] to date
df['Date'] = df['Date'].dt.date
#df['Type'] = df.dtypes['Date']

#Sort Values by Week desc, Position asc
df.sort_values(by=["Date","Time"], ascending=[False, True], inplace=True)

#Unique list of racers names
Names = df.Name.drop_duplicates()
Names.sort_values(ascending=True, inplace=True)

##Unique list of Weeks
Date = df.Date.drop_duplicates()
Date.sort_values(ascending=False, inplace=True)

#Filter text
Racer = st.multiselect("Enter your name to filter the results",list(Names))
Date = st.multiselect("Enter date to filter the results",list(Date))

##Filter df by input
if (Racer and Date):
    rslt_df1 = df[df['Date'].isin(Date)]
    rslt_df = rslt_df1[rslt_df1['Name'].isin(Racer)]
    #st.line_chart(data=df,x=df['Name'], y=df['Date'] )
elif Racer:
    rslt_df = df[df['Name'].isin(Racer)]
elif Date:
    rslt_df = df[df['Date'].isin(Date)]
else:
    rslt_df = df

#Present filtered df
st.dataframe(rslt_df)


