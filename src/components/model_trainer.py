import os, sys

import pandas as pd
import numpy as np
from dataclasses import dataclass

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_models


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts', 'model.pkl')


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting, training and test data")
            X_train, y_train, X_test, y_test =(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Linear Regression": LinearRegression(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "K-Neighbors Regressior": KNeighborsRegressor(),
                "AdaBoost Regressor": AdaBoostRegressor()
            }

            params ={
                "Decision Tree": {
                    'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson']
                },

                "Random Forest": {
                    'n_estimators': [8,16,32,64,128,256]
                },

                "Gradient Boosting": {
                    'learning_rate': [0.1, 0.01, 0.05, 0.001]
                },

                "Linear Regression": {},
                "K-Neighbors Regressior": {
                    'n_neighbors': [5,7,9,11]
                },

                "AdaBoost Regressor": {
                    'learning_rate': [0.1, 0.01, 0.5, 0.05]
                }
            }


            model_report:dict = evaluate_models(X_train=X_train, y_train=y_train,X_test=X_test, y_test=y_test, models=models, param= params)

            # To get best model score from dict
            best_model_score = max(sorted(model_report.values()))

            # To get best model from dict
            best_model_name = list(model_report.keys())[ list(model_report.values()).index(best_model_score)]

            best_model = models[best_model_name]

            if best_model_score <0.6:
                raise CustomException("No best model found")
            logging.info("Best model found on both training ansd test set")

            save_object(
                file_path = self.model_trainer_config.trained_model_file_path,
                obj = best_model
            )

            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted)
            return r2_square

        except Exception as e:
            raise CustomException(e, sys)