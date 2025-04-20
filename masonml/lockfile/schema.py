from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
import yaml


class System_info(BaseModel):
    os: str
    cuda_version: Optional[str] = None
    python_version: List[int]


class Lock_file(BaseModel):
    system_info: System_info
    conda_env_name: str
    packages: List[str] = []


def save_lock_file(lock_file: Lock_file, file_path: str) -> None:
    """
    Save the lock file to a YAML file.
    """
    with open(file_path, "w") as file:
        yaml.dump(lock_file.model_dump(), file, default_flow_style=False)


def load_lock_file(file_path: str) -> Lock_file:
    """
    Load the lock file from a YAML file.
    """
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return Lock_file(**data)
