import sys
from pathlib import Path

# Add parent directory to path
parent_folder = str(Path(__file__).parent.parent.parent)
sys.path.append(parent_folder)

from src.config_manager import ConfigurationManager
from src.data_module_def.data_validation import DataValidation
from custom_logger import logger

STAGE_NAME = "Data Validation stage"

class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        # Create configuration manager
        config = ConfigurationManager()

        # Instantiate the DataValidation component and run it.
        # Replace 'initiate_data_validation' with the actual method name used in your DataValidation class
        data_validation = DataValidation(config=config)
        try:
            data_validation.initiate_data_validation()
        except AttributeError:
            # Fallback to a commonly used alternative name if present
            if hasattr(data_validation, "validate"):
                data_validation.validate()
            else:
                # Re-raise with a clearer message to help debugging
                raise AttributeError(
                    "DataValidation instance has no 'initiate_data_validation' or 'validate' method. "
                    "Check the DataValidation class interface."
                )

if __name__ == '__main__':
    try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj = DataValidationTrainingPipeline()
        obj.main()
        logger.info(f">>>>> stage {STAGE_NAME} completed <<<<<\n\nx=======x")
    except Exception as e:
        logger.exception(e)
        raise e
