import pandas as pd
import seaborn as sns


class DatasetManager:
    def __init__(self):
        self.available_datasets = ["tips", "titanic"]

    def load_dataset(self, name: str) -> pd.DataFrame:
        if name == "tips":
            df_tips = sns.load_dataset("tips")
            df_tips["tip_perc"] = df_tips["tip"] / df_tips["total_bill"]
            df_tips["overall"] = "overall"
            return df_tips
        elif name == "titanic":
            df_titanic = sns.load_dataset("titanic")
            df_titanic["overall"] = "overall"
            return df_titanic
        else:
            raise ValueError(f"Dataset {name} is not available.")

    def dataset_agg_func(self, name: str, df: pd.DataFrame) -> pd.DataFrame:
        if name == "tips":
            return self.aggregate_tips(df)
        elif name == "titanic":
            return self.aggregate_titanic(df)
        else:
            raise ValueError(f"Dataset {name} does not have an aggregation function.")

    def aggregate_tips(self, df: pd.DataFrame) -> pd.DataFrame:
        """fake"""
        tips_agg = df.agg(
            avg_tips=pd.NamedAgg("tip", "mean"),
            avg_tip_perc=pd.NamedAgg("tip_perc", "mean"),
        ).round(2)

        return tips_agg

    def aggregate_titanic(self, df: pd.DataFrame) -> pd.DataFrame:
        survival_rate = df.agg(
            survivors=pd.NamedAgg("survived", "sum"),
            survival_rate=pd.NamedAgg("survived", "mean"),
        ).round(4)
        return survival_rate


# Create a single instance of the DatasetManager
dataset_manager = DatasetManager()
