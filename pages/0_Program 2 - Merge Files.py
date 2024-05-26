"""This is for the COSC480-24S1 project
   Project Name: Data Download Centre 
   Date: 2024-05-26
   Developer: Shuan Hong
   Program 2: Merge Files
   Purpose: This program is mainly to merge multiple csv files with same columns and 
   order of columns since we have limitation on extracting API data.
"""

import pandas as pd
import streamlit as st

def upload():
    '''To let users upload the files they want to merge'''
    uploaded_files = st.file_uploader("Choose CSV file(s) you want to merge", 
                                      type = 'csv', accept_multiple_files = True)
    return uploaded_files


def show_uploads(uploaded_files):
    '''To show the preview of the files'''
    if uploaded_files:
        dfs = []  # List to store DataFrames read from uploaded files
        for file in uploaded_files:
            # file_name = file_name.append(file.name)
            df = pd.read_csv(file)
            dfs.append(df)
    for num in range(len(uploaded_files)):
        st.write(f'Preview {num}:')
        st.table(dfs[0][:2])


def main():
    '''The main function includes other functions'''
    st.write("# Merge CSV Files")
    st.markdown(
        """This program is mainly to merge multiple csv files with same columns and 
        order of columns since we have limitation on extracting API data."""
                )
    st.sidebar.header("2 - Merge CSV Files")
    uploaded_files = upload() # uploaded_files will be a list 
    if uploaded_files is not None:
        show_uploads(uploaded_files)


if __name__ == "__main__":
    main()