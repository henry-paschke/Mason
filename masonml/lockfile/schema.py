from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class OperatingSystem(str, Enum):
    LINUX = "linux"
    WINDOWS = "windows"


class SystemInfo(BaseModel):
    os: OperatingSystem
    cuda_version: Optional[str] = None
    python_version: List[int]
