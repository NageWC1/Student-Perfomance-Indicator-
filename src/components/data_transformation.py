# this will include the feature that used to transfer the data
# here we will do the categorical data into numberical data 
# how to handle one hot encoding, how handle label encoding 
# those kind of implementation will be here 
import sys 
from dataclasses import dataclass
import os
import numpy as np 
import pandas as pd 
# used to create the pipeline 
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomeException
from src.logger import logging
from src.utils import save_object

# it will give any path that will probably requiring any inputs 
@dataclass
class DataTransformationConfig:
    # we just giving the data transfer pickle file path to save the preprocessor pickle file 
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_tranformation_config = DataTransformationConfig()

    # create all the pickle file which will be responsible in covertin categorical fesature into numerical 
    # perform standard scaler 
    def get_trasnformer_obj(self):
        '''
        This function is responsible for data transformation 
        '''
        try:
            numerical_clumns =['writing_score','reading_score']
            categorical_columns = [
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course'
            ]

            # creating pipeline to handle the numerical variable 
            num_pipepline= Pipeline(
                steps=[
                # this is handle the missing value
                ("imputer",SimpleImputer(strategy="median")),
                # this is standardize the numerical inputs 
                ("scaler",StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                # handling the missing values using  
                ("imputer", SimpleImputer(strategy="most_frequent")),
                # transfer the categorical features into numerical by  using OneHotHandling 
                ("one_hot_encoder",OneHotEncoder()),
                # also we doing standard scaler as once
                ("scaler", StandardScaler(with_mean=False))

                ]
            )
            logging.info("Numerical columns standard scalin completed")
            logging.info("categorical columns encoding completed")

            # to combine the pipeline we use Columntransformer
            preprocessor = ColumnTransformer(
                [
                  #giving the piple and the columns that going to hanlde numerical feature 
                ("num_pipepline",num_pipepline,numerical_clumns),
                # giving the pipeline and columns that hanle the categorical featrure 
                ("cat_pipeline",cat_pipeline,categorical_columns)
                ]
            )

            return preprocessor
        except Exception as e:
            raise CustomeException(e, sys)

    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj=self.get_trasnformer_obj()

            target_column_name="math_score"
            numerical_columns = ["writing_score", "reading_score"]

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(

                file_path=self.data_tranformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )

            return (
                train_arr,
                test_arr,
                self.data_tranformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomeException(e,sys)