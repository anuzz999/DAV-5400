import pandas as pd
import numpy as np


class FeatureEngineering:
    """
    Handles feature engineering tasks for the SPY options dataset.
    """

    def __init__(self, data):
        """
        Initializes the FeatureEngineering with the dataset.

        Parameters:
        - data (DataFrame): The pandas DataFrame containing the options data.
        """
        self.data = data

    def calculate_decay_features(self):
        """
        Calculates the daily changes in option prices and additional decay features.

        Returns:
        - DataFrame: The modified DataFrame with new features.
        """
        self.data["C_LAST_CHANGE"] = (
            self.data.groupby(["STRIKE", "EXPIRE_DATE"])["C_LAST"].diff().fillna(0)
        )
        self.data["C_LAST_PREV"] = self.data.groupby(["STRIKE", "EXPIRE_DATE"])[
            "C_LAST"
        ].shift(1)
        self.data.dropna(subset=["C_LAST_PREV"], inplace=True)
        self.data["DECAY_RATE"] = self.data["C_LAST_CHANGE"] / self.data["C_LAST_PREV"]
        self.data.replace([np.inf, -np.inf], np.nan, inplace=True)
        self.data.dropna(inplace=True)
        return self.data
