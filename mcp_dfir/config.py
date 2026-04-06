"""Defines the config object"""

# Standard libraries
from pathlib import Path

# Third-party libraries
from attrs import define, field, validators

# Project libraries
from mcp_dfir.constants import VERSION


@define
class DockerVolume:
    name: str = field(validator=validators.instance_of(str))
    internal_path: str = field(validator=validators.instance_of(str))
    external_path: Path = field(validator=validators.instance_of(Path))
    permissions: str = field(validator=validators.instance_of(str))


@define
class DockerConfig:
    container_name: str = field(validator=validators.instance_of(str))
    image_name: str = field(validator=validators.instance_of(str))


@define
class Config:
    working_directory: Path = field(default=Path.cwd(), validator=validators.instance_of(Path))

    # Directories
    analysis_directory: Path = field(init=False, validator=validators.instance_of(Path))
    artifact_directory: Path = field(init=False, validator=validators.instance_of(Path))
    symbols_directory: Path = field(init=False, validator=validators.instance_of(Path))
    evidence_directory: Path = field(init=False, validator=validators.instance_of(Path))

    # Command history
    command_history_json: Path = field(init=False, validator=validators.instance_of(Path))
    command_record_directory: Path = field(init=False, validator=validators.instance_of(Path))

    # Analyst notes
    analyst_notes_list_json: Path = field(init=False, validator=validators.instance_of(Path))
    analyst_notes_directory: Path = field(init=False, validator=validators.instance_of(Path))

    # Docker
    docker_volumes: list[DockerVolume] = field(
        init=False,
        validator=validators.deep_iterable(
            member_validator=validators.instance_of(DockerVolume), iterable_validator=validators.instance_of(list)
        ),
    )
    docker_config: DockerConfig = field(init=False, validator=validators.instance_of(DockerConfig))

    def load(self, working_directory: Path):

        # Directories
        self.working_directory = working_directory
        self.analysis_directory = self.working_directory / "analysis"
        self.artifact_directory = self.working_directory / "artifacts"
        self.symbols_directory = self.working_directory / "symbols"
        self.evidence_directory = self.working_directory / "evidence"

        # Command history
        self.command_history_json = self.analysis_directory / "command_history.json"
        self.command_record_directory = self.analysis_directory / "command_history"

        # Analyst notes
        self.analyst_notes_list_json = self.analysis_directory / "analyst_notes.json"
        self.analyst_notes_directory = self.analysis_directory / "analyst_notes"

        # Docker
        self.docker_volumes = [
            DockerVolume(
                name="evidence", internal_path="/evidence", external_path=self.evidence_directory, permissions="ro"
            ),
            DockerVolume(
                name="analysis", internal_path="/analysis", external_path=self.analysis_directory, permissions="ro"
            ),
            DockerVolume(
                name="symbols", internal_path="/symbols", external_path=self.symbols_directory, permissions="rw"
            ),
            DockerVolume(
                name="artifacts", internal_path="/artifacts", external_path=self.artifact_directory, permissions="rw"
            ),
        ]
        self.docker_config = DockerConfig(
            container_name=f"{self.working_directory.name.replace(' ', '_')}-forensics",
            image_name=f"androsh7/forensics-docker:{VERSION}",
        )


config = Config()
