import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

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
        filename = st.text_input("Enter the file name you want to plot (with .csv and in the same folder): ").strip()
        if filename and not filename.lower().endswith('.csv'):
            st.error("Invalid file name. Please enter a filename with the .csv extension.")
            return None
        if filename and not os.path.exists(filename):
            st.error(f"Error: File '{filename}' does not exist in the current directory.")
            return None
        if filename and not self.check_columns(filename):
            st.error("Your file is missing necessary columns for plotting.")
            st.info(f"Necessary columns are: {self.columns}")
            return None
        return filename

    def need_filter(self):
        '''Asking if user need filter. If not, then it will plot the default 
        setting'''
        st.write("Do you want to filter site and pollutant to plot or use default setting which is the the hourly PM2.5 in site 1 - Keelung ?")
        return st.radio("Enter Y to choose filter, N to use default setting:", ('Y', 'N'))

    def set_site_id(self): 
        '''set the filter site by entering id'''
        site_id = st.number_input("Please enter one site id (1~313): ", min_value=1, max_value=313)
        return site_id

    def set_pollutant(self):
        '''set the filter for pollutants'''
        return st.selectbox("Please enter one pollutant (PM2.5/SO2/O3) or enter 'all' to plot all pollutants:", ['PM2.5', 'SO2', 'O3', 'all'])

class Plot:
    """
    A class to generate plots based on AQI data.
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
        filtered_df = self.df[self.df['site_id'] == site_id]
        site_name = np.array(filtered_df)[1,1]
        sorted_filtered_df = filtered_df.sort_values(by='created_date', ascending=True)
        plt.figure(figsize=(10, 6))
        plt.plot(sorted_filtered_df['created_date'], sorted_filtered_df[pollutant])
        plt.xticks(rotation=10)
        plt.xlabel('Date Time')
        plt.ylabel(f'{pollutant} (µg/m³)')
        plt.title(f'{pollutant} level over Time at {site_name}')
        plt.grid(True)
        st.pyplot()

    def plot_filtered_site_all_pollutants(self, site_id):
        '''Plotting the filtered site with all pollutants.'''
        filtered_df = self.df[self.df['site_id'] == site_id]
        sorted_filtered_df = filtered_df.sort_values(by='created_date', ascending=True)
        s_f_df = sorted_filtered_df
        site_name = np.array(filtered_df)[1,1]
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
        st.pyplot()

    def plot_default(self):
        '''Plotting the default setting: All pollutant @ Keelung site'''
        filtered_df = self.df[self.df['site_id'] == 1]
        sorted_filtered_df = filtered_df.sort_values(by='created_date', ascending=True)
        s_f_df = sorted_filtered_df
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
        st.pyplot()


def main():
    '''To let user choose file and filters to plot the chart. Depends on their 
    setting, differnt kind of charts will be generated.'''
    st.write("""# Plot Graphs with Streamlit""")
    analyzer = AQIDataAnalyzer()
    filename = analyzer.ask_file()
    if filename:
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
