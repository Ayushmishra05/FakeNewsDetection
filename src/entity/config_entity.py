from src.logging import logger 
from datetime import datetime 
from src.constants import (DATA_INGESTION_DIR , DATA_INGESTION_DATA_PATH, TRUE_DATA_PATH, 
                           FALSE_DATA_PATH, VALIDATION_ROOT_DATA, VALID_ROOT, VALID_DATA, VALID_REPORT, 
                           INVALID_DATA, INVALID_REPORT, INVALID_ROOT, REFERENCE_DATA_PATH, TRANSFORMATION_ROOT_DIR, TRANSFORMATION_TEST_DIR
                           , TRANSFORMATION_TEST_DIR, TRANSFORMATION_TEST_PATH, TRANSFORMATION_TRAIN_DIR, TRANSFORMATION_TRAIN_PATH, 
                           MODEL_ROOT_DIR, MODEL_PATH , MODEL_REPORT_PATH, MLFLOW_EXP_NAME)
import os 


class TrainingPipelineConfig:
    def __init__(self):
        dirname = "Artifacts" 
        inside_dirname = f"{datetime.now().strftime("%H_%M_%d_%m_%Y")}"

        self.foldername = f"{dirname}/{inside_dirname}/" 
        os.makedirs(self.foldername, exist_ok=True) 


class IngestionPipelineConfig:
    def __init__(self , training_pipeline : TrainingPipelineConfig):
        self.folder = training_pipeline.foldername 
        self.data_ingestion_dir = os.path.join(self.folder, DATA_INGESTION_DIR)
        self.data_ingestion_data_path = os.path.join(self.data_ingestion_dir , DATA_INGESTION_DATA_PATH)
        self.true_data_path = TRUE_DATA_PATH
        self.false_data_path = FALSE_DATA_PATH


class ValidationPipelineConfig:
    def __init__(self, training_pipeline : TrainingPipelineConfig):
        self.root_dir = os.path.join(training_pipeline.foldername , VALIDATION_ROOT_DATA)
        self.valid_dir = os.path.join(self.root_dir , VALID_ROOT)
        self.invalid_dir = os.path.join(self.root_dir , INVALID_ROOT)
        self.valid_data = os.path.join(self.valid_dir , VALID_DATA)
        self.valid_report = os.path.join(self.valid_dir , VALID_REPORT)
        self.invalid_data = os.path.join(self.invalid_dir, INVALID_DATA)
        self.invalid_report = os.path.join(self.invalid_dir, INVALID_REPORT)
        self.reference_data_path = REFERENCE_DATA_PATH
        

class TransformationPipelineConfig:
    def __init__(self, training_pipeline : TrainingPipelineConfig):
        self.root_dir = os.path.join(training_pipeline.foldername , TRANSFORMATION_ROOT_DIR)
        self.train_dir = os.path.join(self.root_dir , TRANSFORMATION_TRAIN_DIR)
        self.test_dir = os.path.join(self.root_dir , TRANSFORMATION_TEST_DIR)
        self.train_path = os.path.join(self.train_dir , TRANSFORMATION_TRAIN_PATH)
        self.test_path = os.path.join(self.test_dir , TRANSFORMATION_TEST_PATH)

class ModelTrainingPipelineConfig:
    def __init__(self, training_pipeline : TrainingPipelineConfig):
        self.root_dir = os.path.join(training_pipeline.foldername, MODEL_ROOT_DIR)
        self.model_path = os.path.join(self.root_dir, MODEL_PATH)
        self.model_report = os.path.join(self.root_dir , MODEL_REPORT_PATH)
        
    

class ModelEvaluationPipelineConfig:
    def __init__(self, training_pipeline : TrainingPipelineConfig):
        self.root_dir = os.path.join(training_pipeline.foldername, )


        
        
