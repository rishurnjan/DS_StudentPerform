import sys 
from dataclasses import dataclass
import os

import numpy as np 
import pandas as pd 
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer 
from sklearn.pipeline import Pipeline 
from sklearn.preprocessing import OneHotEncoder, StandardScaler 


from src.exception import CustomException
from src.logger import logging

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file= os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            numerical_columns=['writing_score','reading_score']
            categorical_columns=["gender",
                                 "race_ethnicity",
                                 "parental_level_of_education",
                                 "lunch",
                                 "test_prepration_course",
                                 ]
            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy='median') ),
                    ("Scaler",StandardScaler())
                ]
            )
            cat_pipeline=Pipeline(
                steps=[ 
                    ("imputer",SimpleImputer(strategy='most_frequent')),
                    ("one_hot_encoder",OneHotEncoder())
                    ("scaler",StandardScaler())
                ]
            )
            
            logging.info("numerical columns standard scaling completed and categorical columns got encoded")

            preprocessor=ColumnTransformer(
                 [
                     ("numerical_pipeline",num_pipeline,numerical_columns)
                     ("categorical_pipeline",cat_pipeline,categorical_columns)
                 ]
            )
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_df)
            logging.info("read the train and test data")

            preprocessing_obj=self.get_data_transformer_object()

            target_column='math_score'

            input_train_df= train_df.drop(columns=[target_column])
            target_train_df=train_df[target_column]

            input_test_df= test_df.drop(columns=[target_column])
            target_test_df=test_df[target_column]

            input_train_arr=preprocessing_obj.fit_transform(input_train_df)
            input_test_arr=preprocessing_obj.transform(input_test_df)

            train_arr= np.c_[input_train_arr,np.array(target_train_df)]
            test_arr=np.c_[input_test_arr,np.array(target_test_df)]

            logging.info("saved preprocessing object")
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file,
            )

        except:
            pass
        