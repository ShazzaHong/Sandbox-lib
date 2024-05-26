"""This is for the COSC480-24S1 project
   Project Name: Data Download Centre 
   Date: 2024-05-26
   Developer: Shuan Hong
   Program 2: Merge Files
   Purpose: This program is mainly to (outer join) merge multiple csv files with basic columns 
   ('siteid', 'sitename', 'datacreationdate', 'aqi', 'status'). The merged file allows user to 
   plot longer time series (charts).
"""

import pandas as pd
import streamlit as st


BASIC_COL_SET = set(['siteid', 'sitename', 'datacreationdate', 'aqi', 'status'])


def upload():
    '''To let users upload the files they want to merge'''
    uploaded_files = st.file_uploader("Choose CSV file(s) you want to merge", 
                                      type = 'csv', accept_multiple_files = True)
    return uploaded_files


def has_basic_cols(uploaded_files):
    '''To check if the files have basic columns'''
    for file in uploaded_files:
        df = pd.read_csv(file.name)
        for col in df[0]:
            if col not in BASIC_COL_SET:
                st.write(f'{file} is missing basic columns. This program only merges files '
                         f'with {BASIC_COL_SET} columns. Please delete the file and reupload.')
                #return False
    print('done')   
    

def preview_uploads(uploaded_files):
    '''To show the preview of the files'''
    if uploaded_files:
        dfs = []  # List to store DataFrames read from uploaded files
        for file in uploaded_files:
            # file_name = file_name.append(file.name)
            df = pd.read_csv(file)
            dfs.append(df)
    for num in range(len(uploaded_files)):
        st.write(f'Preview {num + 1}:')
        st.dataframe(dfs[num][:1])


def merge_files(file_list, basic_cols_set): #Ask tutor about RuntimeWarning
    '''merging the files'''
    # Initialize merged_df with the first DataFrame
    merged_df = pd.read_csv(file_list[0])
    
    # Iterate over the remaining file paths and merge each DataFrame with merged_df
    for file in file_list[1:]:
        df = pd.read_csv(file)
        # Perform an outer join on the common columns
        merged_df = pd.merge(merged_df, df, on = BASIC_COL_SET, how = 'outer')
    return merged_df


def main():
    '''The main function includes other functions'''
    st.write("# Merge CSV Files")
    st.markdown(
        """This program is mainly to merge multiple csv files with same columns and 
        order of columns since we have limitation on extracting API data."""
                )
    
    uploaded_files = upload() # uploaded_files will be a list 
    if uploaded_files is not None:
        has_basic_cols(uploaded_files)
        preview_uploads(uploaded_files)
        

if __name__ == "__main__":
    main()