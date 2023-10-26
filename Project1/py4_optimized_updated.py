import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Part4Analysis:
    def __init__(self, file_path: str):
        """
        Initializes the class and loads the data from a file.
        
        Parameters:
        file_path (str): The path to the dataset file.
        """
        try:
            self.data = pd.read_csv(file_path)
        except FileNotFoundError:
            print(f"Error: The file at path {file_path} does not exist.")
        
    def plot_scatter(self, x_columns, y_columns, titles, x_labels, y_labels, subplot_shape=(2, 1)):
        """
        Creates scatter plots based on the input parameters.
    
        Parameters:
        x_columns (list): List of column names for the x-axis.
        y_columns (list): List of column names for the y-axis.
        titles (list): Titles for the scatter plots.
        x_labels (list): Labels for the x-axis.
        y_labels (list): Labels for the y-axis.
        subplot_shape (tuple): Shape of the subplot layout.
        """
        for i, (x_col, y_col, title, x_label, y_label) in enumerate(zip(x_columns, y_columns, titles, x_labels, y_labels)):
            plt.figure(figsize=(12, 6))
        
            # Error handling for non-existent columns
            if x_col not in self.data.columns or y_col not in self.data.columns:
                print(f"Error: One or both of the columns {x_col}, {y_col} do not exist in the dataset.")
                return
        
            data_to_plot = self.data.dropna(subset=[x_col, y_col])
        
            # Matplotlib Scatter Plot
            plt.subplot(subplot_shape[0], subplot_shape[1], 1)
            plt.scatter(data_to_plot[x_col], data_to_plot[y_col], alpha=0.5)
            plt.title(f"Matplotlib: {title}")
            plt.xlabel(x_label)
            plt.ylabel(y_label)
        
            # Seaborn Scatter Plot
            plt.subplot(subplot_shape[0], subplot_shape[1], 2)
            sns.scatterplot(x=x_col, y=y_col, data=data_to_plot, alpha=0.5, color='salmon')
            plt.title(f"Seaborn: {title}")
            plt.xlabel(x_label)
            plt.ylabel(y_label)
        
            plt.tight_layout()
            plt.show()

      
        
    def plot_correlation_matrix(self):
        """
        Creates a heatmap of the correlation matrix of the dataset's attributes.
        """
        correlation_matrix = self.data.corr()
        plt.figure(figsize=(12, 8))
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', linewidths=2, linecolor='black')
        plt.title('Correlation Matrix')
        plt.show()
    
    # Other plot methods go here, utilizing the plot_scatter method

    def plot_iv_vs_dte(self):
        """
        Creates scatter plots to visualize the relationship between Implied Volatility (IV) 
        and Days to Expiry (DTE) for options.
        """
        x_columns = ['DTE', 'DTE']
        y_columns = ['C_IV', 'P_IV']
        titles = ['Call Option IV vs. DTE', 'Put Option IV vs. DTE']
        x_labels = ['Days to Expiry (DTE)'] * 2
        y_labels = ['Implied Volatility (IV)'] * 2
        self.plot_scatter(x_columns, y_columns, titles, x_labels, y_labels)
    
    def plot_iv_vs_moneyness(self):
        """
        Creates scatter plots to visualize the relationship between Implied Volatility (IV) 
        and Strike Distance (Moneyness) for options.
        """
        x_columns = ['STRIKE_DISTANCE', 'STRIKE_DISTANCE']
        y_columns = ['C_IV', 'P_IV']
        titles = ['Call Option IV vs. Moneyness', 'Put Option IV vs. Moneyness']
        x_labels = ['Strike Distance (Moneyness)'] * 2
        y_labels = ['Implied Volatility (IV)'] * 2
        self.plot_scatter(x_columns, y_columns, titles, x_labels, y_labels)
