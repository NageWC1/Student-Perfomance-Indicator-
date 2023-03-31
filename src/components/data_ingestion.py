# this file will include all the script related to reading the data 
# will divide the dataset train and test 
# create validation data, different form of data for differen purpose 

import os
import sys 
import pandas as pd 
from sklearn.model_selection import train_test_split
from dataclasses import dataclass


# this is the exception that we created and that located under the src folder 
from src.exception import CustomeException
# this is also created by us to have record of execution of the prorame by the time 
from src.logger import logging 

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig
from src.components.model_trainer import ModelTrainer

# some of the input needed by the data ingesion like where we have to store the raw, train and test data 
# these will be creating below class 
# any data that will be give through this class 
# if we use this @dataclass decorater we can directly define the class variables without using __init__
@dataclass
class DataIngestionConfig:
    # all the output will store under the artifact folder 
    train_data_path: str = os.path.join('artifacts','train.csv')
    test_data_path: str = os.path.join('artifacts','test.csv')
    raw_data_path: str = os.path.join('artifacts','raw.csv')

class DataIngestion:
    def __init__(self):
        # inside this variable we string all the path that different data goin to store 
        self.ingesion_config=DataIngestionConfig()
    
    # this will responsible to read the data from any source (implementation to read data from any sources)
    def initiate_data_ingestion(self):
        logging.info("Enter into the data ingession method or component")
        try:
            df=pd.read_csv('nootbook\data\stud.csv')
            logging.info("Read the dataset as dataframe")
            # exist_ok=True : says that if the file is the we dont need to delete and create in again
            # that will be keep in there 
            os.makedirs(os.path.dirname(self.ingesion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingesion_config.raw_data_path, index=False,header=True)
            logging.info("train and test applit initiated")

            train_set,test_set = train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingesion_config.train_data_path, index=False,header=True)

            test_set.to_csv(self.ingesion_config.test_data_path, index=False,header=True)

            logging.info("Ingestion of the data completed")
            # we return the file path and this can access from any where the data_ingession file imported
            return(
                self.ingesion_config.train_data_path,
                self.ingesion_config.test_data_path
            )
        except Exception as e:
            logging.info(str(e))
            raise CustomeException(e, sys)

    
     
if __name__ == '__main__':
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    
    data_transformation = DataTransformation()
    train_arr, test_arr, _= data_transformation.initiate_data_transformation(train_data, test_data)

    model_trainer = ModelTrainer()
    print(model_trainer.initiate_model_trainer(train_arr,test_arr))

