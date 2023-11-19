import requests
import pandas as pd


class StockDataCollector:
    """
    A class to collect stock data using the Alpha Vantage API.

    Attributes:
    api_key (str): API key for Alpha Vantage.
    symbol (str): Stock symbol to fetch data for.
    interval (str): Time interval for stock data (default is '5min').
    """

    def __init__(self, api_key, symbol, interval="5min"):
        """
        Initialize the StockDataCollector with the API key, stock symbol, and interval.
        """
        self.base_url = "https://www.alphavantage.co/query"
        self.api_key = api_key
        self.symbol = symbol
        self.interval = interval
        self.params = self._create_params()

    def _create_params(self):
        """
        Create the parameters for the API request.
        """
        return {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": self.symbol,
            "interval": self.interval,
            "apikey": self.api_key,
        }

    def fetch_intraday_data(self):
        try:
            response = requests.get(self.base_url, params=self.params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching data: {response.status_code}")
                print(response.json())  # This will show the full error response
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request exception: {e}")
            return None

    def get_stock_dataframe(self):
        """
        Converts fetched stock data into a pandas DataFrame.

        Returns:
        DataFrame: DataFrame containing stock data, or empty if an error occurs.
        """
        intraday_data = self.fetch_intraday_data()
        if intraday_data:
            time_series_key = next(
                (key for key in intraday_data if key.startswith("Time Series")), None
            )
            if time_series_key:
                time_series_data = intraday_data[time_series_key]
                df = pd.DataFrame.from_dict(time_series_data, orient="index")
                df.columns = ["Open", "High", "Low", "Close", "Volume"]
                df.index = pd.to_datetime(df.index)
                df = df.apply(pd.to_numeric, errors="coerce")
                return df
            else:
                print("Time series data not found in the response.")
                return pd.DataFrame()
        else:
            print("Failed to fetch or parse intraday data.")
            return pd.DataFrame()
