from src.logging import logger 
from src.entity.config_entity import ModelTrainingPipelineConfig
from src.entity.artifcats_entity import DataTransformationArtifacts, ModelTrainingArtifacts
import os 
import pandas as pd 
import numpy as np 
import pickle
import ast
from sklearn.ensemble import RandomForestClassifier 



class ModelTrainingPipeline:
    def __init__(self, transform_arts : DataTransformationArtifacts, training_config  : ModelTrainingPipelineConfig):
        self.config = training_config
        self.artifacts = transform_arts 
    
    @staticmethod
    def get_data(data):
        return pd.read_csv(data)
    
    def initiate_model_training(self):
        try:
            logger.info("Initiating Model Training")
            train_data = ModelTrainingPipeline.get_data(self.artifacts.train_data)
            train_data['text'] = train_data['text'].apply(ast.literal_eval)
            logger.info("Taking only the Text part ")
            os.makedirs(self.config.root_dir, exist_ok= True)
            model = self.train_the_model(train_data)
            with open(self.config.model_path , 'wb') as fp:
                pickle.dump(model, fp)
            return ModelTrainingArtifacts(
                model_path=self.config.model_path 
            )
        except Exception as e:
            raise e
        
    

    def train_the_model(self, train):
        try:
            logger.info("Initiating Model Training")
            model = RandomForestClassifier()
            x = np.array(train['text'].tolist())
            y = pd.DataFrame(train['reality'])
            model.fit(x , y)
            logger.info("Model Training Completed")
            return model 
        except Exception as e:
            raise e 


        

