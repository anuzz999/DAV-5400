import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import itertools


class ModelPreparation:
    """
    Handles preparation of data for model training and evaluation.
    """

    def __init__(self, data):
        """
        Initializes the ModelPreparation with the dataset.

        Parameters:
        - data (DataFrame): The pandas DataFrame containing the options data.
        """
        self.data = data

    def prepare_data(
        self, feature_columns, target_column, data=None, test_size=0.2, random_state=42
    ):
        """
        Prepares the data for modeling by selecting features and splitting into train and test sets.
        Can work with a specified subset of the data if provided.

        Parameters:
        - feature_columns (list of str): List of column names to be used as features.
        - target_column (str): Column name to be used as the target variable.
        - data (DataFrame, optional): The subset of data to use. If None, uses the full dataset.
        - test_size (float): Proportion of the dataset to include in the test split.
        - random_state (int): Controls the shuffling applied to the data before applying the split.

        Returns:
        - tuple: A tuple containing the split data (X_train, X_test, y_train, y_test).
        """
        if data is None:
            data = self.data

        features = data[feature_columns]
        target = data[target_column]

        X_train, X_test, y_train, y_test = train_test_split(
            features, target, test_size=test_size, random_state=random_state
        )
        return X_train, X_test, y_train, y_test

    def prepare_subset(self, frac=0.1, random_state=42):
        """
        Prepares a subset of the data for faster processing.

        Parameters:
        - frac (float): Fraction of the data to sample for the subset.
        - random_state (int): Random state for reproducible sampling.

        Returns:
        - DataFrame: The subset of the data.
        """
        return self.data.sample(frac=frac, random_state=random_state)

    def simplified_model_cross_validation(
        self, X, y, n_estimators=10, cv_folds=3, random_state=42
    ):
        """
        Sets up a simplified Random Forest model and performs cross-validation.

        Parameters:
        - X: Features of the subset.
        - y: Target variable of the subset.
        - n_estimators (int): Number of trees in the Random Forest.
        - cv_folds (int): Number of folds for cross-validation.

        Returns:
        - tuple: Mean and standard deviation of cross-validation scores.
        """
        pipeline = Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "rf_regressor",
                    RandomForestRegressor(
                        n_estimators=n_estimators, random_state=random_state
                    ),
                ),
            ]
        )

        cv_scores = cross_val_score(
            pipeline, X, y, cv=cv_folds, scoring="neg_mean_squared_error"
        )
        cv_mean_score = np.mean(cv_scores)
        cv_std_score = np.std(cv_scores)

        return cv_mean_score, cv_std_score


class ModelEvaluation:
    """
    Handles the training, prediction, and evaluation of machine learning models.
    """

    def __init__(self, model):
        """
        Initializes the ModelEvaluation with a machine learning model.

        Parameters:
        - model: The machine learning model to be used for training and prediction.
        """
        self.model = model
        self.predictions = None

    def fit_and_predict(self, X_train, y_train, X_test):
        """
        Fits the model to the training data and makes predictions on the test data.

        Parameters:
        - X_train: Training features.
        - y_train: Training target variable.
        - X_test: Test features to make predictions on.

        Returns:
        - ndarray: Predictions made by the model on the test set.
        """
        self.model.fit(X_train, y_train)
        return self.model.predict(X_test)

    def evaluate_model(self, y_true, y_pred):
        """
        Evaluates the performance of the model using MSE and R-squared.

        Parameters:
        - y_true: True target values.
        - y_pred: Predicted target values from the model.

        Returns:
        - tuple: Mean Squared Error (MSE) and R-squared (R2) scores.
        """
        mse = mean_squared_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        return mse, r2

    def get_feature_importances(self, feature_names):
        """
        Extracts feature importances from the trained model, assuming it supports this attribute.

        Parameters:
        - feature_names (list of str): List of feature names.

        Returns:
        - DataFrame: A DataFrame containing features and their importances.
        """
        try:
            # Ensure the model is a pipeline with a regressor that has feature_importances_
            if hasattr(self.model, "named_steps") and hasattr(
                self.model.named_steps["rf_regressor"], "feature_importances_"
            ):
                feature_importances = self.model.named_steps[
                    "rf_regressor"
                ].feature_importances_
            else:
                raise AttributeError("The model does not support feature importances.")

            importances_df = pd.DataFrame(
                {"Feature": feature_names, "Importance": feature_importances}
            )
            return importances_df.sort_values(by="Importance", ascending=False)
        except AttributeError as e:
            print("Error:", e)
            return None

    def fit_and_evaluate_simplified_rf_with_poly(
        self,
        X_train,
        y_train,
        X_test,
        y_test,
        degree=2,
        interaction_only=True,
        n_estimators=10,
        max_depth=5,
        random_state=42,
    ):
        """
        Fits a simplified Random Forest model with polynomial feature transformation
        (interaction only) and evaluates its performance.

        Parameters:
        - X_train: Training features.
        - y_train: Training target variable.
        - X_test: Test features.
        - y_test: Test target variable.
        - degree (int): Degree of the polynomial features.
        - interaction_only (bool): If True, produce only interaction features.
        - n_estimators (int): Number of trees in the Random Forest.
        - max_depth (int): Maximum depth of the trees.
        - random_state (int): Random state for reproducibility.

        Returns:
        - tuple: Mean Squared Error (MSE) and R-squared (R2) scores.
        """
        # Creating interaction terms and polynomial features
        poly = PolynomialFeatures(
            degree=degree, include_bias=False, interaction_only=interaction_only
        )
        X_train_poly = poly.fit_transform(X_train)
        X_test_poly = poly.transform(X_test)

        # Creating and fitting a simplified Random Forest model
        self.model = RandomForestRegressor(
            n_estimators=n_estimators, max_depth=max_depth, random_state=random_state
        )
        self.model.fit(X_train_poly, y_train)

        # Predicting on the test set and evaluating the model
        self.predictions = self.model.predict(X_test_poly)
        mse_rf = mean_squared_error(y_test, self.predictions)
        r2_rf = r2_score(y_test, self.predictions)

        return mse_rf, r2_rf

    def get_predictions(self):
        """
        Returns the predictions stored in the class.

        Returns:
        - ndarray: Predictions made by the model.
        """
        if self.predictions is not None:
            return self.predictions
        else:
            raise ValueError(
                "No predictions available. Please run a prediction method first."
            )

    def create_importances_dataframe(self, X_train, degree=2):
        """
        Creates a DataFrame of feature importances for polynomial features.

        Parameters:
        - X_train: Training features DataFrame.
        - degree (optional): Degree of polynomial features.

        Returns:
        - DataFrame: A DataFrame with features and their importances.
        """
        # Creating interaction terms and polynomial features
        poly = PolynomialFeatures(
            degree=degree, include_bias=False, interaction_only=True
        )
        poly.fit_transform(X_train)

        # Get or create feature names
        if hasattr(poly, "get_feature_names_out"):
            poly_feature_names = poly.get_feature_names_out(X_train.columns)
        else:
            poly_feature_names = self._create_poly_feature_names(
                X_train.columns, degree
            )

        # Extract feature importances from the model
        if hasattr(self.model, "feature_importances_"):
            feature_importances = self.model.feature_importances_
        else:
            raise AttributeError(
                "The model does not have feature_importances_ attribute."
            )

        # Create a DataFrame for feature importances
        importances_df = pd.DataFrame(
            {"Feature": poly_feature_names, "Importance": feature_importances}
        )

        # Sort the DataFrame by importance
        importances_df.sort_values(by="Importance", ascending=False, inplace=True)

        return importances_df

    def simulate_trading_strategy(
        self, predictions, X_test, y_test, quantile_threshold=0.75
    ):
        """
        Simulates a trading strategy based on model predictions and calculates performance metrics.

        Parameters:
        - predictions: Predictions made by the model.
        - X_test: Test features DataFrame.
        - y_test: Test target variable.
        - quantile_threshold: Threshold for determining the decay rate.

        Returns:
        - dict: A dictionary containing total return, average return per trade, win rate, and max drawdown.
        """
        # Convert predictions to a Pandas Series
        predicted_decay_rates = pd.Series(predictions, index=X_test.index)

        # Determine the decay rate threshold
        decay_rate_threshold = predicted_decay_rates.quantile(quantile_threshold)

        # Simulate the strategy on the test set
        X_test["Predicted_Decay"] = predicted_decay_rates
        X_test["Trade"] = (X_test["Predicted_Decay"] > decay_rate_threshold).astype(int)
        X_test["Next_Day_Return"] = y_test.shift(
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
