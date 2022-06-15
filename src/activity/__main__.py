import click
import structlog
import uvloop

from activity.app import init
from activity.cli.server import server
from activity.logging import configure_logging


@click.group()
@click.option("--debug", is_flag=True, default=False)
@click.pass_context
def cli(ctx, debug: bool = False) -> None:
    """Main application entry point for command line interface."""
    uvloop.install()

    configure_logging(app_name="activity", debug=debug)
    logger = structlog.get_logger("activity")

    app = init("activity", logger=logger)

    ctx.obj["app"] = app
    ctx.obj["logger"] = logger


cli.add_command(server, name="server")


if __name__ == "__main__":
    cli(obj={})
