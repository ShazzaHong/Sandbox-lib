import streamlit as st
import pandas as pd
from io import StringIO

def check_nan(df):
    """Check if the DataFrame contains any NaN values."""
    return df.isnull().values.any()

def merge_csv(files):
    """Merge CSV files with outer join."""
    dfs = []
    for file in files:
        df = pd.read_csv(file)
        dfs.append(df)
    
    merged_df = pd.concat(dfs, axis=1, join='outer')
    return merged_df

def main():
    st.title("CSV File Merger")

    # File upload section
    st.subheader("Upload CSV files")
    uploaded_files = st.file_uploader("Upload CSV files", accept_multiple_files=True)

    if uploaded_files:
        # Check if any of the uploaded files contain NaN values
        for file in uploaded_files:
            df = pd.read_csv(file)
            if check_nan(df):
                st.error(f"File '{file.name}' contains NaN values. Please upload files with no NaN values.")
                return

        # Merge CSV files
        merged_df = merge_csv(uploaded_files)

        # Display merged DataFrame
        st.subheader("Merged DataFrame")
        st.write(merged_df)

        # Provide download link for merged CSV file
        csv_data = merged_df.to_csv(index=False)
        csv_data = csv_data.encode('utf-8')
        st.download_button(label="Download Merged CSV", data=csv_data, file_name='merged_data.csv', mime='text/csv')

if __name__ == "__main__":
    main()