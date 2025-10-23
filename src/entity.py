from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any


@dataclass(frozen=True)
class DataIngestionConfig:
    """
    Configuration for the data ingestion step.
    """
    root_dir: Path
    source_url: str
    local_data_file: Path
    unzip_dir: Path


@dataclass(frozen=True)
class DataValidationConfig:
    """
    Configuration for the data validation step.
    """
    root_dir: Path
    STATUS_FILE: str
    unzip_data_dir: Path
    all_schema: Dict[str, Any]


@dataclass(frozen=True)
class DataTransformationConfig:
    """
    Configuration for the data transformation step.
    """
    root_dir: Path
    data_path: Path


@dataclass(frozen=True)
class ModelTrainerConfig:
    """
    Configuration for the model training step.
    """
    root_dir: Path
    X_train_path: Path
    y_train_path: Path
    X_test_path: Path
    y_test_path: Path
    model_name: str
    alpha: float
    l1_ratio: float


@dataclass(frozen=True)
class ModelEvaluationConfig:
    """
    Configuration for the model evaluation step.
    """
    root_dir: Path
    X_test_path: Path
    y_test_path: Path
    model_path: Path
    metric_file_name: Path
    all_params: Dict[str, Any]
    mlflow_uri: str
