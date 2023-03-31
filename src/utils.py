# any functionality  that writing as common way, which will be using in entire appication
# basically we can create mongo db client here 
# if probably want to save the model over the clouse we write that here 
import os
import sys
import numpy as np 
import pandas as pd
# another library which will help us to create pickle file 
import dill 
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomeException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise CustomeException(e, sys)


def evaluate_model(X_train,Y_train,x_test, y_test , models, param):
    try:
        report ={}
        # going through each and every model
        for i in range(len(list(models))):
            # take one model from list with its index by loop value 
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,Y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,Y_train)

            y_train_pred = model.predict(X_train) # predict with x_train

            y_test_pred = model.predict(x_test) # predict with x_tes

            # calculate the sore by compare y_train value and y_train predicted value
            train_model_score = r2_score(Y_train, y_train_pred) 

            # calculate the sore by compare y_test value and y_test predicted value
            test_model_score = r2_score(y_test, y_test_pred)

            # create the report using test model score 
            report[list(models.keys())[i]] =  test_model_score

        return report
    except Exception as e:
        raise Exception(e,sys)

def load_object(file_path):
    try:
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomeException(e, sys)