# Module for data loading, inspection, summarization, and integrity checks in exploratory data analysis.


# importing required libraries
import pandas as pd


class DataSummary:
    """
    Provides methods for basic exploratory data analysis of datasets loaded from file paths.
    Offers functionality to load, inspect, summarize, and check data for integrity and outliers.

    Attributes:
        file_paths (list of str): List of file paths for the data files to be analyzed.

    Methods:
        load_data: Load and concatenate data from file_paths into a single DataFrame.
        inspect_data: Print basic information about the DataFrame's structure.
        summarize_data: Provide summary statistics of numerical columns in the DataFrame.
        check_missing_values: Count missing values in each column of the DataFrame.
        detect_outliers: Identify outliers in the DataFrame using the IQR method.
        validate_data_types_ranges: Check the data types and value ranges of the DataFrame's columns.

    """

    def __init__(self, file_paths):
        """
        Initialize the DataSummary with file paths.

        Parameters:
        file_paths (list of str): List of file paths for the data files.
        """
        self.file_paths = file_paths

    def load_data(self):
        """
        Loads data from the provided file paths and concatenates into a single DataFrame.

        Returns:
        pd.DataFrame: The concatenated DataFrame containing all data.
        """
        data_frames = [pd.read_csv(file) for file in self.file_paths]
        combined_data = pd.concat(data_frames, ignore_index=True)
        return combined_data

    def inspect_data(self, data):
        """
        Inspects the basic structure of the DataFrame.

        Parameters:
        data (pd.DataFrame): The DataFrame to inspect.

        Returns:
        str: Basic information about the DataFrame.
        """
        info = data.info()
        return info

    def summarize_data(self, data):
        """
        Provides summary statistics of the DataFrame's numerical columns.

        Parameters:
        data (pd.DataFrame): The DataFrame to summarize.

        Returns:
        pd.DataFrame: Summary statistics of the DataFrame.
        """
        summary = data.describe()
        return summary

    @staticmethod
    def check_missing_values(data):
        """
        Checks for missing values in each column of the DataFrame.

        Parameters:
        data (pd.DataFrame): The DataFrame to check for missing values.

        Returns:
        pd.Series: A Series displaying the number of missing values in each column.
        """
        missing_values = data.isnull().sum()
        return missing_values

    def detect_outliers(self, data, method="IQR", threshold=1.5):
        """
        Detects outliers in a dataset based on the specified method.

        Parameters:
        data (pd.DataFrame): The dataset in which to find outliers.
        method (str): The method used to detect outliers. Default is 'IQR' for Interquartile Range method.
        threshold (float): The multiplier for IQR to determine the range beyond which data is considered an outlier. Default is 1.5.

        Returns:
        pd.Series: A series indicating the number of outliers for each column.
        """
        if method == "IQR":
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            outliers = (
                (data < (Q1 - threshold * IQR)) | (data > (Q3 + threshold * IQR))
            ).sum()
        return outliers

    def validate_data_types_ranges(self, data, expected_dtypes, expected_ranges):
        """
        Validates the data types and value ranges of the dataset's columns against expected values.

        Parameters:
        data (pd.DataFrame): The dataset to be validated.
        expected_dtypes (dict): A dictionary where keys are column names and values are expected data types.
        expected_ranges (dict): A dictionary where keys are column names and values are tuples indicating the expected minimum and maximum range (inclusive).

        Returns:
        dict: A dictionary with columns as keys and validation results as values, which are dictionaries with keys 'Correct Type' and 'Within Range' indicating the result of validations.
        """
        validation_results = {}
        for col, expected_dtype in expected_dtypes.items():
            validation_results[col] = {
                "Correct Type": data[col].dtype == expected_dtype,
                "Within Range": data[col]
                .apply(
                    lambda x: expected_ranges[col][0] <= x <= expected_ranges[col][1]
                )
                .all(),
            }
        return validation_results
