import os
import sys 
from dataclasses import dataclass 

from catboost import CatBoostRegressor 
from sklearn.ensemble import AdaBoostRegressor,GradientBoostingRegressor,RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score 
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor 
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer= ModelTrainerConfig()

    def initiate_model_trainer(train_array,test_array,preprocessor_path):
        try:
            logging.info("Spliting train and test data")
            X_train=train_array[:,:-1]
            y_train=train_array[:,-1]
            X_test=test_array[:,:-1]# validation set
            y_test=test_array[:,-1]

            model={
                "Random Forest":RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression":LinearRegression(),
                "K neighbors regression": KNeighborsRegressor(),
                "XGBoost Regression": XGBRegressor(),
                "CatBoosting": CatBoostRegressor(),
                "Adaboost": AdaBoostRegressor(),
            }

            model_report:dict=evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,
                                             models=models,param=params)
            
            best_model_score=max(sorted(model_report.values()))

            best_model_name= list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model= model[best_model_name]
            if best_model_score<0.6:
                raise CustomException("No best model found")
            logging.info(f"Best found model on both training and testing dataset")
            
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model

            )

            predicted=best_model.predict(X_test)
            r2_square= r2_score(y_test,predicted)
            return r2_square
        
        except Exception as e:
            raise CustomException(e,sys)

