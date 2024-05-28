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
from datetime import datetime, timedelta
import streamlit as st
import matplotlib.pyplot as plt


API_KEY = "273a432a-4c0f-4cad-b1cb-304a90bdc6a1"
API_URL_HEAD = "https://data.moenv.gov.tw/api/v2/aqx_p_488?language=en&offset=0&limit=1000&api_key="
DATETIME_FORMAT = "%Y-%m-%d %H:%M"
LIST_SENSORS = ['pm2.5', 'so2', 'o3', 'co', 'pm10', 'no2', 'no']

def call_api():
    '''To check the connection of API.'''
    response = requests.get(API_URL_HEAD + API_KEY)
    if response.status_code == 200:
        aqi_all = response.json()
        records = aqi_all.get("records", [])
        return records
    else:
        st.error("Failed to fetch data from the API.")
        return []
    

def available_range(records):
    '''To check the available time range, so the dropdown selectbox has options.'''
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
    selected_time = st.selectbox("Start datetime:", time_list[:-1])
    return selected_time


def end_date_time(start_str, time_list):
    '''Ask user to set the end datetime in the new range and check the validity. 
    The end time should be at least one hour after start time.'''
    update_time_list = []
    for time in time_list:
        if datetime.strptime(time, DATETIME_FORMAT) > datetime.strptime(start_str, 
                                                                        DATETIME_FORMAT):
            update_time_list.append(time)
    selected_time = st.selectbox(f"End datetime:", update_time_list)
    return selected_time


def combine_lists(selected_lst):
    '''create empty pandas data frames for loading data.
    The columns has basic columns needed, plus user's selection of sensors'''
    basic_cols = ['siteid', 'sitename', 'datacreationdate', 'aqi', 'status']
    basic_cols.extend(selected_lst) # list aliasing trap. basic_cols now has changed
    return basic_cols


def load_data(cols_list, start_str, end_str):
    '''First to notify users that the data is loading, then make API get request.
    Filter attributes and load data to the empty data frame.
    (For) Loop through the data, extract specific columns, and append them to the DataFrame.
    Append the filtered dictionary to the list of rows. '''
    data_load_state = st.text(f"Loading data from {start_str} to {end_str}...")
    start_datetime = datetime.strptime(start_str, DATETIME_FORMAT)
    # Minus one hour to the start_datetime, otherwise it won't include the start time
    new_start_datetime = str(start_datetime - timedelta(hours = 1))
    limit_data = requests.get(API_URL_HEAD + API_KEY
                            + '&filters=datacreationdate,GR,' + new_start_datetime
                            + '|datacreationdate,LE,' + end_str + ':00').json()
    records_list = limit_data["records"] # records_list is a list of dictionaries
    rows = [] # Initialize an empty list to store DataFrame rows
    for record_dict in records_list: # record_dict is the individual dictionary in the records_list
        filtered_dict = {key: record_dict[key] for key in cols_list} # dictionary comprehension
        rows.append(filtered_dict)
    df_records = pd.DataFrame(rows)
    return df_records, data_load_state
    

def download_file(df_records, start_str, end_str, data_load_state):
    '''The function will be actived after use click Download button. 
    First, change the format of time so the filename can be shorter. 
    Secondly, save as a csv file with start and end DateTime. 
    New reminder will replace the original loading message.
    '''
    start_str, end_str = start_str.strip(':00'), end_str.strip(':00')
    csv = df_records.to_csv(index = False)
    st.download_button(
        label = "Download CSV",
        data = csv,
        file_name = f'{start_str}_to_{end_str}_aqi_data.csv'
        )
    if st.download_button:
        data_load_state.text("Please click button below to download the file!")


def preview_chart(df_records, selected_lst):
    '''To preview the plotting function provided and hint users that there are other
     programs available to use.'''
    st.markdown(
        """
        **Now run Program 2 or 3 offline with the python file I uploaded to LEARN or download 
        from https://github.com/ShazzaHong/Sandbox-lib
        """
    )
    st.write(f'Preview chart - {selected_lst} level at site 1 (Keelung):')
    condition = df_records['siteid'] == '1'
    filtered_df = df_records[condition] # Apply the filter to the DataFrame
    st.scatter_chart(filtered_df, x = 'datacreationdate', y = selected_lst)

    #st.line_chart(filtered_df, x = 'datacreationdate', y = selected_lst[0], color=None, width=None, height=None, use_container_width=True)
    
    #chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    #st.line_chart(chart_data)   
def main():
    '''
    This main function shows the page setting on Streamlit first, then call api, check 
    available time range, let user select the range (step 1) and sensors/pollutants (step 2).
    Lastly, load the data to an empty pandas DataFrame and save as a CSV file for user to 
    download. 
    '''
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
        
        ### Program 1 - Download data"""
    )
    
    records = call_api()
    st.subheader('Step 1. Select Time')
    time_list = available_range(records)
    col1, col2 = st.columns(2)  # Create two columns
    with col1:
        start_str = start_date_time(time_list)
    if start_str:
        with col2:
            end_str = end_date_time(start_str, time_list)
    st.subheader('Step 2. Select Sensor(s)/Pollutant(s)') 
    selected_lst = st.multiselect("Please select at least one.", 
                                  LIST_SENSORS, [LIST_SENSORS[0]]) 
    if len(selected_lst) >= 1 and st.button("Load"):
        cols_list = combine_lists(selected_lst)
        df_records, data_load_state = load_data(cols_list, start_str, end_str)
        #preview_df(df_records)
        download_file(df_records, start_str, end_str, data_load_state)
        preview_chart(df_records, selected_lst)
    elif len(selected_lst) < 1:
        st.warning('Download button will only be shown when there are more than one '
                   'sensor/pollutant selected.', icon="⚠️")
    

if __name__ == "__main__":
    main()