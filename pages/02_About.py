import streamlit as st

st.set_page_config(
    page_title="About HSA",
    layout="wide",
)

st.write(
    """
## Hot Spot Analysis (HSA)

Hot Spot Analysis (HSA) is an analytic reporting framework designed to identify key drivers behind metric movements by analyzing data cuts across multiple features. This tool enhances reporting, uncovers insights, and simplifies understanding of why metrics shift. It automatically processes all viable combinations within the data, offering a structured output for deeper analysis. Future updates aim to improve speed and functionality. HSA is particularly useful for analysts looking to simplify complex data interactions and trends.


For more details, visit the [Hot Spot Analysis PyPI page](https://pypi.org/project/hot-spot-analysis/) or reach out to Philip Gundy (PhilipGundy@Gmail.com).

"""
)
