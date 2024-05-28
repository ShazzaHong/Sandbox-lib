"""This is for the COSC480-24S1 project
   Project Name: Data Download Centre 
   Date: 2024-05-29
   Developer: Shuan Hong
   Program 2: Merge Files
   Purpose: This program is mainly to merge multiple csv files with same columns 
   and order of columns since we have limitation on extracting API data.
"""

import pandas as pd
import os # It allows us to perform various operating system-related tasks


# List of basic common columns
COMMON_COLS = ['siteid', 'sitename', 'datacreationdate', 'aqi', 'status']

    
def has_common_columns(filename):
    '''
    Compare the columns between CSV files.
    Returns True if the files have the basic commmon columns, False otherwise.
    '''
    df = pd.read_csv(filename, nrows = 1)
    columns = df.columns.tolist() # confirm if tolist() is to convert object to list data type
    # Check if the columns match COMMON_COLS
    for col in COMMON_COLS:
        if col not in set(columns):
            print(f"{filename} doesn't fit the requirement of columns. {col} missing")
            return False 
        else:
            return True
    
    
def ask_files(): # shorten it
    '''Ask users to enter the file names they want to merge and 
    check if they are retrievable.'''
    # Initialize an empty list to store file paths
    file_list = []
    while True:
        filename = input('Enter a file name with .csv (enter q to quit and go next step): ').strip() 
        if filename.lower() == 'q':
            if len(file_list) < 2:
                print("Error: You must enter at least two valid file names before quitting.")
                continue
            else:
                break
        if not filename.lower().endswith('.csv'):
            print("Invalid file name. Please enter a filename with the .csv extension.")
            continue            
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' does not exist in the current directory.")
            continue            
        if has_common_columns(filename):
            file_list.append(filename)
    return file_list

    
def merge_files(file_list):
    '''
    Merging the files. 
    First, initialize merged_df with the first DataFrame.
    Iterate over the remaining file paths and merge each DataFrame with merged_df.
    In order to prevent extra columns with suffixes generated while using 
    outer join to merge data frames, we need to identify overlapping columns 
    with the same values. equals() method in pandas is used to compare two 
    pandas objects. Then we remove overlapping columns from one of the DataFrames 
    while keeping basic columns (COMMON_COLS). The second for loop is to ensure 
    basic columns are kept by adding them back to the DataFrame. 
    '''
    merged_df = pd.read_csv(file_list[0])

    for file in file_list[1:]:
        df = pd.read_csv(file) 
        overlap_cols = [col for col in merged_df.columns if col in df.columns 
                        and merged_df[col].equals(df[col])] 
        merged_df_filtered = merged_df.drop(columns = overlap_cols)
        for col in COMMON_COLS:
            if col not in merged_df_filtered.columns:
                merged_df_filtered[col] = merged_df[col]        

        merged_df = pd.merge(merged_df_filtered, df, on = COMMON_COLS, how = 'outer')
    return merged_df


def name_file(sorted_merged_df):
    '''
    Let user name the file with .csv extension and remind them the naming.
    Write the result to a new CSV file by using to_csv() method in pandas library.
    '''
    done = False
    while not done:
        merged_filename = input("Please name the merged csv file (with .csv). "
                                "Be careful of naming, so it won't overwrite: ")
        result = merged_filename.strip().lower().endswith('.csv') # T/F
        if result:
            sorted_merged_df.to_csv(merged_filename, index = False) # need to exclude the first column (index)
            print("Complete!")
            done = True
        else:
            print("Wrong naming! Your file name has to include .csv extension.")
        
    
def main():
    '''let users choose the files they want to merge'''
    print('Please enter the csv file names you want to merge.\n'
          'The files have to include the following columns:\n'
          f'{COMMON_COLS}')
    file_list = ask_files() 
    print(f"The entered files:")
    for file in file_list:
        print(file)    
    merged_df = merge_files(file_list)  
    name_file(merged_df)


main() # test: 2024-05-28 04_to_2024-05-28 05_aqi_data.csv and 2024-05-28 04_to_2024-05-28 05_aqi_data (2).csv