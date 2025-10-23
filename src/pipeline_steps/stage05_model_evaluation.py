import sys
from pathlib import Path

# Add parent directory to path
parent_folder = str(Path(__file__).parent.parent.parent)
sys.path.append(parent_folder)

from src.config_manager import ConfigurationManager
from src.models_module_def.model_evaluation import ModelEvaluation
from custom_logger import logger

STAGE_NAME = "Model evaluation stage"

class ModelEvaluationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            # Initialize configuration manager
            config = ConfigurationManager()

            # Try to obtain the model evaluation config from ConfigurationManager.
            # Adjust the method name below to match your ConfigurationManager implementation.
            if hasattr(config, "get_model_evaluation_config"):
                model_eval_config = config.get_model_evaluation_config()
            elif hasattr(config, "get_model_eval_config"):
                model_eval_config = config.get_model_eval_config()
            else:
                # Fallback: pass the whole config object to ModelEvaluation if that is how it's designed
                model_eval_config = config

            # Instantiate the ModelEvaluation with the config
            model_evaluator = ModelEvaluation(model_eval_config)

            # Call a plausible entry point on the ModelEvaluation instance.
            # Update these method names to match your ModelEvaluation API.
            if hasattr(model_evaluator, "initiate_model_evaluation"):
                model_evaluator.initiate_model_evaluation()
            elif hasattr(model_evaluator, "start_model_evaluation"):
                model_evaluator.start_model_evaluation()
            elif hasattr(model_evaluator, "evaluate"):
                model_evaluator.evaluate()
            else:
                raise AttributeError(
                    "ModelEvaluation instance has no known entry method. "
                    "Expected one of: 'initiate_model_evaluation', 'start_model_evaluation', 'evaluate'."
                )

        except Exception as e:
            logger.exception(f"Exception in {STAGE_NAME}: {e}")
            raise

if __name__ == '__main__':
    try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj = ModelEvaluationTrainingPipeline()
        obj.main()
        logger.info(f">>>>> stage {STAGE_NAME} completed <<<<< \n\n x========x")
    except Exception as e:
        logger.exception(e)
        raise e
