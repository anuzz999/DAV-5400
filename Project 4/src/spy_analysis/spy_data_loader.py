import pandas as pd


class DataLoader:
    """
    DataLoader is responsible for loading and providing an initial look at the data.
    """

    def __init__(self, file_path):
        """
        Initializes the DataLoader with the file path of the data.

        Parameters:
        - file_path (str): The path to the CSV file containing the data.
        """
        self.file_path = file_path

    def load_data(self):
        """
        Loads the data from the CSV file.

        Returns:
        - DataFrame: The loaded data as a pandas DataFrame.
        """
        return pd.read_csv(self.file_path)

    def display_head(self, data):
        """
        Displays the first few rows of the DataFrame.

        Parameters:
        - data (DataFrame): The pandas DataFrame to display.

        Returns:
        - DataFrame: The first few rows of the DataFrame.
        """
        return data.head()

    def display_info(self, data):
        """
        Displays information about the DataFrame.

        Parameters:
        - data (DataFrame): The pandas DataFrame to display information about.

        Returns:
        - None
        """
        return data.info()

    def display_description(self, data):
        """
        Displays basic statistics about the DataFrame.

        Parameters:
        - data (DataFrame): The pandas DataFrame to display statistics about.

        Returns:
        - DataFrame: The basic statistics of the DataFrame.
        """
        return data.describe()

    def convert_dates_and_set_index(self, date_column, data):
        """
        Converts a specified column to datetime and sets it as the index of the DataFrame.

        Parameters:
        - date_column (str): The name of the column to convert and set as index.
        - data (DataFrame): The pandas DataFrame to modify.

        Returns:
        - DataFrame: The modified DataFrame with the specified column as datetime index.
        """
        data[date_column] = pd.to_datetime(data[date_column])
        data.set_index(date_column, inplace=True)
        return data
