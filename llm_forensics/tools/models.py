"""Defines commonly used models"""

# Third-party libraries
from pydantic import BaseModel, Field


class FileDetails(BaseModel):
    name: str = Field(examples=["example.mem"])
    path: str = Field(examples=["/evidence/example.mem"])
    size: int = Field(ge=0, examples=["1502"])
