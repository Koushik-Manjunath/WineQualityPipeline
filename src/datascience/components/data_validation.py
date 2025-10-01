import os
from src.datascience.logging import logger
import pandas as pd
from src.datascience.entity.config_entity import DataValidationConfig

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self) -> bool:
        """
        Validate that all columns in the dataset match the schema.
        Returns True if validation passes, False otherwise.
        """
        try:
            # Read the dataset
            data = pd.read_csv(self.config.unzip_data_dir)
            dataset_cols = list(data.columns)

            # Convert schema list of dicts to dict: column_name -> dtype
            schema_dict = {col['name']: col['dtype'] for col in self.config.all_schema}

            validation_status = True  # assume valid unless we find a mismatch

            for col in dataset_cols:
                if col not in schema_dict:
                    logger.error(f"Column '{col}' is not in schema!")
                    validation_status = False

            # Write validation status once
            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation status: {validation_status}")

            if validation_status:
                logger.info("All columns are valid according to the schema.")
            else:
                logger.warning("Some columns are not valid according to the schema.")

            return validation_status

        except Exception as e:
            logger.exception("Error during column validation")
            raise e
