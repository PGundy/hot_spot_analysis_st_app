# %%
import inspect

import pandas as pd
import seaborn as sns
import streamlit as st
from hot_spot_analysis.hot_spot_analysis import HotSpotAnalyzer


def aggregate_tips(df: pd.DataFrame) -> pd.DataFrame:
    tips_agg = df.agg(
        avg_tips=pd.NamedAgg("tip", "mean"),
        avg_tip_perc=pd.NamedAgg("tip_perc", "mean"),
    ).round(2)

    return tips_agg


def aggregate_titanic(df: pd.DataFrame) -> pd.DataFrame:
    survival_rate = df.agg(
        survivors=pd.NamedAgg("survived", "sum"),
        survival_rate=pd.NamedAgg("survived", "mean"),
    ).round(4)
    return survival_rate


class DatasetManager:
    def __init__(self):
        self.available_datasets = ["tips", "titanic"]
        self.aggregate_tips = aggregate_tips
        self.aggregate_titanic = aggregate_titanic

    def load_dataset(self, name: str) -> pd.DataFrame:
        if name == "tips":
            df_tips = sns.load_dataset("tips")
            df_tips["tip_perc"] = df_tips["tip"] / df_tips["total_bill"]
            df_tips["overall"] = "overall"
            return df_tips
        elif name == "titanic":
            df_titanic = sns.load_dataset("titanic")
            subset_columns = ["survived", "class", "sex", "deck", "embark_town", "alone"]
            df_titanic = df_titanic[subset_columns]
            df_titanic["overall"] = "overall"
            return df_titanic
        else:
            raise ValueError(f"Dataset {name} is not available.")

    def get_agg_function(self, name: str) -> callable:
        """
        Return an python function meant to aggregate a pandas data frame
        """
        if name == "tips":
            return self.aggregate_tips
        elif name == "titanic":
            return self.aggregate_titanic
        else:
            raise ValueError(f"Dataset {name} does not have an aggregation function.")


dataset_manager = DatasetManager()

st.set_page_config(page_title="Hot Spot Analysis Demo", page_icon="🔍", layout="wide")


st.header("Hot Spot Analysis Demo")
st.markdown(
    """
    This app has 2 interactive demos of Hot Spot Analysis (HSA). Click around, and see how the output changes by changing parameters! 
    
    The code shown in the app is the same code that the app is using to generate the shown dataframes.
    """
)

st.markdown("***")
col1, col2 = st.columns(2, vertical_alignment="center")
with col1:
    available_datasets = dataset_manager.available_datasets
    st_dataset_name = str(st.selectbox("Select a dataset", available_datasets, index=0))

    # Load the selected dataset & objective function
    st_df: pd.DataFrame = dataset_manager.load_dataset(st_dataset_name)

    # NOTE: Extract the function, then define it as a function. This let's us print the agg function.
    agg_function_var: callable = dataset_manager.get_agg_function(name=st_dataset_name)

    def agg_function(df: pd.DataFrame) -> pd.DataFrame:
        return agg_function_var(df)

    # 1. View the dataset, and see the out put of the related aggregation function
    st.text("Preview the raw data")
    st.dataframe(st_df.head(5))

with col2:
    # 2. See the output of the objective function
    st.text("Below is our aggregation function:")
    code, line_no = inspect.getsourcelines(agg_function_var)
    st.code("".join(code))

    st.text("Aggregation function output when grouped by 'overall':")
    st.write(agg_function(st_df.groupby("overall")))  # type: ignore


st.markdown("***")
st.subheader(f"Pick features & interaction limit for HotSpotAnalysis")
col3, col4 = st.columns(2, vertical_alignment="center")

interactable_columns = list(st_df.select_dtypes(include=["category", "object"]).columns)
interactable_columns = [x for x in interactable_columns if x != "overall"]

with col3:
    # 3. Select at least 2 columns
    hsa_features = st.multiselect(
        """Select 2 or more columns for the demo! 
        There can be a delay if all are selected.
        """,
        options=interactable_columns,
        default=interactable_columns,
    )
    if len(hsa_features) < 2:
        st.error("Please select at least 2 columns.")

    # 4. Select an interaction limit
    interaction_max = len(interactable_columns) + 1
    interaction_selection = st.radio(
        "Select an interaction limit:",
        # value=interaction_max,
        horizontal=True,
        options=reversed(range(2, interaction_max)),
    )

with col4:
    st.code(
        f"""
        # Setup the HSA class & define parameters
        HSA = HotSpotAnalyzer(
            data=df_{st_dataset_name},
            target_cols={hsa_features},
            interaction_limit={interaction_selection},
            objective_function={agg_function_var.__name__}, # callable function 
            )
        
        # Run HSA, then export HSA
        HSA.run_hsa()
        HSA.export_hsa_output_df()
        """
    )


# Save selections to session state & run HSA
if st.button("Run HSA"):  #!!, type="primary"):

    st.session_state["st_dataset_name"] = st_dataset_name
    st.session_state["st_df"] = st_df
    st.session_state["hsa_features"] = hsa_features
    st.session_state["interaction_max"] = interaction_max

    st.title("Hot Spot Analysis")

    HSA = HotSpotAnalyzer(
        data=st.session_state["st_df"],
        target_cols=st.session_state["hsa_features"],
        interaction_limit=st.session_state["interaction_max"],
        objective_function=agg_function,
    )
    st.session_state["HSA"] = HSA

    # 5. Process the DataFrame using the custom module
    HSA.run_hsa()
    hsa_data = HSA.export_hsa_output_df()
    st.session_state["hsa_data"] = hsa_data
    st.session_state["hsa_ran"] = True


if st.session_state.get("hsa_ran", False):
    if st_dataset_name != st.session_state["st_dataset_name"]:
        st.warning("Please re-run HSA. The dataset has been changed.")
        st.stop()

    st.subheader("HSA Data Output")
    st.dataframe(st.session_state["hsa_data"], use_container_width=True)

    st.markdown("***")
    st.subheader("Search across HSA Data")

    col1, col2 = st.columns(2, vertical_alignment="center")
    with col1:
        col1_label = "Search for specific columns or values"
        st.markdown(col1_label)
        search_across_dict = {"columns (keys)": "keys", "values": "values"}
        search_across = st.selectbox(
            col1_label,
            label_visibility="collapsed",
            options=search_across_dict.keys(),
        )
        st.session_state["search_across"] = str(search_across_dict.get(search_across))  # type: ignore

        ## define input for 'search_terms'
        col2_label = "Select search terms"
        st.markdown(col2_label)
        combo_values = [list(x.values()) for x in st.session_state["hsa_data"].combo_dict]

        def get_unique_values(list_of_lists):
            unique_values = set()
            for sublist in list_of_lists:
                unique_values.update(sublist)
            return list(unique_values)

        search_term_map = {
            "keys": st.session_state["hsa_features"],
            "values": [str(x) for x in get_unique_values(combo_values)],
        }
        search_term_options = search_term_map.get(st.session_state["search_across"])  # type: ignore
        search_term_options = ["Overall"] + list(search_term_options)  # type: ignore

        search_terms = st.multiselect(
            col2_label,
            options=search_term_options,
            default=search_term_options[1:3],
            label_visibility="collapsed",
        )  # type: ignore
        st.session_state["search_terms"] = search_terms

        col3_label = "Search type: Any matches or All must match"
        st.markdown(col3_label)
        ## define input for 'search_type'
        search_type_options = ["any", "all"]
        st.session_state["search_type"] = st.selectbox(
            col3_label,
            options=search_type_options,
            index=0,
            label_visibility="collapsed",
            help="Should we return results for any matches or require all terms to appear?",
        )

        col4_label = "Select the number of desired interactions"
        st.markdown(col4_label)

        interactions = list(st.session_state["hsa_data"].interaction_count.unique())
        interactions = [int(x) for x in interactions]

        interaction_options = interactions
        st.session_state["interactions"] = st.multiselect(
            col4_label,
            options=interaction_options,
            default=[0, 1, 2, 3],
            label_visibility="collapsed",
        )

        col5_label = "Set a minimum number of rows/observations"
        st.markdown(col5_label)
        n_rows = st.session_state["hsa_data"].n_rows.unique()

        st.session_state["n_row_minimum"] = st.number_input(
            col5_label,
            min_value=0,
            max_value=n_rows.max(),
            label_visibility="collapsed",
        )

    with col2:
        st.code(
            f"""
            HSA.search_hsa_output(
                hsa_df={st.session_state["st_dataset_name"]}_hsa_output, # Optional, defaults to full HSA data
                search_across="{st.session_state["search_across"]}",
                search_terms={st.session_state["search_terms"]},
                search_type="{st.session_state["search_type"]}",
                interactions={st.session_state["interactions"]},
                n_row_minimum = {st.session_state["n_row_minimum"]},
            )
            
            # See output below
                """
        )

    st.markdown("***")
    HSA = st.session_state["HSA"]

    search_results = HSA.search_hsa_output(
        hsa_df=st.session_state["hsa_data"],
        search_across=st.session_state["search_across"],
        search_terms=st.session_state["search_terms"],
        search_type=st.session_state["search_type"],
        interactions=st.session_state["interactions"],
        n_row_minimum=st.session_state["n_row_minimum"],
    )
    st.dataframe(search_results, use_container_width=True)
