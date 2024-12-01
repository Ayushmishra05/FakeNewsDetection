from src.logging import logger 
from src.entity.config_entity import IngestionPipelineConfig 
from src.entity.artifcats_entity import DataIngestionArtifacts 
import os 
import pandas as pd 
import numpy 


class DataIngestion:
    def __init__(self, data_ingestion_config : IngestionPipelineConfig):
        self.config = data_ingestion_config 
    
    @staticmethod
    def get_data(data):
        return pd.read_csv(data)
        
    def initiate_data_ingestion(self):
        try:
            logger.info("Initiating Data Ingestion")
            self.true_data = DataIngestion.get_data(self.config.true_data_path)
            self.true_data['reality'] = 1 
            self.false_data = DataIngestion.get_data(self.config.false_data_path)
            logger.info("Data Extracted")
            self.false_data['reality'] = 1
            self.merged_data = self.merge_data(self.true_data, self.false_data)
            logger.info("Data Merged")
            os.makedirs(self.config.data_ingestion_dir , exist_ok=True)
            self.merged_data.to_csv(self.config.data_ingestion_data_path, header=True, index= False)
            logger.info("Data has been saved into the Artifacts")
            return DataIngestionArtifacts(
                data_path=self.config.data_ingestion_data_path
            )
        except Exception as e:
            raise e

        
        
    def merge_data(self, data1 : pd.DataFrame , data2 : pd.DataFrame):
        try:
            logger.info("Merging Data")
            concatenated = pd.concat([data1, data2] , axis = 0).reset_index(drop=True)
            merged = concatenated.sample(frac=1 , random_state=42).reset_index(drop=True)
            return merged 
        except Exception as e:
            raise e
    
    
        
        
