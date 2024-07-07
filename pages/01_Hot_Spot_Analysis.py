# %%
import inspect

import pandas as pd
import seaborn as sns
import streamlit as st
from hot_spot_analysis.hot_spot_analysis import HotSpotAnalyzer
from streamlit_extras.dataframe_explorer import dataframe_explorer

from utils.backend import dataset_manager

st.set_page_config(
    page_title="Hot Spot Analysis",
    page_icon="🔍",
    layout="wide",
)

# 0. Pick a dataset
st.markdown("***")
available_datasets = dataset_manager.available_datasets
st_dataset_name = str(st.selectbox("Select a dataset", available_datasets, index=0))

# Load the selected dataset & objective function
st_df: pd.DataFrame = dataset_manager.load_dataset(st_dataset_name)


def objective_function(df: pd.DataFrame) -> pd.DataFrame:
    return dataset_manager.dataset_agg_func(
        name=st_dataset_name,
        df=df,
    )


# Create two columns
st.markdown("***")
st.subheader(f"Aggregate metrics of {st_dataset_name} dataset")
col1, col2 = st.columns(2)
with col1:
    # 1. View the dataset, and see the out put of the related aggregation function
    st.write(st_df.head())

with col2:
    # 2. See the output of the objective function
    st.text("Below is the output of the objective function.")
    st.markdown("***")
    st.write(objective_function(st_df.groupby("overall")))  # type: ignore


st.markdown("***")
st.subheader(f"Pick features & interaction limit for HotSpotAnalysis")
col3, col4 = st.columns(2)

interactable_columns = list(st_df.select_dtypes(include=["category", "object"]).columns)
interactable_columns = [x for x in interactable_columns if x != "overall"]

with col3:
    # 3. Select at least 2 columns
    hsa_features = st.multiselect(
        "Select at least 2 columns for the hot spot analysis! There can be a delay if all are selected.",
        options=interactable_columns,
        default=None,
    )
    if len(hsa_features) < 2:
        st.error("Please select at least 2 columns.")

with col4:
    # 4. Select an interaction limit
    interaction_max = st.select_slider(
        "Select an interaction limit:",
        options=range(
            2,
            len(interactable_columns) + 1,
        ),
    )

# Save selections to session state
if st.button("Save Selections"):
    st.session_state["st_dataset_name"] = st_dataset_name
    st.session_state["st_df"] = st_df
    st.session_state["hsa_features"] = hsa_features
    st.session_state["interaction_max"] = interaction_max
    st.success("Hot Spot Analysis results are below:")


st.title("Hot Spot Analysis")

if "st_dataset_name" not in st.session_state:
    st.warning("Please make selections on the Input Selection page first.")
else:

    HSA = HotSpotAnalyzer(
        data=st.session_state["st_df"],
        target_cols=st.session_state["hsa_features"],
        interaction_limit=st.session_state["interaction_max"],
        objective_function=objective_function,
    )

    # 5. Process the DataFrame using the custom module
    HSA.run_hsa()
    hsa_data = HSA.export_hsa_output_df()

    # 6. Explore the output data frame
    st.subheader("HSA Data Output")
    st.dataframe(hsa_data, use_container_width=True)

    st.markdown("***")
    st.markdown("TODO: Add section using HSA search functions to let an user explore the results")
