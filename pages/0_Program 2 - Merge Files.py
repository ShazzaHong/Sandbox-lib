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


BASIC_COLS = ['siteid', 'sitename', 'datacreationdate', 'aqi', 'status']


class FileHandler:
    '''This class is mainly to handle files. '''
    def __init__(self):
        '''Initialiser'''
        self.uploaded_files = []

    def upload_files(self):
        '''Upload files'''
        uploaded_files = []
        uploaded_filenames = []
        self.uploaded_files = st.file_uploader("Upload files", accept_multiple_files = True)
        if self.uploaded_files is not None:
            # Append the uploaded file to the list of uploaded files
            uploaded_files.append(self.uploaded_files)
        for i, file in enumerate(self.uploaded_files):
            delete_checkbox = st.checkbox(f"Delete {file.name}")
            if delete_checkbox:
                uploaded_files.remove(file)
        return uploaded_filenames # delete if not using

    def process_files(self):
        '''To read the file and convert it to pandas dataframe if no error found.
        At the same time, collect the column names (headers) of csv files and 
        store in a dictionary for later use.'''
        list_of_dfs = []
        dict_of_headers = {}
        for uploaded_file in self.uploaded_files:
            try:
                file_contents = uploaded_file.read().decode("utf-8")
                if len(file_contents) > 0:
                    df = pd.read_csv(io.StringIO(file_contents))
                    list_of_dfs = list_of_dfs.append(df)
                    col_list = df.columns.tolist()
                    dict_of_headers[uploaded_file.name] = col_list
                    st.write(f"DataFrame from uploaded file - {uploaded_file.name}:")
                    st.write(df[:2])
                    st.write(type(list_of_dfs))
                    return list_of_dfs, dict_of_headers
            except FileNotFoundError:
                st.error("File not found. Please make sure you uploaded the correct files.")


    def de_has_basic_cols(self, list_of_dfs):
        '''To check if the files have basic columns.'''
        for df_i in list_of_dfs: # enumerate adds a counter to an iterable object (like a list, tuple, or string) and returns it as an enumerate object. 
            cols = df_i.columns.tolist()
            for bcs in BASIC_COLS:
                if bcs not in set(cols):
                    st.write(f'Missing basic columns. This program only merges files '
                            f'with {BASIC_COLS} columns. Please delete the file and reupload.')
                    #return False
        print('done')   

    def has_basic_cols(self, list_of_dfs):
        '''Check if all DataFrames in the list contain the basic columns.'''
        for i, df in enumerate(list_of_dfs, 1):
            missing_cols = [col for col in BASIC_COLS if col not in df.columns]
            if missing_cols:
                st.warning(f"DataFrame {i} is missing basic columns: {', '.join(missing_cols)}")
                return False
        return True


def main():
    '''The main function includes other functions'''
    st.write("# Merge CSV Files")
    st.markdown(
        """This program is mainly to (outer join) merge multiple csv files with basic columns 
        ('siteid', 'sitename', 'datacreationdate', 'aqi', 'status'). The merged file allows 
        user to plot longer time series (charts).
        """
        )
    
    # Create an instance of FileHandler (class)
    file_handler = FileHandler()

    # Call methods to upload and process files
    uploaded_filenames = file_handler.upload_files()
    
    if file_handler.process_files():
        list_of_dfs, dict_of_headers = file_handler.process_files()
    
    print('success')


if __name__ == "__main__":
    main()