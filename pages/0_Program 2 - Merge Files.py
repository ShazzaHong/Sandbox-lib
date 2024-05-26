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
        '''Initialiser'''
        self.uploaded_files = []

    def upload_files(self):
        '''Upload files'''
        uploaded_filenames = []
        self.uploaded_files = st.file_uploader("Upload files", accept_multiple_files = True)
        for uploaded_file in self.uploaded_files:
            uploaded_filenames.append(uploaded_file.name)
        return uploaded_filenames

    def process_files(self):
        '''To read the file and convert it to pandas dataframe if no error found.'''
        dfs = []
        for uploaded_file in self.uploaded_files:
            try:
                file_contents = uploaded_file.read().decode("utf-8")
                df = pd.read_csv(io.StringIO(file_contents))
                dfs = dfs.append(df)
                st.write(f"DataFrame from uploaded file - {uploaded_file.name}:")
                st.write(df[:2])
                return dfs
            except FileNotFoundError:
                st.error("File not found. Please make sure you uploaded the correct files.")
    
    def has_basic_cols(self, dfs):
        '''To check if the files have basic columns.'''
        for df in dfs:
            for col in df[0]:
                if col not in BASIC_COL_SET:
                    st.write(f'{file} is missing basic columns. This program only merges files '
                            f'with {BASIC_COL_SET} columns. Please delete the file and reupload.')
                    #return False
        print('done')   


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
    uploaded_filenames = file_handler.upload_files()
    dfs = file_handler.process_files()
    file_handler.has_basic_cols(dfs)

if __name__ == "__main__":
    main()