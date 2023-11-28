import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from pandas.plotting import scatter_matrix


class Inference:
    """
    A class for performing various inference analyses on options data.

    Methods
    -------
    correlation_analysis(data):
        Performs correlation analysis on the given data.

    multivariate_analysis(data):
        Performs multivariate analysis on selected variables.

    temporal_analysis(data):
        Plots temporal trends in the data.
    """

    def __init__(self, data):
        """
        Initializes the Inference object with options data.

        Parameters:
        data (DataFrame): The options data for analysis.
        """
        self.data = data

    @staticmethod
    def correlation_analysis(data):
        """
        Perform correlation analysis on the given data.

        Parameters:
        data (DataFrame): The options data for analysis.

        Returns:
        None: Plots the correlation heatmap.
        """
        correlation_matrix = self.data.corr()

        plt.figure(figsize=(12, 10))
        sns.heatmap(correlation_matrix, annot=False, cmap="coolwarm")
        plt.title("Correlation Heatmap of Option Chain Data Variables")
        plt.show()

    @staticmethod
    def multivariate_analysis(data):
        """
        Perform multivariate analysis on selected variables.

        Parameters:
        data (DataFrame): The options data for analysis.

        Returns:
        None: Plots a multivariate scatter plot.
        """
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            data=self.data,
            x="DTE",
            y="C_IV",
            hue="UNDERLYING_LAST",
            size="C_DELTA",
            sizes=(20, 200),
        )
        plt.title(
            "Multivariate Scatter Plot: DTE vs C_IV with UNDERLYING_LAST and C_DELTA"
        )
        plt.legend(
            title="UNDERLYING_LAST & C_DELTA",
            loc="upper right",
            bbox_to_anchor=(1.25, 1),
        )
        plt.show()

    @staticmethod
    def temporal_analysis(data):
        """
        Plot temporal trends in the data.

        Parameters:
        data (DataFrame): The options data for analysis.

        Returns:
        None: Plots a line chart showing trends over time.
        """
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=self.data, x="QUOTE_DATE", y="C_IV")
        plt.title("Temporal Trend of Call Implied Volatility (C_IV) Over Time")
        plt.xticks(rotation=45)
        plt.show()

    def histogram_underlying_last(self):
        """
        Creates a histogram of UNDERLYING_LAST using Matplotlib.
        """
        plt.figure(figsize=(10, 6))
        plt.hist(
            self.data["UNDERLYING_LAST"], bins=30, color="skyblue", edgecolor="black"
        )
        plt.title("Histogram of Underlying Asset Last Price (SPY)")
        plt.xlabel("Underlying Last Price")
        plt.ylabel("Frequency")
        plt.show()

    def scatterplot_dte_c_iv(self):
        """
        Creates a scatter plot of DTE vs C_IV using Matplotlib.
        """
        plt.figure(figsize=(10, 6))
        plt.scatter(
            self.data["DTE"],
            self.data["C_IV"],
            c=self.data["UNDERLYING_LAST"],
            cmap="viridis",
        )
        plt.colorbar(label="Underlying Last Price")
        plt.title("Scatter Plot: DTE vs C_IV with UNDERLYING_LAST")
        plt.xlabel("Days to Expiry (DTE)")
        plt.ylabel("Call Implied Volatility (C_IV)")
        plt.show()

    def lineplot_c_iv_over_time(self):
        """
        Creates a line plot of C_IV over time using Matplotlib.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(self.data["QUOTE_DATE"], self.data["C_IV"], color="orange")
        plt.title("Temporal Trend of Call Implied Volatility (C_IV) Over Time")
        plt.xlabel("Date")
        plt.ylabel("Call Implied Volatility (C_IV)")
        plt.xticks(rotation=45)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=10))
        plt.show()

    def weekly_aggregation_analysis(self):
        """
        Performs weekly aggregation of implied volatility and Greeks, and plots the results.
        """
        self.data["Week"] = self.data["QUOTE_DATE"].dt.isocalendar().week
        weekly_agg = self.data.groupby("Week").agg({"C_IV": "mean", "C_DELTA": "mean"})

        plt.figure(figsize=(12, 6))
        plt.plot(
            weekly_agg.index, weekly_agg["C_IV"], label="Average Call IV", marker="o"
        )
        plt.plot(
            weekly_agg.index,
            weekly_agg["C_DELTA"],
            label="Average Call Delta",
            marker="x",
        )
        plt.title("Weekly Aggregated Call Implied Volatility and Delta")
        plt.xlabel("Week Number")
        plt.ylabel("Average Value")
        plt.legend()
        plt.grid(True)
        plt.show()

    def expiration_grouping_analysis(self):
        """
        Groups data by expiration dates, analyzes variations in IV, and plots the results.
        """
        expiration_grouped = self.data.groupby("EXPIRE_DATE").agg(
            {"C_IV": "mean", "P_IV": "mean"}
        )

        plt.figure(figsize=(12, 6))
        plt.bar(
            expiration_grouped.index,
            expiration_grouped["C_IV"],
            label="Average Call IV",
            alpha=0.7,
        )
        plt.bar(
            expiration_grouped.index,
            expiration_grouped["P_IV"],
            label="Average Put IV",
            alpha=0.7,
        )
        plt.title("Average Implied Volatility Grouped by Expiration Date")
        plt.xlabel("Expiration Date")
        plt.ylabel("Average Implied Volatility")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)
        plt.show()

    def hexbin_plot(self):
        """
        Creates a hexbin plot of option delta vs. option prices.
        """
        np.random.seed(0)
        sample_delta = np.random.normal(0, 0.1, 1000)
        sample_option_prices = np.random.normal(100, 20, 1000)

        plt.figure(figsize=(10, 6))
        plt.hexbin(
            sample_delta, sample_option_prices, gridsize=50, cmap="Blues", alpha=0.8
        )
        plt.colorbar(label="Count in Bin")
        plt.title("Hexbin Plot: Option Delta vs. Option Prices")
        plt.xlabel("Option Delta")
        plt.ylabel("Option Prices")
        plt.show()

    def seaborn_jointplot(self):
        """
        Creates a Seaborn jointplot of option delta vs. option prices.
        """
        np.random.seed(0)
        sample_delta = np.random.normal(0, 0.1, 1000)
        sample_option_prices = np.random.normal(100, 20, 1000)

        sns.jointplot(
            x=sample_delta, y=sample_option_prices, kind="hex", color="green", space=0
        )
        plt.xlabel("Option Delta")
        plt.ylabel("Option Prices")
        plt.suptitle(
            "Seaborn Jointplot: Option Delta vs. Option Prices",
            verticalalignment="top",
            y=1.02,
        )
        plt.show()

    def linear_regression_analysis(self):
        """
        Performs linear regression to predict 'C_LAST' using 'C_IV' and 'C_DELTA'.
        Includes visualization and model evaluation.
        """
        filtered_data = (
            self.data[["C_LAST", "C_IV", "C_DELTA"]]
            .replace([np.inf, -np.inf], np.nan)
            .dropna()
        )

        X = filtered_data[["C_IV", "C_DELTA"]]
        y = filtered_data["C_LAST"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = LinearRegression()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # Matplotlib Visualization
        plt.figure(figsize=(10, 6))
        plt.scatter(y_test, y_pred, alpha=0.5)
        plt.title("Actual vs. Predicted Option Prices (Matplotlib)")
        plt.xlabel("Actual Prices")
        plt.ylabel("Predicted Prices")
        plt.plot(
            [y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "k--", lw=2
        )
        plt.show()

        # Seaborn Visualization
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=y_test, y=y_pred, alpha=0.5)
        plt.title("Actual vs. Predicted Option Prices (Seaborn)")
        plt.xlabel("Actual Prices")
        plt.ylabel("Predicted Prices")
        plt.plot(
            [y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "k--", lw=2
        )
        plt.show()

        return mse, r2

    def scatter_matrix_visualization(self, columns, sample_size=10000):
        """
        Creates a scatter matrix for the specified columns in the data.

        Parameters:
        columns (list): List of column names to include in the scatter matrix.
        sample_size (int): Number of samples to take from the data (default is 10000).
        """
        if sample_size:
            sampled_data = self.data[columns].sample(n=sample_size, random_state=42)
        else:
            sampled_data = self.data[columns]

        scatter_matrix(sampled_data, alpha=0.5, figsize=(12, 12), diagonal="kde")
        plt.show()

    def pairplot_visualization(self, columns, sample_size=10000):
        """
        Creates a pairplot for the specified columns in the data.

        Parameters:
        columns (list): List of column names to include in the pairplot.
        sample_size (int): Number of samples to take from the data (default is 10000).
        """
        if sample_size:
            sampled_data = self.data[columns].sample(n=sample_size, random_state=42)
        else:
            sampled_data = self.data[columns]

        sns.pairplot(sampled_data, diag_kind="kde", plot_kws={"alpha": 0.5})
        plt.show()
