"""Defines all functions to run commands on the docker container"""

# Third-party libraries
from attrs import define, field, validators
from loguru import logger
from mcp.server.fastmcp import Context
from python_on_whales import Container, DockerClient
from python_on_whales.exceptions import DockerException, NoSuchContainer

# Project libraries
from mcp_dfir.config import config
from mcp_dfir.data_manager import command_history_manager
from mcp_dfir.tools.models import CommandRecord, CommandRecordSummary


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
            self.container = self.docker.container.inspect(config.docker_config.container_name)

            if self.container.state.running:
                logger.info("Forensics container already running")
                return

            logger.info("Forensics container exists but is stopped, starting it")
            self.docker.container.start(config.docker_config.container_name)
            return

        except NoSuchContainer:
            logger.info("Forensics container does not exist, creating one")

        volumes = [
            (volume_mount.external_path, volume_mount.internal_path, volume_mount.permissions)
            for volume_mount in list(config.docker_volumes)
        ]
        self.container = self.docker.run(
            config.docker_config.image_name,
            name=config.docker_config.container_name,
            detach=True,
            remove=False,
            volumes=volumes,
            networks=["none"],
        )

    def stop_forensic_container(self):
        if self.container is not None:
            logger.info("Stopping forensics docker container")
            self.container.stop()

    def clear_forensic_container(self):
        if self.container is not None:
            logger.info("Clearing forensics docker container")
            self.container.stop()
            self.container.remove()
            self.container = None

    def exec_stream(self, ctx: Context, command_list: list[str]) -> CommandRecordSummary:
        if self.container is None:
            raise RuntimeError("No docker container is currently running")

        ctx.report_progress(f"Running command {' '.join(command_list)}")
        output = []
        exit_code = 0
        try:
            for stream, data in self.docker.execute(self.container, command_list, stream=True):
                if stream == "stdout":
                    output.append(data.decode())
        except DockerException as ex:
            exit_code = ex.return_code if ex.return_code is not None else 1
            output.append(str(ex))
        result = "".join(output)
        return command_history_manager.add_command(
            CommandRecord(
                command=" ".join(command_list),
                result=result,
                exit_code=exit_code,
            )
        )


docker_manager = DockerManager()
