import sys
from pathlib import Path

# Add parent directory to path
parent_folder = str(Path(__file__).parent.parent.parent)
sys.path.append(parent_folder)

from src.config_manager import ConfigurationManager
from src.data_module_def.data_transformation import DataTransformation
from custom_logger  import logger

STAGE_NAME = "Data Transformation stage"

class DataTransformationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            status_file = Path("data/status.txt")
            status = ""
            if status_file.exists():
                try:
                    status = status_file.read_text().strip().split(" ")[-1]
                except Exception:
                    logger.warning("Could not parse data/status.txt, continuing with transformation.")
                    status = ""
            else:
                logger.info("data/status.txt not found; will run data transformation.")

            # Decide whether to run transformation based on status value
            if status.lower() != "data_transformation_completed":
                logger.info("Starting data transformation...")

                # Get configuration for data transformation
                config_manager = ConfigurationManager()
                # adjust the method name if your ConfigurationManager uses a different API
                data_transformation_config = config_manager.get_data_transformation_config()

                # Run the transformation
                data_transformation = DataTransformation(data_transformation_config)
                # adjust the method name if your DataTransformation uses a different API
                data_transformation.initiate_data_transformation()

                # Update status file to mark this stage as completed
                status_file.parent.mkdir(parents=True, exist_ok=True)
                status_file.write_text("data_transformation_status: data_transformation_completed\n")
                logger.info("Data transformation completed and status file updated.")
            else:
                logger.info("Skipping data transformation; already completed according to status file.")
        except Exception as e:
            logger.exception("Exception in DataTransformationTrainingPipeline.main")
            raise e

if __name__ == '__main__':
    try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj =  DataTransformationTrainingPipeline()
        obj.main()
        logger.info(f">>>>> stage {STAGE_NAME} completed <<<<<\n\nx=======x")
    except Exception as e:
        logger.exception(e)
        raise e
