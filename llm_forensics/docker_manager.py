"""Defines all functions to run commands on the docker container"""

# Standard libraries
from typing import Generator

# Third-party libraries
from attrs import define, field, validators
from loguru import logger
from mcp.server.fastmcp import Context
from python_on_whales import DockerClient, Container
from python_on_whales.exceptions import NoSuchContainer

# Project libraries
from llm_forensics.constants import DOCKER_IMAGE, DOCKER_NAME, ANALYSIS_DIRECTORY, EVIDENCE_DIRECTORY

@define
class DockerManager:
    docker: DockerClient = field(validator=validators.instance_of(DockerClient), init=False)
    container: Container = field(validator=validators.optional(validators.instance_of(Container)), init=False)

    def __attrs_post_init__(self):
        self.docker = DockerClient()
        self.container = None

    def start_forensic_container(self):
        logger.info("Starting forensics docker container")

        try:
            self.container = self.docker.container.inspect(DOCKER_NAME)
            if self.container.state.running:
                logger.info("Forensics container already running")
                return

            logger.info("Forensics container exists but is stopped, starting it")
            self.docker.container.start(DOCKER_NAME)
            return

        except NoSuchContainer:
            logger.info("Forensics container does not exist, creating one")

        self.container = self.docker.run(
            DOCKER_IMAGE,
            name=DOCKER_NAME,
            detach=True,
            remove=False,
            volumes=[(EVIDENCE_DIRECTORY, "/evidence", "ro")],
        )
    

    def stop_forensic_container(self):
        if self.container is not None:
            logger.info(f'Stopping forensics docker container')
            self.container.stop()

    def exec_stream(self, ctx: Context, command_list: list[str]) -> str:
        if self.container is None:
            raise RuntimeError("No docker container is currently running")

        ctx.report_progress(f'Running command {" ".join(command_list)}')
        return self.docker.execute(
            self.container,
            command_list,
        )

docker_manager = DockerManager()
