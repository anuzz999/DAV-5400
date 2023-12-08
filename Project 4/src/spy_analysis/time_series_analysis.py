import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


class TimeSeriesAnalysis:
    """
    Handles time series analysis tasks, including stationarity tests.
    """

    def __init__(self, data):
        """
        Initializes the TimeSeriesAnalysis with the dataset.

        Parameters:
        - data (DataFrame): The pandas DataFrame containing the time series data.
        """
        self.data = data

    def perform_adf_test(self, series_name, subset_size=None):
        """
        Performs the Augmented Dickey-Fuller test on a specified time series.

        Parameters:
        - series_name (str): The name of the column containing the time series data.
        - subset_size (int, optional): Number of recent data points to include in the test.

        Returns:
        - Series: A pandas Series with the ADF test results.
        """
        series = self.data[series_name]
        if subset_size is not None:
            series = series.iloc[-subset_size:]

        adf_test = adfuller(series)
        adf_output = pd.Series(
            adf_test[0:4],
            index=[
                "Test Statistic",
                "p-value",
                "#Lags Used",
                "Number of Observations Used",
            ],
        )
        for key, value in adf_test[4].items():
            adf_output["Critical Value (%s)" % key] = value
        return adf_output

    def decompose_time_series(self, series_name, model="additive", period=1):
        """
        Decomposes a time series into its trend, seasonal, and residual components.

        Parameters:
        - series_name (str): The name of the column containing the time series data.
        - model (str): Type of decomposition model ('additive' or 'multiplicative').
        - period (int): The period of the time series.

        Returns:
        - DecomposeResult: The decomposed time series components.
        """
        sns.set(style="whitegrid")
        series = self.data[series_name]
        decomposition = seasonal_decompose(series, model=model, period=period)

        # Plot the decomposed components
        fig = decomposition.plot()
        fig.set_size_inches(14, 7)
        plt.tight_layout()
        plt.show()
        return decomposition

    def plot_acf_pacf(self, series_name, lags=20):
        """
        Plots the Autocorrelation and Partial Autocorrelation Functions.

        Parameters:
        - series_name (str): The name of the column containing the time series data.
        - lags (int): Number of lags to include in the plots.
        """
        series = self.data[series_name]
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4))
        plot_acf(series, lags=lags, ax=ax1)
        plot_pacf(series, lags=lags, ax=ax2)
        plt.show()

    def fit_arima(self, series_name, order):
        """
        Fits an ARIMA model to the time series.

        Parameters:
        - series_name (str): The name of the column containing the time series data.
        - order (tuple): The order (p, d, q) of the ARIMA model.

        Returns:
        - ARIMAResultsWrapper: The fitted ARIMA model.
        """
        series = self.data[series_name]
        arima_model = ARIMA(series, order=order)
        arima_result = arima_model.fit()
        return arima_result

    def plot_residuals(self, model_result, lags=20, zoom_range=None):
        """
        Plots the residuals of a fitted time series model and their autocorrelation.

        Parameters:
        - model_result: The result of the fitted time series model.
        - lags (int): Number of lags to include in the ACF plot.
        - zoom_range (tuple, optional): Range (min, max) to zoom in on the residuals density plot.
        """
        residuals = pd.DataFrame(model_result.resid)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4))

        # Plot residual errors
        sns.histplot(residuals, kde=True, ax=ax1)
        ax1.set_title("Residuals Density Plot")

        # Plot ACF of residuals
        plot_acf(residuals, lags=lags, ax=ax2)
        ax2.set_title("ACF of Residuals")

        plt.show()

        # Plotting the residuals density plot with a limited x-axis if zoom_range is provided
        if zoom_range:
            plt.figure(figsize=(10, 6))
            sns.histplot(residuals, kde=True)
            plt.xlim(zoom_range)  # Setting the x-axis limits based on zoom_range
            plt.title("Residuals Density Plot Zoomed In")
            plt.xlabel("Residuals")
            plt.ylabel("Density")
            plt.show()
