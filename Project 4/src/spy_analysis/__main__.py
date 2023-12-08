# __main__.py for spy_analysis package

from .spy_data_loader import DataLoader
from .visualization import Visualization


def main():
    # Load the data
    data_loader = DataLoader("SPY_options_data.csv")
    data = data_loader.load_data()
    print("Data loaded successfully.")

    # Perform a sample visualization or analysis
    viz = Visualization(data)
    viz.sample_visualization()


if __name__ == "__main__":
    main()
