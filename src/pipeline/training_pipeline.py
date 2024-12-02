from src.logging import logger 
from src.entity.config_entity import IngestionPipelineConfig, ValidationPipelineConfig, TransformationPipelineConfig, ModelTrainingPipelineConfig, ModelEvaluationPipelineConfig
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_training import ModelTrainingPipeline
from src.entity.config_entity import TrainingPipelineConfig
from src.components.model_evaluation import ModelEvaluation




class Training:
    def __init__(self):
        self.training = TrainingPipelineConfig()
    
    def ingestion_pipe(self, training):
        ingestion_config = IngestionPipelineConfig(training_pipeline=training)
        ingestion = DataIngestion(ingestion_config)
        arts = ingestion.initiate_data_ingestion()
        return arts 
    
    def validation_pipe(self, training, arts):
        validation_config = ValidationPipelineConfig(training_pipeline=training)
        validation = DataValidation(arts, validation_config)
        valid_arts = validation.initiate_data_validation()
        return valid_arts
    
    def transformation(self, valid_arts, training):
        transformation_config = TransformationPipelineConfig(training_pipeline=training)
        transformation = DataTransformation(valid_arts, transformation_config)
        arts = transformation.initiate_data_transformation()
        return arts 
    
    def model_training(self, arts, training):
        model_training = ModelTrainingPipelineConfig(training)
        model = ModelTrainingPipeline(arts, model_training)
        model_arts = model.initiate_model_training()
        return model_arts
    
    def evaluation(self, model_arts, arts, training):
        model_evaluation = ModelEvaluationPipelineConfig(training)
        eval= ModelEvaluation(model_arts, model_evaluation, arts)
        evalarts= eval.initiate_model_evaluation()
        return evalarts
    
    def train(self):
        logger.info("Initating Model Training")
        ingest = self.ingestion_pipe(self.training)
        logger.info("Data Ingestion Successsfully Completed")
        valid = self.validation_pipe(self.training, ingest)
        logger.info("Data Validation Successsfully Completed")
        transform = self.transformation(valid, self.training)
        logger.info("Data Transformation Successsfully Completed")
        training_arts = self.model_training(transform, self.training)
        logger.info("Model Training Successfully Completed")
        evalarts = self.evaluation(training_arts, transform, self.training)
        logger.info("Model Evaluation Successfully Completed")

























