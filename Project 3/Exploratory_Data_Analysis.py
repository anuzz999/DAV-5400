import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


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
    """
    A class for performing Exploratory Data Analysis on the SPY options dataset.

    Methods:
    - plot_iv_behavior: Plots Implied Volatility over time.
    - plot_greek_dynamics: Plots the dynamics of a specified Greek over time.
    - analyze_strike_price_relationship: Analyzes relationship between strike price and an option attribute.
    - plot_iv_near_expiry: Plots IV behavior near option expiry.
    - correlation_analysis: Performs correlation analysis between specified columns.
    - plot_histogram_with_inset: Plots a histogram with an inset for a specified range.
    - plot_with_annotations: Creates a plot and annotates it with typical ranges.
    - multivariate_analysis: Performs multivariate analysis on specified columns.
    - summary_statistics: Generates summary statistics for the dataset.
    """

    def __init__(self, data):
        self.data = data

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

    def plot_greek_dynamics(
        self, data, greek="C_DELTA", title="Greek Dynamics Over Time"
    ):
        # Implementation for plot_greek_dynamics method
        plt.figure(figsize=(10, 6))
        plt.plot(data.index, data[greek], label=f"{greek} Value")
        plt.title(title)
        plt.xlabel("Date")
        plt.ylabel(greek)
        plt.legend()
        plt.show()

    def analyze_strike_price_relationship(
        self, data, strike_column="STRIKE", attribute_column="C_LAST"
    ):
        # Implementation for analyze_strike_price_relationship method
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=data[strike_column], y=data[attribute_column])
        plt.title(f"Relationship Between {strike_column} and {attribute_column}")
        plt.xlabel("Strike Price")
        plt.ylabel(attribute_column)
        plt.show()

    def plot_iv_near_expiry(
        self, data, column="C_IV", expiry_column="DTE", threshold=30
    ):
        # Implementation for plot_iv_near_expiry method
        near_expiry_data = data[data[expiry_column] <= threshold]
        plt.figure(figsize=(10, 6))
        plt.plot(
            near_expiry_data.index,
            near_expiry_data[column],
            label="Implied Volatility Near Expiry",
        )
        plt.title(f"Implied Volatility Behavior Near Expiry (Within {threshold} Days)")
        plt.xlabel("Date")
        plt.ylabel("Implied Volatility")
        plt.legend()
        plt.show()

    def correlation_analysis(self, data, columns):
        # Implementation for correlation_analysis method
        plt.figure(figsize=(10, 8))
        sns.heatmap(data[columns].corr(), annot=True, cmap="coolwarm")
        plt.title("Correlation Matrix")
        plt.show()

    def plot_histogram_with_inset(
        self, data, column, inset_range=None, title="Histogram with Inset"
    ):
        # Implementation for plot_histogram_with_inset method
        fig, ax = plt.subplots()
        data[column].hist(ax=ax, bins=30, edgecolor="black")
        ax.set_title(title)
        if inset_range:
            ax_inset = fig.add_axes([0.5, 0.5, 0.4, 0.4])
            data[column].hist(
                ax=ax_inset, bins=15, range=inset_range, edgecolor="black"
            )
            ax_inset.set_title("Inset Histogram")
        plt.show()

    def plot_with_annotations(
        self, data, x_col, y_col, annotation_ranges, title="Annotated Plot"
    ):
        # Implementation for plot_with_annotations method
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=data[x_col], y=data[y_col])
        for label, range_val in annotation_ranges.items():
            plt.axhline(
                y=range_val, color="red", linestyle="--", label=f"{label}: {range_val}"
            )
        plt.title(title)
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.legend()
        plt.show()

    def multivariate_analysis(self, data, columns, plot_type="pairplot"):
        # Implementation for multivariate_analysis method
        if plot_type == "pairplot":
            sns.pairplot(data[columns])
        elif plot_type == "heatmap":
            corr_matrix = data[columns].corr()
            sns.heatmap(corr_matrix, annot=True, cmap="coolwarm")
        plt.show()

    def summary_statistics(self, data):
        # Implementation for summary_statistics method
        return data.describe(include="all", datetime_is_numeric=True)

    def plot_price_and_iv_trends(self):
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))

        # Plotting Call Option Prices Over Time with Matplotlib
        axes[0, 0].plot(self.data["QUOTE_DATE"], self.data["C_LAST"], label="C_LAST")
        axes[0, 0].set_title("Call Option Prices Over Time")
        axes[0, 0].set_xlabel("Quote Date")
        axes[0, 0].set_ylabel("Call Option Last Price")
        axes[0, 0].legend()

        # Plotting Put Option Prices Over Time with Matplotlib
        axes[0, 1].plot(
            self.data["QUOTE_DATE"], self.data["P_LAST"], label="P_LAST", color="orange"
        )
        axes[0, 1].set_title("Put Option Prices Over Time")
        axes[0, 1].set_xlabel("Quote Date")
        axes[0, 1].set_ylabel("Put Option Last Price")
        axes[0, 1].legend()

        # Plotting Call Option Implied Volatility Over Time with Seaborn
        sns.lineplot(ax=axes[1, 0], data=self.data, x="QUOTE_DATE", y="C_IV").set_title(
            "Call Option Implied Volatility Over Time"
        )

        # Plotting Put Option Implied Volatility Over Time with Seaborn
        sns.lineplot(ax=axes[1, 1], data=self.data, x="QUOTE_DATE", y="P_IV").set_title(
            "Put Option Implied Volatility Over Time"
        )

        # Plotting Call Option Prices Over Time
        sns.lineplot(
            ax=axes[0, 0], data=self.data, x="QUOTE_DATE", y="C_LAST"
        ).set_title("Call Option Prices Over Time")

        # Plotting Put Option Prices Over Time
        sns.lineplot(
            ax=axes[0, 1], data=self.dat, x="QUOTE_DATE", y="P_LAST"
        ).set_title("Put Option Prices Over Time")

        plt.show()

    def plot_with_matplotlib(
        self, x_column, y_column, title, xlabel, ylabel, color="blue"
    ):
        plt.figure(figsize=(15, 5))
        plt.plot(self.data[x_column], self.data[y_column], label=ylabel, color=color)
        plt.title(title + " (Matplotlib)")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.show()

    def plot_with_seaborn(
        self, x_column, y_column, title, xlabel, ylabel, color="blue"
    ):
        plt.figure(figsize=(15, 5))
        sns.lineplot(data=self.data, x=x_column, y=y_column, color=color).set_title(
            title + " (Seaborn)"
        )
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()
