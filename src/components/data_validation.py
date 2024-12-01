from evidently.report import Report
from evidently.metrics import DatasetMissingValuesMetric, ColumnDriftMetric
import pandas as pd
from src.logging import logger 
from src.entity.config_entity import ValidationPipelineConfig 
from src.entity.artifcats_entity import DataIngestionArtifacts , DataValidationArtifacts
import os 
import pandas as pd 

class DataValidation:
    def __init__(self, ingestion_artifacts : DataIngestionArtifacts , validation_config : ValidationPipelineConfig):
        self.config = validation_config
        self.artifacts = ingestion_artifacts

    @staticmethod
    def read_data(data):
        return pd.read_csv(data)

    def initiate_data_validation(self):
        try:
            logger.info("Initiating Data Validation")
            self.reference_data = DataValidation.read_data(self.config.reference_data_path)
            self.current_data = DataValidation.read_data(self.artifacts.data_path)
            os.makedirs(self.config.root_dir, exist_ok=True)
            os.makedirs(self.config.valid_dir, exist_ok=True)
            os.makedirs(self.config.invalid_dir, exist_ok=True)

            self.data_drift_report = self.generate_report(self.reference_data, self.current_data)
            logger.info("Data Validation completed")
            if self.data_drift_report:
                logger.info("Returning Invalid Data Path")
                return DataValidationArtifacts(
                    valid_data=None,
                    valid_report=None,
                    invalid_data=self.config.invalid_data,
                    invalid_report=self.config.invalid_report
                )
            else:
                logger.info("Returning Valid Data Path")
                return DataValidationArtifacts(
                    valid_data=self.config.valid_data,
                    valid_report=self.config.valid_report,
                    invalid_data=None,
                    invalid_report=None
                )
        except Exception as e:
            raise e

    def generate_report(self, reference_data, current_data):
        report = Report(
            metrics=[# Drift check for the 'text' column
                ColumnDriftMetric(column_name='subject'),  # Drift check for the 'subject' column
                ColumnDriftMetric(column_name='reality'),  # Drift check for the 'reality' column   # Text drift check for 'text' column
            ]
        )
        report.run(reference_data=reference_data, current_data=current_data)

        report_data = report.as_dict()

        data_drift = report_data["metrics"][1]["result"]["drift_detected"]
       
        missing_values = report_data["metrics"][0]["result"].get("missing_values", 0)

        if data_drift:
            logger.info("WARNING: Significant data drift detected.")
            report.save_html(self.config.invalid_report)
            current_data.to_csv(self.config.invalid_data, header = True, index = False)
            logger.info(f"Data is being saved to INValid Dir = {self.config.invalid_data}")
            return True
        elif missing_values > 0:
            logger.info(f"WARNING: Missing values detected. Total: {missing_values}")
            report.save_html(self.config.invalid_report)
            current_data.to_csv(self.config.invalid_data, header = True, index = False)
            logger.info(f"Data is being saved to INValid Dir = {self.config.invalid_data}")
            return True
        else:
            logger.info("Data is valid.")
            report.save_html(self.config.valid_report )
            current_data.to_csv(self.config.valid_data, header = True, index = False)
            logger.info(f"Data is being saved to Valid Dir = {self.config.valid_data}")
            return False
