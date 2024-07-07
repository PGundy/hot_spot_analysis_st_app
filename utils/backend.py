import pandas as pd
import seaborn as sns


class DatasetManager:
    def __init__(self):
        self.available_datasets = ["tips", "titanic"]

    def load_dataset(self, name: str) -> pd.DataFrame:
        if name == "tips":
            df_tips = sns.load_dataset("tips")
            df_tips["tip_perc"] = df_tips["tip"] / df_tips["total_bill"]
            return df_tips
        elif name == "titanic":
            return sns.load_dataset("titanic")
        else:
            raise ValueError(f"Dataset {name} is not available.")

    def agg_func(self, name: str, df: pd.DataFrame) -> pd.DataFrame:
        if name == "tips":
            return self.aggregate_tips(df)
        elif name == "titanic":
            return self.aggregate_titanic(df)
        else:
            raise ValueError(f"Dataset {name} does not have an aggregation function.")

    def aggregate_tips(self, df: pd.DataFrame) -> pd.DataFrame:
        """fake"""
        tmp = df.agg(
            avg_tips=pd.NamedAgg("tip", "mean"),
            avg_tip_perc=pd.NamedAgg("tip_perc", "mean"),
        ).round(2)

        return tmp

    def aggregate_titanic(self, df: pd.DataFrame) -> pd.DataFrame:
        survival_rate = df.groupby("class")["survived"].mean().reset_index()
        survival_rate.rename(columns={"survived": "survival_rate"}, inplace=True)
        return survival_rate


# Create a single instance of the DatasetManager
dataset_manager = DatasetManager()
