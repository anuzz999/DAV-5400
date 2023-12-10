import pandas as pd


class StrategySimulation:
    """
    Handles the simulation of trading strategies based on model predictions.
    """

    def simulate_trading_strategy(
        self, X_test, y_pred, y_actual, quantile_threshold=0.75
    ):
        """
        Simulates a trading strategy based on predicted values and calculates performance metrics.

        Parameters:
        - X_test: Test features DataFrame.
        - y_pred: Predicted values from the model.
        - y_actual: Actual target values for the test set.
        - quantile_threshold (float): Threshold for decision-making based on quantile of predictions.

        Returns:
        - dict: Dictionary containing various performance metrics of the trading strategy.
        """
        # Convert predictions to a Pandas Series and add to X_test
        predicted_decay_rates = pd.Series(y_pred, index=X_test.index)
        X_test["Predicted_Decay"] = predicted_decay_rates

        # Determine the decay rate threshold
        decay_rate_threshold = predicted_decay_rates.quantile(quantile_threshold)

        # Create trading signals
        X_test["Trade"] = (X_test["Predicted_Decay"] > decay_rate_threshold).astype(int)
        X_test["Next_Day_Return"] = y_actual.shift(
            -1
        )  # Assuming the next day's return for simplicity

        # Calculate returns from the strategy
        X_test["Strategy_Return"] = X_test["Trade"] * X_test["Next_Day_Return"]

        # Aggregate and calculate performance metrics
        total_return = X_test["Strategy_Return"].sum()
        average_return_per_trade = X_test["Strategy_Return"].mean()
        win_rate = (X_test["Strategy_Return"] > 0).mean()
        max_drawdown = X_test["Strategy_Return"].cumsum().min()

        return {
            "Total Return": total_return,
            "Average Return per Trade": average_return_per_trade,
            "Win Rate": win_rate,
            "Max Drawdown": max_drawdown,
        }
