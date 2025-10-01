import os
import sys
import json
import yaml
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any, Union
from box.exceptions import BoxValueError

from src.datascience.logging import logger


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Read YAML file and return ConfigBox object."""
    try:
        with open(path_to_yaml, "r") as yaml_file:
            content = yaml.safe_load(yaml_file) or {}
            logger.info(f"YAML file loaded successfully: {path_to_yaml}")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("YAML file is empty")
    except Exception as e:
        logger.error(f"Error reading YAML file {path_to_yaml}: {e}")
        raise e



@ensure_annotations
def create_directories(path_to_directories: list, verbose: bool = True):
    """Create multiple directories."""
    for path in path_to_directories:
        if not isinstance(path, (str, Path)):
            raise TypeError(f"Path must be str or Path, got {type(path)}")
        Path(path).mkdir(parents=True, exist_ok=True)
        if verbose:
            logger.info(f"Created directory at: {path}")



@ensure_annotations
def save_json(path: Path, data: dict):
    """Save dictionary as JSON file."""
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        logger.info(f"JSON file saved at: {path}")
    except Exception as e:
        logger.error(f"Error saving JSON file {path}: {e}")
        raise e


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """Load JSON file and return ConfigBox object."""
    try:
        with open(path, "r") as f:
            content = json.load(f)
        logger.info(f"JSON file loaded successfully from: {path}")
        return ConfigBox(content)
    except Exception as e:
        logger.error(f"Error loading JSON file {path}: {e}")
        raise e


@ensure_annotations
def save_bin(data: Any, path: Path):
    """Save Python object as binary file."""
    try:
        joblib.dump(value=data, filename=path)
        logger.info(f"Binary file saved at: {path}")
    except Exception as e:
        logger.error(f"Error saving binary file {path}: {e}")
        raise e


@ensure_annotations
def load_bin(path: Path) -> Any:
    """Load Python object from binary file."""
    try:
        data = joblib.load(path)
        logger.info(f"Binary file loaded from: {path}")
        return data
    except Exception as e:
        logger.error(f"Error loading binary file {path}: {e}")
        raise e
