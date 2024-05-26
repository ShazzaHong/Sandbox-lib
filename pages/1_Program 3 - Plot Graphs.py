
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd # we gonna save our data into a pandas data frame
#from datetime import datetime, timedelta 


class AQIDataAnalyzer:
    '''This is a class to ask file name and the need of filter'''
    def __init__(self):
        self.columns = ['site_id','site_name','created_date','PM2.5','SO2','O3']

    def check_columns(self, filename):
        '''Check if the necessary columns exist to plot'''
        df = pd.read_csv(filename, nrows=1)
        columns = df.columns.tolist()
        missing_columns = [col for col in self.columns if col not in columns]
        if missing_columns:
            return False
        else:
            return True       

    def ask_file(self):
        '''Ask users to enter the file names they want to plot and check if 
        they are retrievable.'''
        while True:
            filename = input("Enter the file name you want to plot "
                                 "(with .csv and in the same folder): ").strip()
            if not filename.lower().endswith('.csv'):
                print("Invalid file name. Please enter a filename with the .csv extension.")
                continue            
            if not os.path.exists(filename):
                print(f"Error: File '{filename}' does not exist in the current directory.")
                continue            
            if self.check_columns(filename):
                return filename
            else:
                print("Your file is missing necessary columns for plotting. \n"
                      f"Necessary columns are: {self.columns}")
                
    def need_filter(self):
        '''Asking if user need filter. If not, then it will plot the default 
        setting'''
        print(f"Do you want to filter site and pollutant to plot or use default" 
              " setting which is the the hourly PM2.5 in site 1 - Keelung ?")
        is_done = False 
        while True:
            answer = input(f"Enter Y to choose filter, N to use default setting: ")
            if answer not in ['Y', 'N']:
                print("Only Y or N allowed!!", end = ' ')
            else:
                return answer
    
    def set_site_id(self): 
        '''set the filter site by entering id'''
        is_valid = False
        while not is_valid:
            site_id = input("Please enter one site id (1~313): ")
            if site_id.isdigit(): # Check if site_id is a valid integer
                site_id = int(site_id) # Convert site_id to an integer
                if 1 <= site_id <= 313: # Check if site_id is in the range of 1~313
                    is_valid = True
                else:   
                    print("site id is not within the range of 1 to 313.")
            else:
                print("Invalid input. Please enter a valid integer.")
        return site_id

            
    def set_pollutant(self):
        '''set the filter for pollutants'''
        is_valid = False
        while not is_valid:
            pollutant = input("Please enter one pollutant (PM2.5/SO2/O3) "
                              "or enter 'all' to plot all pollutants: ")
            if pollutant in ['PM2.5', 'SO2', 'O3', 'all']:
                is_valid = True 
            else:
                print("Invalid input!", end = ' ')
        return pollutant


class Plot:
    """
    A class to generate plots based on AQI data.

    This class provides methods to plot filtered AQI data for a specific site 
    and pollutant, plot all pollutants over time for a specific site, and plot 
    default pollutant levels over time at a predefined site.

    Methods:
       1. __init__(self, df): Initialize the Plot class with the DataFrame 
          containing AQI data.
       2. plot_filtered_data(self, site_id, pollutant): Plot filtered data for 
          a specific site and pollutant.
       3. plot_filtered_site_all_pollutants(self, site_id): Plot all pollutants 
          over time for a specific site.
       4. plot_default(self): Plot default pollutant levels over time at a 
          predefined site.
    """

    def __init__(self, df):
        """
        Initialize the Plot class with the DataFrame containing AQI data.

        Parameters:
            df (DataFrame): DataFrame containing AQI data.
        """
        self.df = df

    def plot_filtered_data(self, site_id, pollutant):
        '''Plotting with filtered data (one pollutant only).'''
        # Filter the data where site_id is equal to the chosen one
        filtered_df = self.df[self.df['site_id'] == site_id]
        site_name = np.array(filtered_df)[1,1]
        # sort the 'created_date' column 
        sorted_filtered_df = filtered_df.sort_values(by='created_date', 
                                                     ascending=True)
        # Plot the filtered data
        plt.figure(figsize=(10, 6)) # Create a new figure with the size (width, height) in inches
        plt.plot(sorted_filtered_df['created_date'], sorted_filtered_df[pollutant])
        plt.xticks(rotation=10)
        plt.xlabel('Date Time')
        plt.ylabel(f'{pollutant} (µg/m³)')
        plt.title(f'{pollutant} level over Time at {site_name}')
        plt.grid(True)
        plt.show()

    def plot_filtered_site_all_pollutants(self, site_id): # is it too long?
        '''Plotting the filtered site with all pollutants.'''
        filtered_df = self.df[self.df['site_id'] == site_id]
        # sort the 'created_date' column 
        sorted_filtered_df = filtered_df.sort_values(by='created_date', 
                                                     ascending=True)
        s_f_df = sorted_filtered_df # shorten the name for pylint purpose
        site_name = np.array(filtered_df)[1,1]
        # Plot the filtered data.
        plt.figure(figsize=(10, 6))
        plt.plot(s_f_df['created_date'], s_f_df['PM2.5'], label='PM2.5', marker='o')
        plt.plot(s_f_df['created_date'], s_f_df['SO2'], label='SO2', marker='s')
        plt.plot(s_f_df['created_date'], s_f_df['O3'], label='O3', marker='^')
        plt.xticks(rotation=10)
        plt.xlabel('Date Time')
        plt.ylabel('Pollutant Level (µg/m³)')
        plt.title(f'All Pollutants over Time at {site_name}')
        plt.grid(True)
        plt.legend()  
        plt.show()

    def plot_default(self): # should it be link this long? Will this be minus in pylint style check?
        '''Plotting the default setting: All pollutant @ Keelung site'''
        filtered_df = self.df[self.df['site_id'] == 1]
        # sort the 'created_date' column 
        sorted_filtered_df = filtered_df.sort_values(by = 'created_date', ascending = True)
        s_f_df = sorted_filtered_df # shorten the name for pylint purpose
        # Plot the filtered data.
        plt.figure(figsize=(10, 6))
        plt.plot(s_f_df['created_date'], s_f_df['PM2.5'], label='PM2.5', marker='o')
        plt.plot(s_f_df['created_date'], s_f_df['SO2'], label='SO2', marker='s')
        plt.plot(s_f_df['created_date'], s_f_df['O3'], label='O3', marker='^')
        plt.xticks(rotation=10)
        plt.xlabel('Date Time')
        plt.ylabel('Pollutant Level (µg/m³)')
        plt.title(f'Pollutant levels over time at Keelung')
        plt.grid(True)
        plt.legend()  
        plt.show()


def main():
    '''To let user choose file and filters to plot the chart. Depends on their 
    setting, differnt kind of charts will be generated.'''
    analyzer = AQIDataAnalyzer()
    filename = analyzer.ask_file()
    df = pd.read_csv(filename)
    df['created_date'] = pd.to_datetime(df['created_date']) # Convert 'created_date' column to datetime type
    plotter = Plot(df)
    if analyzer.need_filter() == 'Y':
        site_id = analyzer.set_site_id() 
        pollutant = analyzer.set_pollutant() 
        if pollutant == 'all':
            plotter.plot_filtered_site_all_pollutants(site_id)
        else:
            plotter.plot_filtered_data(site_id, pollutant)
    else:
        plotter.plot_default()


if __name__ == "__main__":
    main() 