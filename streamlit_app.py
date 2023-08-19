import streamlit as st
import pandas as pd
import os

# Function to merge Excel files based on selected columns
def merge_excel_files(files, selected_columns):
    dfs = []
    for file in files:
        df = pd.read_excel(file)
        dfs.append(df)
    
    merged_df = pd.concat(dfs, ignore_index=True, sort=False)
    merged_df = merged_df.groupby(selected_columns).sum().reset_index()
    return merged_df

# Streamlit app
st.title("Excel File Merger App")

# Upload multiple Excel files
st.sidebar.header("Upload Excel Files")
uploaded_files = st.sidebar.file_uploader("Upload your Excel files", type=["xlsx"], accept_multiple_files=True)

# Common columns selection
st.sidebar.header("Select Columns for Merge")
selected_columns = st.sidebar.multiselect("Select columns for merging", [])  # Corrected line

# Choose output format
st.sidebar.header("Choose Output Format")
output_format = st.sidebar.selectbox("Select output format", ["Excel (.xlsx)", "CSV (.csv)"])

# Display uploaded data
st.sidebar.subheader("Uploaded Data")
if uploaded_files:
    for file in uploaded_files:
        st.sidebar.write(file.name)
        df = pd.read_excel(file)
        st.dataframe(df)

# Merge and display the result
if st.sidebar.button("Merge Excel Files"):
    if not selected_columns:
        st.warning("Please select at least one column for merging.")
    elif len(uploaded_files) < 2:
        st.warning("Please upload at least two Excel files.")
    else:
        merged_df = merge_excel_files(uploaded_files, selected_columns)
        st.subheader("Merged Data:")
        st.dataframe(merged_df)
        
        # Download button
        st.sidebar.subheader("Download Merged Data")
        if output_format == "Excel (.xlsx)":
            csv = merged_df.to_excel(index=False)
            st.sidebar.download_button("Download as Excel", csv, key="excel_download")
        elif output_format == "CSV (.csv)":
            csv = merged_df.to_csv(index=False)
            st.sidebar.download_button("Download as CSV", csv, key="csv_download")
