import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class ExploratoryDataAnalysis:
    def __init__(self, file_path: str):
        """
        Initializes the class and loads the data from a file.
        
        Parameters:
        file_path (str): The path to the dataset file.
        """
        self.data = pd.read_csv(file_path)
        
    def calculate_summary_statistics(self) -> pd.DataFrame:
        """
        Calculates summary statistics for each column in the dataset.
        
        Returns:
        pd.DataFrame: A DataFrame containing summary statistics.
        """
        return self.data.describe().transpose()
    
    
    def plot_histogram(self, column: str, bins: int = 30, title: str = None, 
                       x_label: str = None, y_label: str = 'Frequency'):
        """
        Plots a histogram for a specified column using Matplotlib and Seaborn.
        
        Parameters:
        column (str): The name of the column for which the histogram will be created.
        bins (int): Number of bins in the histogram.
        title (str): Title of the histogram.
        x_label (str): Label for the x-axis.
        y_label (str): Label for the y-axis.
        """
        data_to_plot = self.data[column].dropna()

        # Matplotlib Histogram
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.hist(data_to_plot, bins=bins, color='skyblue', edgecolor='black')
        plt.title(title if title else f"Histogram of {column} (Matplotlib)")
        plt.xlabel(x_label if x_label else column)
        plt.ylabel(y_label)
        
        # Seaborn Histogram
        plt.subplot(1, 2, 2)
        sns.histplot(data_to_plot, bins=bins, kde=True, color='salmon')
        plt.title(title if title else f"Histogram of {column} (Seaborn)")
        plt.xlabel(x_label if x_label else column)
        plt.ylabel(y_label)
        
        plt.tight_layout()
        plt.show()

    def plot_boxplot(self, columns: list, titles: list = None, x_labels: list = None, y_labels: list = None):
        """
        Creates box plots for specified columns using both Matplotlib and Seaborn.
        
        Parameters:
        columns (list): A list of column names for which box plots will be created.
        titles (list): A list of titles for the box plots.
        x_labels (list): A list of x_labels for the box plots.
        y_labels (list): A list of y_labels for the box plots.
        """
        num_columns = len(columns)
        titles = titles or columns
        x_labels = x_labels or columns
        y_labels = y_labels or ['']*num_columns
        
        plt.figure(figsize=(15, 5*num_columns))
        
        for i, column in enumerate(columns):
            data_to_plot = self.data[column].dropna()
            
            # Matplotlib Box Plot
            plt.subplot(num_columns, 2, 2*i+1)
            plt.boxplot(data_to_plot)
            plt.title(titles[i] if titles else f"Box Plot of {column} (Matplotlib)")
            plt.xlabel(x_labels[i] if x_labels else column)
            plt.ylabel(y_labels[i] if y_labels else '')
            
            # Seaborn Box Plot
            plt.subplot(num_columns, 2, 2*i+2)
            sns.boxplot(x=data_to_plot, color='salmon')
            plt.title(titles[i] if titles else f"Box Plot of {column} (Seaborn)")
            plt.xlabel(x_labels[i] if x_labels else column)
            plt.ylabel(y_labels[i] if y_labels else '')
        
        plt.tight_layout()
        plt.show()


    def plot_bar(self, column: str, title: str = None, x_label: str = None, y_label: str = 'Count'):
        """
        Plots a bar chart for the value counts of a specified categorical column using Matplotlib and Seaborn.
        
        Parameters:
        column (str): The name of the categorical column.
        title (str): Title of the bar chart.
        x_label (str): Label for the x-axis.
        y_label (str): Label for the y-axis.
        """
        data_to_plot = self.data[column].value_counts()

        # Matplotlib Bar Plot
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        data_to_plot.plot(kind='bar', color='skyblue', edgecolor='black')
        plt.title(title if title else f"Bar Chart of {column} (Matplotlib)")
        plt.xlabel(x_label if x_label else column)
        plt.ylabel(y_label)
        
        # Seaborn Bar Plot
        plt.subplot(1, 2, 2)
        sns.countplot(x=column, data=self.data, order=data_to_plot.index, color='salmon')
        plt.title(title if title else f"Bar Chart of {column} (Seaborn)")
        plt.xlabel(x_label if x_label else column)
        plt.ylabel(y_label)
        
        plt.tight_layout()
        plt.show()

    def plot_pairplot(self, columns: list, hue: str = None):
        """
        Plots a pair plot of specified columns using Seaborn.
        
        Parameters:
        columns (list): A list of column names to be included in the pair plot.
        hue (str): The name of a categorical column to color encode.
        """
        sns.pairplot(self.data[columns], hue=hue)
        plt.suptitle('Pair Plot', y=1.02)
        plt.show()



