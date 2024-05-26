"""This is for the COSC480-24S1 project
   Project Name: Data Download Centre
   Date: 2024-05-26
   Developer: Shuan Hong
   Program 1: Download Data (through API)
   
   API parameters details: https://data.moenv.gov.tw/en/paradigm
   AQI API URL format: https://data.moenv.gov.tw/api/v2/aqx_p_488?language=en&
                       offset={offset}&limit={limit}&api_key={api-key}
   Considering system performance, the upper limit of data extraction is set to
   be 1,000 items, so I put limit=1000 in URL
"""

# Install and use method:
# 001 In your terminal or command prompt, enter: python3 -m pip install streamlit
# 002 Then: streamlit run Program 1 - Download Data (Streamlit).py （mind the path!）
# 003 Browse Local URL: http://localhost:8501
# 004 Follow the instruction on the webpage: Filter time, select pollutant(s), 
#     and download file by clicking Download button.

import requests
import pandas as pd
from datetime import datetime 
import streamlit as st

API_KEY = "273a432a-4c0f-4cad-b1cb-304a90bdc6a1"
API_URL_HEAD = "https://data.moenv.gov.tw/api/v2/aqx_p_488?language=en&offset=0&limit=1000&api_key="


def call_api():
    '''To check the connection of API'''
    response = requests.get(API_URL_HEAD + API_KEY)
    if response.status_code == 200:
        aqi_all = response.json()
        records = aqi_all.get("records", [])
        return records
    else:
        st.error("Failed to fetch data from the API.")
        return []
    

def available_range(records):
    '''To check the available time range'''
    dates_dict = {}
    for record in records:
        created_date = record['datacreationdate']
        dates_dict[created_date] = created_date
    last_date, min_time = list(dates_dict.items())[-1]
    first_date, max_time = next(iter(dates_dict.items()))
    time_list = []
    for time in dates_dict.values():
        if time not in time_list:
            time_list.append(time)  
    st.write(f"Set time range between {min_time} and {max_time} to download AQI "
          "data.")
    time_list.reverse()
    return time_list


def start_date_time(time_list):
    '''Ask user to set the start datetime within the available range.'''
    # Create the dropdown list
    selected_time = st.selectbox("Select start datetime", time_list[:-1])
    return selected_time


def end_date_time(start_str, time_list):
    '''Ask user to set the end day and time in the new range and check the 
    validity. The end date should be at least one hour after start time'''
    update_time_list = []
    for time in time_list:
        if datetime.strptime(time, "%Y-%m-%d %H:%M")> datetime.strptime(start_str, 
                                                                        "%Y-%m-%d %H:%M"):
            update_time_list.append(time)
    selected_time = st.selectbox(f"Select end datetime", update_time_list)
    return selected_time


def combine_lists(selected_lst):
    '''create empty pandas data frames for loading data.
    The columns has basic columns needed, plus user's selection of sensors'''
    basic_cols = ['siteid', 'sitename', 'datacreationdate', 'aqi', 'status']
    basic_cols.extend(selected_lst) # list aliasing trap. basic_cols now has changed
    return basic_cols


def load_data(cols_list, start_str, end_str):
    '''Filter attributes and load data to the empty data frame.'''
    st.write(f"Loading data from {start_str} to {end_str}...")
    # make API call to the Air quality index (AQI)(historical data)
    limit_data = requests.get(API_URL_HEAD + API_KEY
                            + '&filters=datacreationdate,GR,' + start_str + ':00'
                            + '|datacreationdate,LE,' + end_str + ':00').json()
    records_list = limit_data["records"] # records_list is a list of dictionaries
    # Initialize an empty list to store DataFrame rows
    rows = []
    # Loop through the data, extract specific columns, and append them to the DataFrame
    for record_dict in records_list: # record_dict is the individual dictionary in the records_list
        filtered_dict = {key: record_dict[key] for key in cols_list} # dictionary comprehension
        # Append the filtered dictionary to the list of rows
        rows.append(filtered_dict)
    df_records = pd.DataFrame(rows)
    return df_records
    

def download_file(df_records, start_str, end_str):
    '''The function will be actived after use click Download button'''
    # Change the format of time so the filename can be shorter
    start_str, end_str = start_str.strip(':00'), end_str.strip(':00')
    # save as a csv file with start and end DateTime
    csv = df_records.to_csv(index=False)
    st.download_button(
        label = "Download CSV",
        data = csv,
        file_name = f'{start_str}_to_{end_str}_aqi_data.csv'
        )


def main():
    st.set_page_config(
        page_title="Data Download Centre☁",
        page_icon="☁",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    st.write("# Data Download Centre ☁")
    st.markdown(
        """
        Here you can download the up-to-date air quality data from 
        Ministry for the Environment, ROC (Taiwan).
        
        **👈 Select other functions from the sidebar** (Please ignore the demo pages)
        ### Program 1 - Download data"""
    )
    
    records = call_api()
    st.subheader('Step 1. Select Time')
    time_list = available_range(records)
    start_str = start_date_time(time_list)
    if start_str:
        end_str = end_date_time(start_str, time_list)
    lst_sensorid = ['pm2.5', 'so2', 'o3', 'co', 'pm10', 'no2', 'no']
    st.subheader('Step 2. Select Sensor(s)/Pollutant') 
    selected_lst = st.multiselect("Please select at least one. For tutor, please select more than 3.",
                             lst_sensorid, [lst_sensorid[0]]) 
    if len(selected_lst) >= 1 and st.button("Download"):
        cols_list = combine_lists(selected_lst)
        df_records = load_data(cols_list, start_str, end_str)
        download_file(df_records, start_str, end_str)
    elif len(selected_lst) < 1:
        st.warning('Download button will only be shown when there are more than one sensor/pollutant selected.', icon="⚠️")

if __name__ == "__main__":
    main()