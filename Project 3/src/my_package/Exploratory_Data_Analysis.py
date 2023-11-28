import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.dates as mdates


class DataCleaner:
    """
    A class used for cleaning and preparing data for analysis.

    Attributes
    ----------
    data : DataFrame
        a DataFrame containing the data to be cleaned

    Methods
    -------
    analyze_null_values()
        Analyzes the pattern of null values in the data.
    clean_column_names()
        Cleans the column names by removing unwanted characters.
    drop_columns(columns_to_drop)
        Drops specified columns from the DataFrame.
    convert_to_numeric(columns, errors='coerce')
        Converts specified columns to numeric data type.
    handle_null_values(strategy='drop', columns=None)
        Handles null values based on the specified strategy.
    """

    def __init__(self, data):
        """
        Parameters
        ----------
        data : DataFrame
            The DataFrame to be cleaned.
        """
        self.data = data

    def analyze_null_values(self):
        """
        Analyzes the pattern of null values in the DataFrame.

        Returns
        -------
        Series
            A Series displaying the number of null values in each column.
        """
        return self.data.isnull().sum()

    def clean_column_names(self):
        """
        Cleans the column names by removing leading and trailing spaces and square brackets.
        """
        self.data.columns = self.data.columns.str.strip().str.replace(
            "[\[\]]", "", regex=True
        )

    def drop_columns(self, columns_to_drop):
        """
        Drops specified columns from the DataFrame.

        Parameters
        ----------
        columns_to_drop : list of str
            List of column names to be dropped.
        """
        self.data.drop(columns=columns_to_drop, inplace=True, errors="ignore")

    def convert_to_numeric(self, columns, errors="coerce"):
        """
        Converts specified columns to numeric data type.

        Parameters
        ----------
        columns : list of str
            List of column names to be converted.
        errors : str, optional
            Specifies how to handle errors (default is 'coerce').
        """
        for column in columns:
            self.data[column] = pd.to_numeric(self.data[column], errors=errors)

    def convert_to_datetime(self, columns):
        """
        Converts specified columns to datetime data type.

        Parameters
        ----------
        columns : list of str
            List of column names to be converted.
        errors : str, optional
            Specifies how to handle errors (default is 'coerce').
        """
        for column in columns:
            self.data[column] = pd.to_datetime(self.data[column])
        return self.data

    def handle_null_values(self, strategy="drop", fill_method="mean", columns=None):
        """
        Handles null values based on the specified strategy.

        Parameters
        ----------
        strategy : str, optional
            Strategy to handle null values ('drop' or 'fill', default is 'drop').
        fill_method : str, optional
            Method to fill null values ('mean', 'median', 'mode', default is 'mean').
        columns : list of str, optional
            Specific columns to apply the strategy on (default is None, applied to all columns).
        """
        if strategy == "drop":
            if columns:
                self.data.dropna(subset=columns, inplace=True)
            else:
                self.data.dropna(inplace=True)
        elif strategy == "fill":
            if columns:
                for column in columns:
                    if fill_method == "mean":
                        self.data[column].fillna(self.data[column].mean(), inplace=True)
                    elif fill_method == "median":
                        self.data[column].fillna(
                            self.data[column].median(), inplace=True
                        )
                    elif fill_method == "mode":
                        self.data[column].fillna(
                            self.data[column].mode()[0], inplace=True
                        )
            else:
                for column in self.data:
                    if fill_method == "mean":
                        self.data[column].fillna(self.data[column].mean(), inplace=True)
                    elif fill_method == "median":
                        self.data[column].fillna(
                            self.data[column].median(), inplace=True
                        )
                    elif fill_method == "mode":
                        self.data[column].fillna(
                            self.data[column].mode()[0], inplace=True
                        )

    def save_cleaned_data(self, filename):
        """
        Save the cleaned data to a CSV file.

        Parameters:
        filename (str): The name of the file where the data should be saved.
        """
        try:
            self.full_data.to_csv(filename, index=False)
            print(f"Data successfully saved to {filename}")
        except Exception as e:
            print(f"An error occurred while saving the data: {e}")


class EDA:
    def __init__(self, data):
        """
        Initialize the EDA object with a dataset.

        Parameters:
        data (DataFrame): The dataset to be analyzed.
        """
        self.data = data

    def summary_statistics(self):
        """
        Generate summary statistics for the dataset.

        This method computes summary statistics for all columns in the dataset.
        It includes measures such as mean, standard deviation, min, max for numeric columns,
        and counts, unique values, frequency for categorical columns.

        Returns:
        DataFrame: A DataFrame containing the summary statistics.
        """
        return self.data.describe(include="all", datetime_is_numeric=True)

    def plot_iv_behavior(self, column, title="Implied Volatility Over Time"):
        """
        Plots the behavior of Implied Volatility over time using both Matplotlib and Seaborn.

        Parameters:
        column (str): The column representing Implied Volatility.
        title (str): The title of the plot.
        """
        # Check if the column exists in the DataFrame
        if column in self.data.columns:
            # Using Matplotlib
            plt.figure(figsize=(10, 6))
            plt.plot(
                self.data.index, self.data[column], label="Matplotlib", color="blue"
            )
            plt.title(title + " (Matplotlib)")
            plt.xlabel("Date")
            plt.ylabel("Implied Volatility")
            plt.legend()
            plt.show()

            # Using Seaborn
            plt.figure(figsize=(10, 6))
            sns.lineplot(
                data=self.data,
                x=self.data.index,
                y=column,
                label="Seaborn",
                color="orange",
            )
            plt.title(title + " (Seaborn)")
            plt.xlabel("Date")
            plt.ylabel("Implied Volatility")
            plt.legend()
            plt.show()
        else:
            print(f"Column '{column}' not found in the DataFrame.")

    def plot_price_and_iv_trends(self):
        """
        Plots the trends over time for both Call and Put Option Prices and their Implied Volatilities.

        This method generates four subplots:
        1. Call Option Prices Over Time
        2. Put Option Prices Over Time
        3. Call Option Implied Volatility Over Time
        4. Put Option Implied Volatility Over Time
        """
        # Ensure the date columns are in datetime format
        self.data["QUOTE_DATE"] = pd.to_datetime(self.data["QUOTE_DATE"])
        self.data["EXPIRE_DATE"] = pd.to_datetime(self.data["EXPIRE_DATE"])

        # Setting up the plots
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))

        # Plotting Call Option Prices Over Time
        sns.lineplot(
            ax=axes[0, 0], data=self.data, x="QUOTE_DATE", y="C_LAST"
        ).set_title("Call Option Prices Over Time")

        # Plotting Put Option Prices Over Time
        sns.lineplot(
            ax=axes[0, 1], data=self.data, x="QUOTE_DATE", y="P_LAST"
        ).set_title("Put Option Prices Over Time")

        # Plotting Call Option Implied Volatility Over Time
        sns.lineplot(ax=axes[1, 0], data=self.data, x="QUOTE_DATE", y="C_IV").set_title(
            "Call Option Implied Volatility Over Time"
        )

        # Plotting Put Option Implied Volatility Over Time
        sns.lineplot(ax=axes[1, 1], data=self.data, x="QUOTE_DATE", y="P_IV").set_title(
            "Put Option Implied Volatility Over Time"
        )

        plt.tight_layout()
        plt.show()

    def plot_price_and_iv_trends_matplotlib(self):
        """
        Plots the trends over time for both Call and Put Option Prices and their Implied Volatilities using Matplotlib.

        This method generates four subplots:
        1. Call Option Prices Over Time
        2. Put Option Prices Over Time
        3. Call Option Implied Volatility Over Time
        4. Put Option Implied Volatility Over Time
        """
        # Ensure the date columns are in datetime format
        self.data["QUOTE_DATE"] = pd.to_datetime(self.data["QUOTE_DATE"])

        # Setting up the plots
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))

        # Plotting Call Option Prices Over Time
        axes[0, 0].plot(self.data["QUOTE_DATE"], self.data["C_LAST"])
        axes[0, 0].set_title("Call Option Prices Over Time")
        axes[0, 0].set_xlabel("Date")
        axes[0, 0].set_ylabel("Price")
        axes[0, 0].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

        # Plotting Put Option Prices Over Time
        axes[0, 1].plot(self.data["QUOTE_DATE"], self.data["P_LAST"])
        axes[0, 1].set_title("Put Option Prices Over Time")
        axes[0, 1].set_xlabel("Date")
        axes[0, 1].set_ylabel("Price")
        axes[0, 1].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

        # Plotting Call Option Implied Volatility Over Time
        axes[1, 0].plot(self.data["QUOTE_DATE"], self.data["C_IV"])
        axes[1, 0].set_title("Call Option Implied Volatility Over Time")
        axes[1, 0].set_xlabel("Date")
        axes[1, 0].set_ylabel("Implied Volatility")
        axes[1, 0].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

        # Plotting Put Option Implied Volatility Over Time
        axes[1, 1].plot(self.data["QUOTE_DATE"], self.data["P_IV"])
        axes[1, 1].set_title("Put Option Implied Volatility Over Time")
        axes[1, 1].set_xlabel("Date")
        axes[1, 1].set_ylabel("Implied Volatility")
        axes[1, 1].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

        # Adjusting layout for clarity
        plt.tight_layout()
        plt.show()

    def histogram_matplotlib(self, column, bins=30, title="Histogram"):
        """
        Creates a histogram for the specified column using Matplotlib.

        Parameters:
        column (str): The name of the column to create a histogram for.
        bins (int): The number of bins for the histogram.
        title (str): The title of the histogram.
        """
        plt.figure(figsize=(12, 6))
        plt.hist(self.data[column], bins=bins, color="blue", alpha=0.7)
        plt.title(f"{title} (SPY ETF Price) - Matplotlib")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.axvline(
            self.data[column].mean(),
            color="red",
            linestyle="dashed",
            linewidth=1,
            label="Mean",
        )
        plt.axvline(
            self.data[column].median(),
            color="green",
            linestyle="dashed",
            linewidth=1,
            label="Median",
        )
        plt.legend()
        plt.show()

    def histogram_seaborn(self, column, bins=30, title="Histogram"):
        """
        Creates a histogram for the specified column using Seaborn.

        Parameters:
        column (str): The name of the column to create a histogram for.
        bins (int): The number of bins for the histogram.
        title (str): The title of the histogram.
        """
        plt.figure(figsize=(12, 6))
        sns.histplot(self.data[column], bins=bins, kde=True, color="blue")
        plt.title(f"{title} (SPY ETF Price) - Seaborn")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.axvline(
            self.data[column].mean(),
            color="red",
            linestyle="dashed",
            linewidth=1,
            label="Mean",
        )
        plt.axvline(
            self.data[column].median(),
            color="green",
            linestyle="dashed",
            linewidth=1,
            label="Median",
        )
        plt.legend()
        plt.show()

    def plot_greeks_by_time_frame(self, greek_columns):
        """
        Creates box plots for specified Greek columns across different time frames.

        Parameters:
        greek_columns (list): List of Greek column names to plot.
        """
        # Defining the time frame categories based on DTE
        self.data["Time_Frame"] = pd.cut(
            self.data["DTE"],
            bins=[0, 30, 90, np.max(self.data["DTE"])],
            labels=["Short-term", "Medium-term", "Long-term"],
        )

        # Creating box plots for each Greek across different time frames
        fig, axes = plt.subplots(len(greek_columns), 1, figsize=(10, 20))

        # Plotting box plots for each Greek
        for i, greek in enumerate(greek_columns):
            sns.boxplot(x="Time_Frame", y=greek, data=self.data, ax=axes[i])
            axes[i].set_title(f"Distribution of {greek} by Time Frame")
            axes[i].set_xlabel("Time Frame")
            axes[i].set_ylabel(greek)

        plt.tight_layout()
        plt.show()

    def plot_quote_date_and_civ(self):
        """
        Creates histogram plots for 'QUOTE_DATE' and 'C_IV', including an inset for 'C_IV'.
        """
        # Convert 'QUOTE_DATE' to datetime if not already done
        self.data["QUOTE_DATE"] = pd.to_datetime(self.data["QUOTE_DATE"])

        # Setting the style for the plots
        sns.set(style="whitegrid")

        # Creating enhanced plot for 'QUOTE_DATE'
        plt.figure(figsize=(10, 6))
        date_plot = sns.histplot(self.data["QUOTE_DATE"], kde=False)
        date_plot.set_title("Distribution of Quote Dates")
        date_plot.set_xticklabels(
            self.data["QUOTE_DATE"].dt.strftime("%Y-%m-%d"), rotation=45
        )
        plt.tight_layout()

        # Creating an inset plot for 'C_IV'
        plt.figure(figsize=(10, 6))
        main_ax = sns.histplot(self.data["C_IV"], kde=True)
        main_ax.set_title("Distribution of Call Implied Volatility (C_IV) with Inset")

        # Inset for the concentrated area
        inset_ax = main_ax.inset_axes([0.5, 0.5, 0.45, 0.45])
        sns.histplot(
            self.data[self.data["C_IV"] < 0.5]["C_IV"], ax=inset_ax, bins=30, kde=True
        )
        inset_ax.set_title("Inset: Lower Range of C_IV")
        plt.show()

    def histogram_underlying_last_with_annotations(self):
        """
        Creates a histogram for the 'UNDERLYING_LAST' column and annotates it with the mean and median.
        """
        plt.figure(figsize=(10, 6))
        plt.hist(
            self.data["UNDERLYING_LAST"], bins=30, color="skyblue", edgecolor="black"
        )
        plt.axvline(
            self.data["UNDERLYING_LAST"].mean(),
            color="red",
            linestyle="dashed",
            linewidth=1,
            label="Mean",
        )
        plt.axvline(
            self.data["UNDERLYING_LAST"].median(),
            color="green",
            linestyle="dashed",
            linewidth=1,
            label="Median",
        )
        plt.title("Histogram of Underlying Asset Last Price with Annotations")
        plt.xlabel("Underlying Last Price")
        plt.ylabel("Frequency")
        plt.legend()
        plt.show()

    def histogram_c_iv_with_inset(self):
        """
        Creates a histogram for the 'C_IV' column and adds an inset for a concentrated area of the data.
        """
        plt.figure(figsize=(10, 6))
        main_ax = plt.gca()
        main_ax.hist(self.data["C_IV"], bins=30, color="skyblue", edgecolor="black")
        main_ax.set_title("Distribution of Call Implied Volatility (C_IV) with Inset")
        main_ax.set_xlabel("Call Implied Volatility (C_IV)")
        main_ax.set_ylabel("Frequency")

        # Adding an inset for the concentrated area
        inset_ax = main_ax.inset_axes([0.5, 0.5, 0.45, 0.45])
        inset_ax.hist(
            self.data[self.data["C_IV"] < 0.5]["C_IV"],
            bins=30,
            color="lightgreen",
            edgecolor="black",
        )
        inset_ax.set_title("Inset: Lower Range of C_IV")
        inset_ax.set_xlabel("C_IV")
        inset_ax.set_ylabel("Frequency")
        plt.show()
