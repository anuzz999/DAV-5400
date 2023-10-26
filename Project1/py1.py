import pandas as pd

class DataLoader:
    """
    A class used to load data from a file.

    ...

    Attributes
    ----------
    file_path : str
        a string indicating the path to the data file

    Methods
    -------
    load_sample_data(rows=5)
        Loads a sample of the data from the file to inspect its structure.
    """

    def __init__(self, file_path):
        """
        Parameters
        ----------
        file_path : str
            The file path of the data file to load.
        """
        self.file_path = file_path

    def load_sample_data(self, rows=5, delimiter="\t"):
        """
        Loads a sample of the data from the file to inspect its structure.

        Parameters
        ----------
        rows : int, optional
            Number of rows to load from the file (default is 5)
        delimiter : str, optional
            Delimiter to use (default is tab)

        Returns
        -------
        DataFrame
            A DataFrame containing the loaded sample data.
        """
        try:
            sample_data = pd.read_csv(self.file_path, delimiter=delimiter, nrows=rows)
            return sample_data
        except FileNotFoundError:
            return "The file was not found in the specified path."
        
    
    def clean_column_names(data):
        """
        Cleans the column names by removing square brackets.

        Parameters
        ----------
        data : DataFrame
            The DataFrame whose column names need to be cleaned.

        Returns
        -------
        DataFrame
            A DataFrame with cleaned column names.
        """
        data.columns = data.columns.str.replace('[', '').str.replace(']', '')
        return data
    
    def load_and_concatenate_files(file_paths, delimiter=","):
        """
        Loads and concatenates data from multiple files into a single DataFrame.

        Parameters
        ----------
        file_paths : list of str
            A list of file paths to load and concatenate.
        delimiter : str, optional
            The delimiter used in the data files (default is comma).

        Returns
        -------
        DataFrame
            A DataFrame containing concatenated data from all files.
        """
        all_data = pd.concat((pd.read_csv(file, delimiter=delimiter) for file in file_paths), ignore_index=True)
        return all_data
    
    @staticmethod
    def clean_leading_spaces_in_columns(data):
        """
        Cleans leading spaces from column names.

        Parameters
        ----------
        data : DataFrame
            The DataFrame whose column names need to be cleaned.

        Returns
        -------
        DataFrame
            A DataFrame with cleaned column names.
        """
        data.columns = data.columns.str.strip()
        return data

    @staticmethod
    def select_columns(data, columns_to_keep):
        """
        Selects specific columns from the DataFrame.

        Parameters
        ----------
        data : DataFrame
            The DataFrame from which columns are to be selected.
        columns_to_keep : list of str
            A list of column names to keep.

        Returns
        -------
        DataFrame
            A DataFrame containing only the selected columns.
        """
        return data[columns_to_keep].copy()


    def check_missing_values(data):
        """
        Checks for missing values in each column of the DataFrame.

        Parameters
        ----------
        data : DataFrame
            The DataFrame to check for missing values.

        Returns
        -------
        Series
            A Series displaying the number of missing values in each column.
        """
        return data.isnull().sum()
    
    @staticmethod
    def convert_to_datetime(data, columns):
        """
        Converts specified columns in the DataFrame to datetime data type.

        Parameters
        ----------
        data : DataFrame
            The DataFrame in which columns need data type conversion.
        columns : list of str
            A list of column names to be converted to datetime data type.

        Returns
        -------
        DataFrame
            A DataFrame with specified columns converted to datetime data type.
        """
        for column in columns:
            data[column] = pd.to_datetime(data[column])
        return data
    
    def get_unique_values(data, columns):
        """
        Gets unique values from specified columns of the DataFrame.

        Parameters
        ----------
        data : DataFrame
            The DataFrame from which unique values are to be retrieved.
        columns : list of str
            A list of column names from which unique values are to be found.

        Returns
        -------
        dict
            A dictionary where keys are column names and values are arrays of unique values.
        """
        unique_values = {column: data[column].unique() for column in columns}
        return unique_values
    
    @staticmethod
    def convert_to_numeric(data, columns, errors='coerce'):
        """
        Converts specified columns in the DataFrame to numeric data type.

        Parameters
        ----------
        data : DataFrame
            The DataFrame in which columns need data type conversion.
        columns : list of str
            A list of column names to be converted to numeric data type.
        errors : str, optional
            If 'coerce', then invalid parsing will be set as NaN (default is 'coerce').

        Returns
        -------
        DataFrame
            A DataFrame with specified columns converted to numeric data type.
        """
        for column in columns:
            data[column] = pd.to_numeric(data[column], errors=errors)
        return data
    
    def remove_na_rows(data, columns):
        """
        Removes rows from the DataFrame where specified columns have NaN values.

        Parameters
        ----------
        data : DataFrame
            The DataFrame from which rows are to be removed.
        columns : list of str
            A list of column names to check for NaN values.

        Returns
        -------
        DataFrame
            A DataFrame with rows containing NaN values in specified columns removed.
        """
        return data.dropna(subset=columns)
    
    @staticmethod
    def display_basic_info(data):
        """
        Displays basic information about the DataFrame.

        Parameters
        ----------
        data : DataFrame
            The DataFrame for which basic information is to be displayed.
        """
        return data.info()

    @staticmethod
    def display_statistical_summary(data):
        """
        Displays statistical summary for numerical columns in the DataFrame.

        Parameters
        ----------
        data : DataFrame
            The DataFrame for which statistical summary is to be displayed.

        Returns
        -------
        DataFrame
            A DataFrame containing statistical summary for numerical columns.
        """
        return data.describe()

    @staticmethod
    def display_unique_values(data, columns):
        """
        Displays the number of unique values for specified columns.

        Parameters
        ----------
        data : DataFrame
            The DataFrame from which unique values are to be found.
        columns : list of str
            A list of column names for which unique values are to be displayed.

        Returns
        -------
        dict
            A dictionary where keys are column names and values are counts of unique values.
        """
        unique_counts = {column: len(data[column].unique()) for column in columns}
        return unique_counts
    
    @staticmethod
    def save_to_csv(data, file_path, index=False):
        """
        Saves the DataFrame to a CSV file.

        Parameters
        ----------
        data : DataFrame
            The DataFrame to be saved.
        file_path : str
            The path where the CSV file will be saved.
        index : bool, optional
            Whether to write row (index) names (default is False).
        """
        data.to_csv(file_path, index=index)