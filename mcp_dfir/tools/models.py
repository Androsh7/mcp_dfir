"""Defines commonly used models"""

# Standard libraries
from datetime import datetime
from typing import Literal

# Third-party libraries
from pydantic import BaseModel, Field


class FileDetails(BaseModel):
    name: str = Field(examples=["example.mem"])
    path: str = Field(examples=["/evidence/example.mem"])
    size: int = Field(ge=0, examples=[1502])


def date_as_str() -> str:
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


class CommandRecordSummary(BaseModel):
    number: int = Field(examples=[1])
    command: str = Field(examples=["vol -f capture.mem linux.pslist"])
    date_run: str = Field(default_factory=date_as_str, examples=["01/01/2024 12:00:00"])
    exit_code: int = Field(examples=[0])


class CommandRecord(BaseModel):
    command: str = Field(examples=["vol -f capture.mem linux.pslist"])
    date_run: str = Field(default_factory=date_as_str, examples=["01/01/2024 12:00:00"])
    result: str = Field(
        default="",
        examples=[
            "Volatility 3 Framework 2.27.0\n\nPID\tPPID\tImageFileName\tOffset(V)\tThreads\tHandles\tSessionId\tWow64\tCreateTime\tExitTime\tFile output\n\n4\t0\tSystem\t"
        ],
    )
    exit_code: int = Field(examples=[0])

    def summary(self, number: int) -> CommandRecordSummary:
        return CommandRecordSummary(
            number=number,
            command=self.command,
            date_run=self.date_run,
            exit_code=self.exit_code,
        )


class AnalystNoteSummary(BaseModel):
    title: str = Field(examples=["Found WannaCry ransomware executable"])
    status: Literal["benign", "malicious", "unknown"] = Field(examples=["malicious"])
    tags: list[str] = Field(examples=[["malware", "ransomware", "executable"]])


class AnalystNote(BaseModel):
    title: str = Field(examples=["Found WannaCry ransomware executable"])
    status: Literal["benign", "malicious", "unknown"] = Field(examples=["malicious"])
    tags: list[str] = Field(examples=[["malware", "ransomware", "executable"]])
    description: str = Field(
        examples=[
            "# Found WannaCry ransomware executable\nFound WannaCry executable after running <COMMAND>, follow-on analysis needed"
        ]
    )

    def summary(self) -> AnalystNoteSummary:
        return AnalystNoteSummary(
            title=self.title,
            status=self.status,
            tags=self.tags,
        )
