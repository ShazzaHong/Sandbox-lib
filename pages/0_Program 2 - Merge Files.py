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
import io


BASIC_COL_SET = set(['siteid', 'sitename', 'datacreationdate', 'aqi', 'status'])


class FileHandler:
    '''This class is mainly to handle files. '''
    def __init__(self):
        self.uploaded_files = []

    def upload_files(self):
        # Upload files
        self.uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True)

    def process_files(self):
        for uploaded_file in self.uploaded_files:
            try:
                # Attempt to read the uploaded file
                file_contents = uploaded_file.read().decode("utf-8")
                df = pd.read_csv(io.StringIO(file_contents))
                st.write("DataFrame from uploaded file:")
                st.write(df[:5])
            except FileNotFoundError:
                st.error("File not found. Please make sure you uploaded the correct files.")


def main():
    '''The main function includes other functions'''
    st.write("# Merge CSV Files")
    st.markdown(
        """This program is mainly to merge multiple csv files with same columns and 
        order of columns since we have limitation on extracting API data."""
                )
    
    # Create an instance of FileHandler
    file_handler = FileHandler()

    # Call methods to upload and process files
    file_handler.upload_files()
    file_handler.process_files()
        

if __name__ == "__main__":
    main()