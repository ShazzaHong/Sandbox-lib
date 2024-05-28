"""This is for the COSC480-24S1 project
   Project Name: Data Download Centre 
   Date: 2024-05-26
   Developer: Shuan Hong
   Program 3: Plot Graphs with Class
   Purpose: This program is mainly to plot the charts by using the AQI file 
            users downloaded/merged
"""

import os # os.path.exists() is used to check whether a file or directory exists at a given path.
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd # we gonna save our data into a pandas data frame and use read_csv() function


class AQIDataAnalyzer:
    '''This is a class to ask file name and the need of filter'''
    def __init__(self):
        self.basic_columns = ['siteid', 'sitename', 'datacreationdate', 'aqi', 'status']

    def check_columns(self, filename):
        '''Check if the necessary columns exist.'''
        df = pd.read_csv(filename, nrows=1)
        columns = df.columns.tolist()
        missing_columns = [col for col in self.basic_columns if col not in columns]
        if missing_columns:
            print("Your file is missing necessary column(s) for plotting. \n"
                      f"Necessary columns are {self.basic_columns} \n"
                      f"and you missed {missing_columns}. \n"
                      "Please check the column name(s).")
        else:
            return True, columns

    def ask_file(self):
        '''Ask users to enter the file names they want to plot and check if 
        they are retrievable. continue is a keyword used within loops to skip 
        the rest of the code inside the loop for the current iteration and move 
        to the next iteration. See if it can be replaced by elif.'''
        while True:
            filename = input("Enter the file name you want to plot "
                                 "(with .csv and in the same folder): ").strip()
            if not filename.lower().endswith('.csv'):
                print("Invalid file name. Please enter a filename with the .csv extension.")
                continue
            if not os.path.exists(filename):
                print(f"Error: File '{filename}' does not exist in the current directory.")
                continue
            is_valid, columns = self.check_columns(filename)
            if self.check_columns(filename):
                return filename, columns   
                
    def need_filter(self):
        '''Asking if user need filter. If not, then it will plot the default 
        setting'''
        print(f"Do you want to filter site and pollutant to plot, or use default" 
              " setting which is the the hourly AQI in site 1 - Keelung?", end = ' ') 
        is_done = False 
        while True:
            answer = input(f"Enter Y to choose filter, N to use default setting: ")
            if answer not in ['Y', 'N']:
                print("Only Y or N allowed!!", end = ' ')
            else:
                return answer
    
    def available_siteid(self, df):
        '''To give use available options of site id in the file.'''
        id_dict = {}
        for id_n in df['siteid']:
            id_dict[id_n] = id_n
        return sorted(id_dict.values()) # a list of available_ids

    def set_siteid(self, available_ids): 
        '''
        Let users filter site by entering its id.
        siteid.isdigit() is used to check if siteid is a valid integer, but 
        siteid can still be string, so we need to convert siteid from string to 
        an integer so we can compare the value with the value in available_ids set.
        '''
        print(f"Available site ids in the file: {available_ids}")
        is_valid = False
        while not is_valid:
            siteid = input("Please enter one site id listed above: ")
            if siteid.isdigit():
                siteid = int(siteid)
                if siteid in set(available_ids):
                    is_valid = True
                else:   
                    print("site id is not in the given id list.")
            else:
                print("Invalid input. Please enter a valid integer.")
        return siteid
     
    def set_pollutant(self, columns):
        '''Ask users to set the filter for pollutants. Users can type 'all' to 
        get all pollutant.'''
        addition_cols = [col for col in columns if col not in self.basic_columns]
        valid_cols = ['pm2.5', 'so2', 'o3', 'co', 'pm10', 'no2', 'no']
        intersection_set = set(addition_cols) and set(valid_cols)
        intersection_set.add('all')
        is_valid = False
        while not is_valid:
            pollutant = input(f"Please enter one pollutant among {intersection_set} "
                              "('all' means plot all pollutants): ")
            if pollutant.lower() in intersection_set:
                is_valid = True 
            else:
                print(f"Invalid input! You can only choose from {intersection_set}", end = ' ')
        return pollutant.lower(), intersection_set


class Plot:
    """
    A class to generate plots based on AQI data.

    This class provides methods to plot filtered AQI data for a specific site 
    and pollutant, plot all pollutants over time for a specific site, and plot 
    default pollutant levels over time at a predefined site.

    Methods:
       1. __init__(self, df): Initialize the Plot class with the DataFrame 
          containing AQI data.
       2. plot_filtered_data(self, siteid, pollutant): Plot filtered data for 
          a specific site and pollutant.
       3. plot_filtered_site_all_pollutants(self, siteid): Plot all pollutants 
          over time for a specific site.
       4. plot_default(self): Plot default pollutant levels over time at a 
          predefined site.
    """

    def __init__(self, df):
        """Initialize the Plot class with the DataFrame containing AQI data.
        Parameter: df (DataFrame): DataFrame containing AQI data."""
        self.df = df

    def plot_filtered_data(self, siteid, pollutant):
        '''Plotting with filtered data (one pollutant only).
        First, filter the siteid is equal to the chosen one. And then sort 
        the 'datacreationdate' column before ploting, so that the time series 
        will start from the earlist time.
        I set create a new figure with the size (width, height) in inches, 
        but users can adjust it if they know coding.'''
        filtered_df = self.df[self.df['siteid'] == siteid]
        sitename = np.array(filtered_df)[1,1]
        sorted_filtered_df = filtered_df.sort_values(by='datacreationdate', 
                                                     ascending=True)
        plt.figure(figsize=(10, 6)) 
        plt.plot(sorted_filtered_df['datacreationdate'], 
                 sorted_filtered_df[pollutant], marker ='o')
        plt.xticks(rotation=10)
        plt.xlabel('Date Time')
        plt.ylabel(f'{pollutant.upper()} (µg/m³)')
        plt.title(f'{pollutant.upper()} level over Time at {sitename}')
        plt.grid(True)
        plt.show()

    def plot_filtered_site_all_pollutants(self, siteid, intersection_set): 
        '''Plotting the filtered site with all pollutants available.'''
        filtered_df = self.df[self.df['siteid'] == siteid]
        sorted_filtered_df = filtered_df.sort_values(by='datacreationdate', 
                                                     ascending = True)
        site_name = np.array(filtered_df)[1,1]
        intersection_set.remove('all')
        plt.figure(figsize=(10, 6))
        for pollutant in intersection_set:
            plt.plot(sorted_filtered_df['datacreationdate'], 
                     sorted_filtered_df[pollutant],
                     label = pollutant.upper(), marker = 'o')
        plt.xticks(rotation=10)
        plt.xlabel('Date Time')
        plt.ylabel('Pollutant Level (µg/m³)')
        plt.title(f'All Pollutants over Time at {site_name}')
        plt.grid(True)
        plt.legend()  
        plt.show()

    def plot_default(self):
        '''Plotting the default setting: only AQI at Keelung site. 
        Assumption: every file has site 1 data.''' 
        filtered_df = self.df[self.df['siteid'] == 1]
        sorted_filtered_df = filtered_df.sort_values(by = 'datacreationdate', 
                                                     ascending = True) 
        plt.figure(figsize=(10, 6))
        plt.plot(sorted_filtered_df['datacreationdate'], 
                 sorted_filtered_df['aqi'], label='AQI', marker='o')
        plt.xticks(rotation=10)
        plt.xlabel('Date Time')
        plt.ylabel('AQI Level (µg/m³)')
        plt.title(f'AQI levels over time at Keelung')
        plt.grid(True)
        plt.legend()  
        plt.show()

def continue_plot():
    '''This is to check the intention of user to see if they want to keep using 
    this program.'''
    while True:
        continue_or_quit = input("Do you want to continue plotting or quit (c/q)? ")
        if continue_or_quit == 'c':
            return True
        if continue_or_quit == 'q':
            print("Thanks for using. Bye~")
            return False
        else:
            print("Invalid value. Please enter either c or q to continue or quit: ")    


def set_filter(analyzer, df, columns):
    '''If user want filter, then this functino will ask them the setting of the 
    filter. There are two filter: site id and pollutant. Because there is 
    full-width left parenthesis character in the file (sitename column) and 
    that is not available in the default font Matplotlib configurate. 
    I added 'Heiti TC' font to ensure that the warning no longer appears.'''
    plotter = Plot(df)
    plt.rcParams['font.family'] = 'Heiti TC'
    while True:
        if analyzer.need_filter() == 'Y':
            available_ids = analyzer.available_siteid(df)
            siteid = analyzer.set_siteid(available_ids) 
            pollutant, intersection_set = analyzer.set_pollutant(columns) # already in lower the case
            if pollutant == 'all':
                plotter.plot_filtered_site_all_pollutants(siteid, intersection_set)
            else:
                plotter.plot_filtered_data(siteid, pollutant)
        else:
            plotter.plot_default()
        if continue_plot() == False:
            return False
    

def main():
    '''To let user choose file and filters to plot the chart. Depends on their 
    setting, differnt kind of charts will be generated.'''
    analyzer = AQIDataAnalyzer()
    filename, columns = analyzer.ask_file()
    df = pd.read_csv(filename)
    df['datacreationdate'] = pd.to_datetime(df['datacreationdate']) # Convert 'datacreationdate' column to datetime type
    set_filter(analyzer, df, columns)


main() # 2024-05-26 21_to_2024-05-27 08_aqi_data.csv