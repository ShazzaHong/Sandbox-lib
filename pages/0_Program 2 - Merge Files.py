"""This is for the COSC480-24S1 project
   Project Name: Data Download Centre 
   Date: 2024-05-26
   Developer: Shuan Hong
   Program 2: Merge Files
   Purpose: This program is mainly to merge multiple csv files with same columns and 
   order of columns since we have limitation on extracting API data.
"""

#from typing import Any

import numpy as np
import streamlit as st
# from streamlit.hello.utils import show_code

uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)

for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    st.write(bytes_data)

st.set_page_config(page_title="Merge CSV Files", page_icon="📹")
st.markdown("# Merge CSV Files")
st.sidebar.header("2 - Merge CSV Files")
st.write(
    """This program is mainly to merge multiple csv files with same columns and 
   order of columns since we have limitation on extracting API data."""
)
