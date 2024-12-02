from src.logging import logger 
from src.entity.config_entity import ModelEvaluationPipelineConfig 
from src.entity.artifcats_entity import ModelEvaluationconfig, ModelTrainingArtifacts, DataTransformationArtifacts
import mlflow 
import pandas as pd 
from src.utils.common import load_pickle_file
import pickle 
from sklearn.metrics import accuracy_score, r2_score
import os 
from dotenv import load_dotenv
from mlflow import sklearn 
from src.utils.common import load_json, store_json
import ast 
import numpy as np
import dagshub

load_dotenv()
uri = os.environ['MLFLOW_TRACKING_URI']

class ModelEvaluation:
    def __init__(self, training_artifacts : ModelTrainingArtifacts , evaluation_config : ModelEvaluationPipelineConfig, data_transform : DataTransformationArtifacts):
        self.config = evaluation_config 
        self.artifacts = training_artifacts
        self.data_artifacts =  data_transform
    
    @staticmethod
    def load_data(path):
        return pd.read_csv(path)
    def initiate_model_evaluation(self):
        logger.info("Initiating Model Evaluation")
        self.model = load_pickle_file(self.artifacts.model_path)
        logger.info("Model Loaded")
        self.data = ModelEvaluation.load_data(self.data_artifacts.test_data)
        logger.info("Got the Data")
        x = self.data.drop(columns=['reality'])
        logger.info("Got X")
        y = pd.DataFrame(self.data['reality'])
        logger.info("Got Y")
        x['text'] = x['text'].apply(ast.literal_eval)
        x = np.array(x['text'].tolist())
        logger.info("Literal applied")
        pred = self.model.predict(x)
        logger.info("Prediction completed")
        dagshub.init(repo_owner='Ayushmishra05', repo_name='FakeNewsDetection', mlflow=True)
        mlflow.set_tracking_uri(uri=uri)
        logger.info("Setting URI")
        mlflow.set_experiment(self.config.exp_name)
        os.makedirs(self.config.root_dir, exist_ok=True)

        with mlflow.start_run():
            accuracy = accuracy_score(pred, y)
            r2 = r2_score(pred, y)
            metric = {
                'accuracy' : accuracy, 
                'r2' :  r2
            }
            store_json(metric, self.config.metrics_file_path)
            mlflow.log_metric('accuracy' , accuracy)
            mlflow.log_metric('r2' , r2)
            signature = mlflow.models.infer_signature(x , y)
            sklearn.log_model(sk_model = self.model, signature= signature, input_example = x, artifact_path = "Artifacts")
            return ModelEvaluationconfig(
                model_metrics= self.config.exp_name
            )
        
        