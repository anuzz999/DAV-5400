"""Module for fetching and structuring stock data from the Alpha Vantage API  
and then conducting statistical analysis and visualization on stock market data."""


import requests
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose


class StockDataCollector:
    """
    A class for collecting stock data using the Alpha Vantage API.

    This class provides an interface to fetch intraday stock data from the Alpha Vantage API.
    It handles API interactions and structures the data into pandas DataFrames, suitable for
    financial data analysis tasks.

    Attributes:
        api_key (str): API key for Alpha Vantage.
        symbol (str): Stock symbol to fetch data for.
        interval (str): Time interval for stock data, e.g., '5min', '15min' (default '5min').
        base_url (str): Base URL for the Alpha Vantage API.
        params (dict): Parameters for the API request.

    Methods:
        fetch_intraday_data: Fetches intraday stock data from the API.
        get_stock_dataframe: Converts the fetched data into a pandas DataFrame.
    """

    def __init__(self, api_key, symbol, interval="5min"):
        """
        Initializes the StockDataCollector with the API key, stock symbol, and interval.

        Args:
            api_key (str): API key for accessing the Alpha Vantage API.
            symbol (str): The stock symbol for which data is to be fetched.
            interval (str, optional): The time interval for stock data. Defaults to '5min'.
        """
        self.base_url = "https://www.alphavantage.co/query"
        self.api_key = api_key
        self.symbol = symbol
        self.interval = interval
        self.params = self._create_params()

    def _create_params(self):
        """
        Creates the parameters for the API request based on the instance attributes.

        Returns:
            dict: Parameters for the API request.
        """
        return {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": self.symbol,
            "interval": self.interval,
            "apikey": self.api_key,
        }

    def fetch_intraday_data(self):
        """
        Fetches intraday stock data from the Alpha Vantage API.

        This method sends a request to the API and returns the intraday stock data in JSON format.

        Returns:
            dict: Intraday stock data in JSON format, or None if an error occurs.
        """
        try:
            response = requests.get(self.base_url, params=self.params)
            response.raise_for_status()  # This will raise an exception for HTTP error codes
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Print the HTTP error
            print(response.text)  # Print the full response text
        except Exception as err:
            print(f"An error occurred: {err}")  # Print any other errors
        return None

    def get_stock_dataframe(self):
        """
        Converts fetched stock data into a pandas DataFrame.

        This method processes the JSON data returned by the API and structures it into a
        DataFrame, making it suitable for analysis.

        Returns:
            DataFrame: A DataFrame containing stock data, or an empty DataFrame if an error occurs.
        """
        intraday_data = self.fetch_intraday_data()
        if intraday_data:
            time_series_key = next(
                key for key in intraday_data if key.startswith("Time Series")
            )
            time_series_data = intraday_data[time_series_key]
            df = pd.DataFrame.from_dict(time_series_data, orient="index")
            df.columns = ["Open", "High", "Low", "Close", "Volume"]
            df.index = pd.to_datetime(df.index)
            df = df.apply(pd.to_numeric, errors="coerce")
            return df
        else:
            return pd.DataFrame()  # Return an empty DataFrame if there was an error


class StockAnalysis:
    """
    A class for performing various analyses on stock data.

    This class provides methods to load stock data from a CSV file, perform statistical analyses,
    visualize different aspects of the stock data, and decompose the time series.

    Attributes:
        file_path (str): The path to the CSV file containing stock data.
        stock_df (pandas.DataFrame): The DataFrame holding the stock data.

    Methods:
        display_head: Prints the first few rows of the stock data.
        data_info: Displays information and missing values of the stock data.
        statistical_summary: Prints a statistical summary of the stock data.
        plot_close_price: Plots the closing prices of the stock over time.
        plot_volume_distribution: Plots the distribution of the trading volume.
        calculate_daily_returns: Calculates and adds daily returns to the DataFrame.
        calculate_volatility: Calculates and prints the annualized volatility.
        plot_daily_returns: Plots daily returns of the stock.
        decompose_time_series: Decomposes the closing price into trend, seasonality, and residuals.
    """

    def __init__(self, file_path):
        """
        Initializes the StockAnalysis with the path to the stock data CSV file.

        Args:
            file_path (str): The file path to the CSV file containing the stock data.
        """
        self.file_path = file_path
        self.stock_df = pd.read_csv(file_path)

    def display_head(self):
        """
        Displays the first few rows of the stock DataFrame.
        """
        print(self.stock_df.head())

    def data_info(self):
        """
        Prints information about the stock DataFrame including data types and missing values.
        """
        print(self.stock_df.info())
        print(self.stock_df.isnull().sum())

    def statistical_summary(self):
        """
        Prints a statistical summary of the stock DataFrame.
        """
        print(self.stock_df.describe())

    def plot_close_price(self):
        """
        Plots the closing price of the stock over time.
        """
        plt.figure(figsize=(14, 7))
        plt.plot(
            self.stock_df.index,
            self.stock_df["Close"],
            marker="o",
            linestyle="-",
            color="blue",
            label="Close Price",
        )
        plt.title("Intraday Close Price Trend")
        plt.xlabel("Timestamp")
        plt.ylabel("Close Price (USD)")
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_volume_distribution(self):
        """
        Plots the distribution of the trading volume using a boxplot to inspect its distribution and potential outliers.
        """
        plt.figure(figsize=(10, 6))
        plt.boxplot(self.stock_df["Volume"], vert=False)
        plt.title("Volume Distribution")
        plt.xlabel("Volume")
        plt.grid(True)
        plt.show()

    def calculate_daily_returns(self):
        """
        Calculates the daily returns as a percentage change of closing prices and adds it to the DataFrame.
        """
        self.stock_df["Daily_Returns"] = self.stock_df["Close"].pct_change()

    def calculate_volatility(self):
        """
        Calculates and prints the annualized volatility of the stock.
        """
        volatility = self.stock_df["Daily_Returns"].std() * np.sqrt(252)
        print(f"The annualized volatility is: {volatility:.2%}")

    def plot_daily_returns(self):
        """
        Plots the daily returns of the stock.
        """
        plt.figure(figsize=(14, 7))
        plt.plot(
            self.stock_df.index,
            self.stock_df["Daily_Returns"],
            label="Daily Returns",
            color="orange",
        )
        plt.title("Daily Returns of the Stock")
        plt.xlabel("Time")
        plt.ylabel("Daily Returns (%)")
        plt.legend()
        plt.show()

    def decompose_time_series(self):
        """
        Decomposes the closing price time series into its trend, seasonal, and residual components using an additive model.
        """
        decomposition = seasonal_decompose(
            self.stock_df["Close"], model="additive", period=1
        )
        fig = decomposition.plot()
        fig.set_size_inches(14, 7)
        plt.show()
