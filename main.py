from src.logging import logger 
from src.entity.config_entity import IngestionPipelineConfig, ValidationPipelineConfig, TransformationPipelineConfig, ModelTrainingPipelineConfig
logger.info("Hello World")
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_training import ModelTrainingPipeline
from src.entity.config_entity import TrainingPipelineConfig


training = TrainingPipelineConfig()
ingestion_config = IngestionPipelineConfig(training_pipeline=training)
ingestion = DataIngestion(ingestion_config)
arts = ingestion.initiate_data_ingestion()


validation_config = ValidationPipelineConfig(training_pipeline=training)
validation = DataValidation(arts, validation_config)
valid_arts = validation.initiate_data_validation()


transformation_config = TransformationPipelineConfig(training_pipeline=training)
transformation = DataTransformation(valid_arts, transformation_config)
arts = transformation.initiate_data_transformation()


model_training = ModelTrainingPipelineConfig(training)
model = ModelTrainingPipeline(arts, model_training)
model.initiate_model_training()