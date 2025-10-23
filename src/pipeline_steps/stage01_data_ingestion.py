import sys
from pathlib import Path
from typing import Any, Optional

# Add parent directory to path
parent_folder = str(Path(__file__).parent.parent.parent)
sys.path.append(parent_folder)

from custom_logger import logger
from src.config_manager import ConfigurationManager
from src.data_module_def.data_ingestion import DataIngestion

# logging the parent directory
logger.info(f"Parent folder: {parent_folder}")

# Define stage name
STAGE_NAME = "Data Ingestion stage"


class DataIngestionPipeline:
    def __init__(self) -> None:
        """
        Pipeline wrapper for the data ingestion step.
        """
        self.config_manager = ConfigurationManager()

    def main(self) -> Optional[Any]:
        """
        Run the data ingestion step.

        Returns:
            The artifact or return value from the data ingestion step, if any.
        """
        # Try to obtain a specific data ingestion config if your ConfigurationManager
        # exposes such a method. If not, pass the full config manager to DataIngestion.
        try:
            data_ingestion_config = None
            if hasattr(self.config_manager, "get_data_ingestion_config"):
                data_ingestion_config = self.config_manager.get_data_ingestion_config()
                logger.debug("Obtained data_ingestion_config from ConfigurationManager.")
            else:
                logger.debug("ConfigurationManager has no get_data_ingestion_config(); passing manager to DataIngestion.")

            # Instantiate DataIngestion with whatever constructor it expects.
            # Prefer passing the specific config if available.
            if data_ingestion_config is not None:
                ingestion = DataIngestion(config=data_ingestion_config)
            else:
                ingestion = DataIngestion(config_manager=self.config_manager)

            # Call the ingestion execution method. Try common names for robustness.
            result = None
            if hasattr(ingestion, "initiate_data_ingestion"):
                result = ingestion.initiate_data_ingestion()
            elif hasattr(ingestion, "start"):
                result = ingestion.start()
            elif hasattr(ingestion, "run"):
                result = ingestion.run()
            else:
                logger.warning(
                    "DataIngestion instance has no known entrypoint (initiate_data_ingestion/start/run). "
                    "Please call the correct method manually."
                )

            logger.info("Data ingestion step finished.")
            return result

        except Exception as exc:
            logger.exception("Error while running data ingestion pipeline.")
            raise exc


if __name__ == '__main__':
    try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj = DataIngestionPipeline()
        obj.main()
        logger.info(f">>>>> stage {STAGE_NAME} completed <<<<<\n\nx=======x")

    except Exception as e:
        logger.exception(e)
        raise e
