import streamlit as st
import pandas as pd
import os

# Function to join Excel files based on selected columns
def join_excel_files(files, selected_columns):
    dfs = []
    for file in files:
        df = pd.read_excel(file)
        dfs.append(df)
    
    joined_df = dfs[0]  # Start with the first DataFrame
    for i in range(1, len(dfs)):
        joined_df = pd.merge(joined_df, dfs[i], on=selected_columns, how='inner')
    
    return joined_df

# Streamlit app
st.title("Excel File Joiner App")

# Upload multiple Excel files
st.sidebar.header("Upload Excel Files")
uploaded_files = st.sidebar.file_uploader("Upload your Excel files", type=["xlsx"], accept_multiple_files=True)

# Display uploaded data
st.sidebar.subheader("Uploaded Data")
if uploaded_files:
    uploaded_data = []
    for file in uploaded_files:
        st.sidebar.write(file.name)
        df = pd.read_excel(file)
        uploaded_data.append(df)

# Create dropdowns for selecting columns for each uploaded file
selected_columns = []
if uploaded_data:
    st.sidebar.header("Select Columns for Join")
    for i, df in enumerate(uploaded_data):
        st.sidebar.subheader(f"Columns for {uploaded_files[i].name}:")
        selected = st.sidebar.multiselect(f"Select columns for {uploaded_files[i].name}", df.columns)
        selected_columns.append(selected)

# Choose output format
st.sidebar.header("Choose Output Format")
output_format = st.sidebar.selectbox("Select output format", ["Excel (.xlsx)", "CSV (.csv)"])

# Display uploaded dataframes
if uploaded_data:
    st.sidebar.subheader("Uploaded Dataframes:")
    for i, df in enumerate(uploaded_data):
        st.sidebar.write(f"Data from {uploaded_files[i].name}:")
        st.sidebar.dataframe(df)

# Join and display the result
if st.sidebar.button("Join Excel Files"):
    if not all(selected_columns):
        st.warning("Please select at least one column for each uploaded file.")
    elif len(uploaded_files) < 2:
        st.warning("Please upload at least two Excel files.")
    else:
        joined_df = join_excel_files(uploaded_files, selected_columns[0])
        st.subheader("Joined Data:")
        st.dataframe(joined_df)
        
        # Download button
        st.sidebar.subheader("Download Joined Data")
        if output_format == "Excel (.xlsx)":
            csv = joined_df.to_excel(index=False)
            st.sidebar.download_button("Download as Excel", csv, key="excel_download")
        elif output_format == "CSV (.csv)":
            csv = joined_df.to_csv(index=False)
            st.sidebar.download_button("Download as CSV", csv, key="csv_download")
