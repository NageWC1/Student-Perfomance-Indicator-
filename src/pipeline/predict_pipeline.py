# after createing the model, then we want to predict for the new data we wil basically write 
# over here 

import sys
import pandas as pd

from src.exception import CustomeException
from src.utils import load_object

class PredictPipeline:
    def __init__(self):
        pass
    def pradict(self, features):
        try:
            model_path = 'artifacts\model.pkl'
            preprocessor_path = 'artifacts\preprocessor.pkl'
            model = load_object(file_path = model_path)
            preprocessor = load_object(file_path = preprocessor_path)
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            return preds 
        except Exception as e:
            raise CustomeException(e, sys)
        
# this is class is responsinble to get the data from the front end and then map into backend 
class CustomData:
    def __init__(self,
                 gender: str,
                 race_ethnicity:str,
                 parental_level_of_education,
                 lunch: str,
                 test_preparation_course: str,
                 reading_score: int,
                 writing_score: int,
                 ):
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score

    # return all the data form of daa frame 
    def get_data_as_frame(self):
        try:
            custom_data_input_dict = {
                    "gender": [self.gender],
                    "race_ethnicity": [self.race_ethnicity],
                    "parental_level_of_education": [self.parental_level_of_education],
                    "lunch": [self.lunch],
                    "test_preparation_course": [self.test_preparation_course],
                    "reading_score": [self.reading_score],
                    "writing_score": [self.writing_score],
            }

            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise CustomeException(e,sys)