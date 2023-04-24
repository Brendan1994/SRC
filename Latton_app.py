import streamlit as st
import pandas as pd
import requests as rq
from datetime import datetime
import re

st.title("Latton TT Series")

#def Get_Results():
#    Results = rq.get("https://www.swindon-rc.co.uk/index.php/component/content/article/104", verify=False)
#    Normalized_Results = pandas.json_normalize(Results.json())
#    return Normalized_Results

#st.dataframe(Get_Results)  

#Create list of dataframes - 1 html table per df
df = pd.read_html("https://www.swindon-rc.co.uk/index.php/component/content/article/104",header=0)

#Add 'Week' column to each df
#f = rq.get("https://www.swindon-rc.co.uk/index.php/component/content/article/104")
f = open('2022_Time_Trial_Results.html','r')

Week = []
#lines = f.text.readlines()
lines = f.readlines()

for line in lines:
    if re.search('<strong style="color: #666666; font-family: Arial, Helvetica, sans-serif; font-size: 16px;">',line):
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
  
#Append df's into single df
df1 = pd.DataFrame()

for idx,a in enumerate(df):
    df[idx]['Week'] = Week[idx]
    df1 = pd.concat([df[idx],df1])
#df1.reset_index(inplace=True)

# CSS to inject contained in a string
#hide_dataframe_row_index = """
#            <style>
#            .row_heading.level0 {display:none}
#            .blank {display:none}
#            </style>
#            """

# Inject CSS with Markdown
#st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

#Remove index column
df1.set_index('Position',inplace=True)

#Sort Values by Week desc, Position asc
df1.sort_values(by=["Week","Position"], ascending=[False, True], inplace=True)

#BP = ['Brendan Pearson']

#rslt_df = df1.loc[df1['Name'].isin(BP)]

#Unique list of racers names
Names = df1.Name.drop_duplicates()
Names.sort_values(ascending=True, inplace=True)

#Unique list of Weeks
Date = df1.Week.drop_duplicates()
Date.sort_values(ascending=False, inplace=True)

#Present text
Racer = st.multiselect("Enter your name to filter the results",list(Names))
Date = st.multiselect("Enter date to filter the results",list(Date))

#Filter df by input
#if Racer and Date:
#    rslt_df = (df1.loc[df1['Name'].isin(Racer)]) & (df1.loc[df1['Week'].isin(Date)])
if not Racer:
    rslt_df = df1.loc[df1['Name'].isin(Racer)]
elif not Date:
    rslt_df = df1.loc[df1['Week'].isin(Date)]
else:
    rslt_df = df1

#Present filtered df
#if not Racer:
#    if not Date:
#        st.dataframe(df1)
    
#else:
    st.dataframe(rslt_df)

