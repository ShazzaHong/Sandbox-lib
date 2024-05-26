"""This is for the COSC480-24S1 project
   Project Name: Data Download Centre 
   Date: 2024-05-26
   Developer: Shuan Hong
   Program 2: Merge Files
   Purpose: This program is mainly to merge multiple csv files with same columns and 
   order of columns since we have limitation on extracting API data.
"""

import streamlit as st

def upload():
    '''To let users upload the files they want to merge'''
    uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        st.write(bytes_data)

def main():
    '''The main function includes other functions'''
    st.write("# Merge CSV Files")
    st.markdown(
        """This program is mainly to merge multiple csv files with same columns and 
        order of columns since we have limitation on extracting API data."""
                )
    st.sidebar.header("2 - Merge CSV Files")
    st.write(
        """This program is mainly to merge multiple csv files with same columns and 
    order of columns since we have limitation on extracting API data."""
    )
    upload()

    
if __name__ == "__main__":
    main()