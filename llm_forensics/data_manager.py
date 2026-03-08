"""Defines the data manager class"""

# Standard libraries
import json
from datetime import datetime

# Third-party libraries
from pydantic import BaseModel, Field

# Project libraries
from llm_forensics.constants import COMMAND_LIST_PATH


def date_as_str() -> str:
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


class CommandRecordTruncated(BaseModel):
    command: str = Field(examples=["vol -f capture.mem linux.pslist"])
    date_run: str = Field(default_factory=date_as_str, examples=[datetime.now()])
    result: str = Field(
        examples=["Volatility 3 Framework 2.27.0\n\nPID\tPPID\tImageFileName\tOffset(V)..."],
    )


class CommandRecord(BaseModel):
    command: str = Field(examples=["vol -f capture.mem linux.pslist"])
    date_run: str = Field(default_factory=date_as_str, examples=[datetime.now()])
    result: str = Field(
        default="",
        examples=[
            "Volatility 3 Framework 2.27.0\n\nPID\tPPID\tImageFileName\tOffset(V)\tThreads\tHandles\tSessionId\tWow64\tCreateTime\tExitTime\tFile output\n\n4\t0\tSystem\t"
        ],
    )

    def truncate(self, length: int | None) -> CommandRecordTruncated:
        return CommandRecordTruncated(
            command=self.command,
            date_run=self.date_run,
            result=f"{self.result[:length]}..." if length else self.result,
        )


class DataManager(BaseModel):
    command_list: list[CommandRecord] = Field(default_factory=list, init=False)

    def model_post_init(self, __context):
        if COMMAND_LIST_PATH.exists():
            self.load_from_file()

    def dump_to_file(self):
        with open(file=COMMAND_LIST_PATH, mode="w", encoding="utf-8") as command_file:
            json.dump(
                [record.model_dump() for record in self.command_list],
                command_file,
            )

    def load_from_file(self):
        with open(file=COMMAND_LIST_PATH, encoding="utf-8") as command_file:
            for command_record_dict in json.load(command_file):
                self.command_list.append(CommandRecord.model_validate(command_record_dict))

    def add(self, command_record: CommandRecord) -> CommandRecord:
        self.command_list.append(command_record)
        self.dump_to_file()
        return command_record

data_manager = DataManager()
