import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Home",
    page_icon="👋",
)

st.markdown(
    """
    TODO: Add overview & explination of HSA
    """
)

if st.button("Go to Hot Spot Analysis", type="primary"):
    switch_page("Hot_Spot_Analysis_Demo")
