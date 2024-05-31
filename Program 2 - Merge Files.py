"""This is for the COSC480-24S1 project
   Project Name: Data Download Centre 
   Date: 2024-05-31
   Developer: Shuan Hong
   Program 2: Merge Files
   Purpose: This program is mainly to merge/combine multiple csv files with 
   same columns and order of columns since we have upper limit on extracting API 
   data.
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
    columns = df.columns.tolist()
    for col in COMMON_COLS:
        if col not in set(columns):
            print(f"{filename} doesn't fit the requirement of columns. {col} missing")
            return False 
        else:
            return True
    
    
def ask_files():
    '''Ask users to enter the file names they want to merge and 
    check if they are retrievable.'''
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
    First, initialize merged_df with the first DataFrame and set the COMMON_COLS
    as index for combining data.
    Iterate over the remaining file paths and combine each DataFrame with merged_df.
    combine_first() is a method in Pandas DataFrame objects. It's used to combine 
    two DataFrames, filling missing values in one DataFrame with non-missing values 
    from another DataFrame.
    However, since combine_first() will only combine the overlapping index, I 
    use append to add data back (in the second for loop). I reorder the columns 
    in the middle.
    '''
    merged_df = pd.read_csv(file_list[0]).set_index(COMMON_COLS)
    for file in file_list[1:]:
        df = pd.read_csv(file).set_index(COMMON_COLS)
        merged_df.reset_index(inplace=True) # Reset indices of both DataFrames
        df.reset_index(inplace=True)
        merged_df = merged_df.combine_first(df).fillna(merged_df).fillna(df)  
    merged_df.reset_index(inplace = True)
    new_columns_order = COMMON_COLS + [col for col in merged_df.columns if col 
                                       not in COMMON_COLS]
    merged_df = merged_df[new_columns_order] # Reorder
    for file in file_list[1:]:
        df = pd.read_csv(file)
        merged_df = merged_df.append(df, ignore_index = True)
    return merged_df    


def name_file(merged_df):
    '''
    Let user name the file with .csv extension and remind them the naming.
    Write the result to a new CSV file by using to_csv() method in pandas library.
    '''
    done = False
    while not done:
        merged_filename = input("Please name the merged csv file (with .csv). "
                                "Be careful of naming, so it won't overwrite: ").strip()
        result = merged_filename.strip().lower().endswith('.csv') # T/F
        if result:
            merged_df.to_csv(merged_filename, index = False) # need to exclude the first column (index)
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


main()
# test: 2024-05-30 18_to_2024-05-30 2_aqi_data.csv  , 2024-05-30 19_to_2024-05-31 05_aqi_data.csv  ,   2024-05-30 16_to_2024-05-30 21_aqi_data.csv