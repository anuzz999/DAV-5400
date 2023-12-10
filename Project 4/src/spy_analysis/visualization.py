import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class DataVisualization:
    """
    A class for handling the visualization of SPY options data.
    """

    def __init__(self, data):
        """
        Initializes the DataVisualization with the SPY options dataset.

        Parameters:
        - data (DataFrame): The pandas DataFrame with the SPY options data.
        """
        self.data = data

    def plot_distributions(self, columns, bins=50):
        """
        Plots histograms with Kernel Density Estimate (KDE) for the specified columns.

        Parameters:
        - columns (list of str): List of column names to plot.
        - bins (int): Number of bins to use for the histograms.
        """
        sns.set(style="whitegrid")
        plt.figure(figsize=(15, 10))

        for i, column in enumerate(columns, 1):
            plt.subplot(3, 2, i)
            sns.histplot(self.data[column], kde=True, bins=bins)
            plt.title(f"Distribution of {column}")

        plt.tight_layout()
        plt.show()

    def plot_time_series(self, x, y, title, xlabel, ylabel):
        """
        Plots a time series line plot for the specified x and y data.

        Parameters:
        - x: The data for the x-axis (time).
        - y: The data for the y-axis (values to plot over time).
        - title (str): The title of the plot.
        - xlabel (str): The label for the x-axis.
        - ylabel (str): The label for the y-axis.
        """
        plt.figure(figsize=(12, 6))
        sns.lineplot(x=x, y=y)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    def plot_multi_time_series(self, series_dict, title, xlabel, ylabel):
        """
        Plots a time series line plot for multiple series on the same plot.

        Parameters:
        - series_dict (dict): A dictionary with labels as keys and time series data as values.
        - title (str): The title of the plot.
        - xlabel (str): The label for the x-axis.
        - ylabel (str): The label for the y-axis.
        """
        plt.figure(figsize=(15, 7))
        for label, series in series_dict.items():
            sns.lineplot(x=series.index, y=series.values, label=label)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.show()

    def plot_correlation_matrix(self, columns=None, title="Correlation Matrix"):
        """
        Plots a correlation matrix for the specified columns of the dataset.

        Parameters:
        - columns (list of str, optional): List of column names to include in the correlation matrix.
                                          If None, all columns are included.
        - title (str): Title of the plot.
        """
        if columns:
            correlation_matrix = self.data[columns].corr()
        else:
            correlation_matrix = self.data.corr()

        plt.figure(figsize=(12, 10))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title(title)
        plt.show()

    def plot_scatter(self, x, y, title, xlabel, ylabel):
        """
        Plots a scatter plot for the given x and y data.

        Parameters:
        - x (str): The column name for the x-axis variable.
        - y (str): The column name for the y-axis variable.
        - title (str): The title of the plot.
        - xlabel (str): The label for the x-axis.
        - ylabel (str): The label for the y-axis.
        """
        plt.figure(figsize=(12, 6))
        sns.scatterplot(x=x, y=y, data=self.data, alpha=0.5)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    def plot_violin(
        self, x, y, bins, bin_labels, rotate_xticks=0, title="", xlabel="", ylabel=""
    ):
        """
        Creates a violin plot for the distribution of a variable across binned groups.

        Parameters:
        - x (str): The column name to bin and use as the x-axis.
        - y (str): The column name for the y-axis variable.
        - bins (list): List of bin edges for binning the x variable.
        - bin_labels (list): List of labels for the bins.
        - rotate_xticks (int): Degree to rotate the x-axis labels for readability.
        - title (str): The title of the plot.
        - xlabel (str): The label for the x-axis.
        - ylabel (str): The label for the y-axis.
        """
        self.data[f"{x}_Binned"] = pd.cut(self.data[x], bins=bins, labels=bin_labels)

        plt.figure(figsize=(14, 8))
        sns.violinplot(x=f"{x}_Binned", y=y, data=self.data)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=rotate_xticks)
        plt.show()

    def plot_hexbin(
        self, x, y, gridsize=50, cmap="Greens", mincnt=1, title="", xlabel="", ylabel=""
    ):
        """
        Creates a hexbin plot for two variables to visualize their distribution and density.

        Parameters:
        - x (str): The column name for the x-axis variable.
        - y (str): The column name for the y-axis variable.
        - gridsize (int): The number of hexagons in the x-direction.
        - cmap (str): Colormap for the hexbins.
        - mincnt (int): Minimum number of occurrences required to display a hexbin.
        - title (str): The title of the plot.
        - xlabel (str): The label for the x-axis.
        - ylabel (str): The label for the y-axis.
        """
        plt.figure(figsize=(12, 6))
        plt.hexbin(
            self.data[x], self.data[y], gridsize=gridsize, cmap=cmap, mincnt=mincnt
        )
        plt.colorbar(label="Count in bin")
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()
