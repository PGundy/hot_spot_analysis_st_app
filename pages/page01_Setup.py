# %%
import pandas as pd
import seaborn as sns
import streamlit as st

from utils.backend import dataset_manager

# %%


st.title("Setup")

# 1. Pick a dataset
available_datasets = dataset_manager.available_datasets
st_dataset_name = str(st.selectbox("Select a dataset", available_datasets))

# Load the selected dataset
st_df = dataset_manager.load_dataset(st_dataset_name)

# 2. View the dataset, and see the out put of the related aggregation function
st.subheader(f"Aggregate metrics of {st_dataset_name} dataset")

st.write(st_df.head())
st.write(dataset_manager.agg_func(st_dataset_name, st_df))


# 3. Select at least 2 columns
hsa_features = st.multiselect(
    "Select at least 2 columns for the hot spot analysis!",
    options=list(st_df.columns),
    default=None,
)
if len(hsa_features) < 2:
    st.warning("Please select at least 2 columns.")

# 4. Select an interaction limit
interaction_max = st.select_slider(
    "Select an interaction limit:",
    options=range(
        2,
        len(st_df.columns),
    ),
)

# Save selections to session state
if st.button("Save Selections"):
    st.session_state["st_dataset_name"] = st_dataset_name
    st.session_state["st_df"] = st_df
    st.session_state["hsa_features"] = hsa_features
    st.session_state["interaction_max"] = interaction_max
    st.success("Selections saved. Go to the Results page to see the processed data.")
