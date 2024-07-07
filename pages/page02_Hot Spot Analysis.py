import seaborn as sns
import streamlit as st
from hot_spot_analysis.hot_spot_analysis import HotSpotAnalyzer

from utils.backend import dataset_manager

st.title("Hot Spot Analysis")

if "st_dataset_name" not in st.session_state:
    st.warning("Please make selections on the Input Selection page first.")
else:
    HSA = HotSpotAnalyzer(
        data=st.session_state["st_df"],
        target_cols=st.session_state["hsa_features"],
        interaction_limit=st.session_state["interaction_max"],
        objective_function=dataset_manager.aggregate_tips,
    )

    # 5. Process the DataFrame using the custom module
    HSA.run_hsa()
    hsa_data = HSA.export_hsa_output_df()

    # 6. Explore the output data frame
    st.subheader("Processed DataFrame")
    st.write(hsa_data)
