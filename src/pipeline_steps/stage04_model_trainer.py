import sys
from pathlib import Path

# Add parent directory to path
parent_folder = str(Path(__file__).parent.parent.parent)
sys.path.append(parent_folder)

from src.config_manager import ConfigurationManager
from src.models_module_def.model_trainer import ModelTrainer
from custom_logger import logger

STAGE_NAME = "Model trainer stage"

class ModelTrainerTrainingPipeline:
    def __init__(self):
        # initialize configuration manager once
        self.config = ConfigurationManager()

    def main(self):
        """
        Orchestrate model training:
        - obtain trainer configuration if available,
        - instantiate ModelTrainer,
        - call the trainer's run/train method.
        The code is defensive about method names to make it easier to plug into existing implementations.
        """
        try:
            logger.info("Preparing model trainer configuration")

            trainer_config = None
            # try common config-getter method names; adjust to your repo's API if different
            if hasattr(self.config, "get_model_trainer_config"):
                trainer_config = self.config.get_model_trainer_config()
            elif hasattr(self.config, "get_training_config"):
                trainer_config = self.config.get_training_config()
            else:
                # no specific trainer config method found; fall back to passing the whole config object
                logger.debug("No specific model trainer config getter found; passing ConfigurationManager instance to ModelTrainer")

            # instantiate ModelTrainer; adapt constructor args if your ModelTrainer expects something else
            if trainer_config is not None:
                trainer = ModelTrainer(trainer_config)
            else:
                trainer = ModelTrainer(self.config)

            logger.info("Starting model training")
            # try common training method names; replace with the real one if known
            if hasattr(trainer, "initiate_model_trainer"):
                trainer.initiate_model_trainer()
            elif hasattr(trainer, "train"):
                trainer.train()
            elif hasattr(trainer, "run"):
                trainer.run()
            else:
                logger.warning("ModelTrainer has no known run method (tried: initiate_model_trainer, train, run). Please call the appropriate method.")
        except Exception as e:
            logger.exception("Error in ModelTrainerTrainingPipeline.main")
            raise

if __name__ == '__main__':
    try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj = ModelTrainerTrainingPipeline()
        obj.main()
        logger.info(f">>>>> stage {STAGE_NAME} completed <<<<< \n\n x========x")
    except Exception as e:
        logger.exception(e)
        raise e
