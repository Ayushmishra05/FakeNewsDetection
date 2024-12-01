from dataclasses import dataclass 

@dataclass
class DataIngestionArtifacts:
    data_path  : str

@dataclass 
class DataValidationArtifacts:
    valid_data : str
    valid_report : str 
    invalid_data : str 
    invalid_report : str 

@dataclass
class DataTransformationArtifacts:
    train_data : str 
    test_data : str 
    

@dataclass
class ModelTrainingArtifacts:
    model_path : str

@dataclass 
class ModelEvaluationconfig:
    model_metrics : str 
     


