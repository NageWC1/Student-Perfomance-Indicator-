# here we specifically train our model
# how many differnt kind of model that we  going to user (ex classifcation, regression etc)
# here will call over the confusion matrics (R2 squre, adjusted R2 squre)

import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from sklearn.tree import DecisionTreeRegressor

from src.exception import CustomeException
from src.logger import logging
from src.utils import save_object,evaluate_model

@dataclass
class ModelTrainingConfig:
    train_model_file_path = os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainingConfig() # take the instance of the model config that contain the file paths 

    def initiate_model_trainer(self, train_arr, test_arr):
        try:
            logging.info("spliting the training and test input data")
            X_train,Y_train, X_test,Y_test =(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]

            )
            
            models ={
                "Linear Regression": LinearRegression(),
                "K-Neighbors Regressor": KNeighborsRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Random Forest Regressor": RandomForestRegressor(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoostRegressor": AdaBoostRegressor()
            }

            model_report:dict=evaluate_model(X_train=X_train,Y_train=Y_train,x_test = X_test, y_test = Y_test, models=models)

            ## To get best model score from the dict
            best_model_score = max(sorted(model_report.values()))

            ## To get best model name from dict 
            best_model_name = list(model_report.keys())[
                # what ever the index that  contain the best model score
                list(model_report.values()).index(best_model_score)
            ]   

            best_model = models[best_model_name]  

            if best_model_score < 0.6:
                raise CustomeException("No Best Model found")
            logging.info(f"Best found model on both taining and testing dataset")

            save_object(
                file_path=self.model_trainer_config.train_model_file_path,
                obj=best_model
            )                 

            perdicted = best_model.predict(X_test)

            r2_sqaure = r2_score(Y_test,perdicted)
            return r2_sqaure  
        
        except Exception as e:
            raise CustomeException(e, sys)