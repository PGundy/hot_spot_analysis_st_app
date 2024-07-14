import pandas as pd
import streamlit as st

# Sample data for analysis
data = pd.DataFrame(
    {
        "Name": ["Alice", "Bob", "Charlie", "David"],
        "Score": [85, 92, 78, 90],
        "Department": ["HR", "Engineering", "Marketing", "Engineering"],
    }
)

# Title of the app
st.title("Simple Streamlit App")

# Section 1: Multiple selection options
st.header("Step 1: Select Options")

departments = st.multiselect("Select Departments", options=data["Department"].unique())

# Button to run analysis
if st.button("Run Analysis"):
    st.session_state.analysis_done = True

    # Filter the data based on the selected departments
    if departments:
        filtered_data = data[data["Department"].isin(departments)]
    else:
        filtered_data = data

    # Display the filtered data
    st.write("Analysis Results:")
    st.dataframe(filtered_data)

# Section 2: Search within results
if st.session_state.get("analysis_done", False):
    st.header("Step 2: Search Results")

    search_term = st.text_input("Search by Name")

    if search_term:
        search_results = filtered_data[filtered_data["Name"].str.contains(search_term, case=False)]
        st.write("Search Results:")
        st.dataframe(search_results)
    else:
        st.write("Enter a name to search.")
