import pandas as pd


class DataCleaning:
    """
    Handles the cleaning and preprocessing of SPY options data.
    """

    def __init__(self, data):
        """
        Initializes the DataCleaning with the SPY options dataset.

        Parameters:
        - data (DataFrame): The pandas DataFrame with the SPY options data.
        """
        self.data = data

    def convert_dates(self, date_columns):
        """
        Converts columns with date information into datetime objects.

        Parameters:
        - date_columns (list of str): List of column names to be converted.
        """
        for col in date_columns:
            self.data[col] = pd.to_datetime(self.data[col])

    def check_missing_values(self):
        """
        Checks for missing values in the dataset.

        Returns:
        - Series: A pandas Series with the count of missing values per column.
        """
        return self.data.isnull().sum()

    def check_outliers(self, columns):
        """
        Checks for potential outliers in the specified columns.

        Parameters:
        - columns (list of str): List of column names to check for outliers.

        Returns:
        - DataFrame: Descriptive statistics that can help identify outliers.
        """
        return self.data[columns].describe()
