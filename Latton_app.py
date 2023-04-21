import streamlit as st
import pandas as pd
import requests as rq

st.title("Latton TT Series")

def Get_Results():
    Results = rq.get(https://www.swindon-rc.co.uk/index.php/component/content/article/104)
    Normalized_Results = pandas.json_normalize(Results.json())
    return Normalized_Results

st.dataframe(Get_Results)  
