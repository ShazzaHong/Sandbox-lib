import streamlit as st
import pandas as pd

# Initialize an empty list to store uploaded file names
uploaded_file_names = []

# Display file uploader widget to allow users to upload files
uploaded_files = st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)

# Update the list of uploaded file names when files are uploaded or deleted
if uploaded_files:
    # Add the filenames of newly uploaded files to the list
    for file in uploaded_files:
        uploaded_file_names.append(file.name)

    # Display the list of uploaded file names
    st.write("Uploaded File Names:")
    for filename in uploaded_file_names:
        st.write(filename)

# Allow the user to delete files from the list
files_to_delete = st.multiselect("Select files to delete", uploaded_file_names)
if files_to_delete:
    # Remove the selected files from the list of uploaded file names
    uploaded_file_names = [filename for filename in uploaded_file_names if filename not in files_to_delete]

# Process the uploaded files using the latest valid list of filenames
for filename in uploaded_file_names:
    st.write(f"Processing data from file: {filename}")
    file_data = pd.read_csv(filename)
    # Perform further processing with the file data
