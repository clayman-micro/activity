import click
import uvloop

from activity.app import init
from activity.cli.server import server


@click.group()
@click.option("--debug", is_flag=True, default=False)
@click.pass_context
def cli(ctx, debug: bool = False) -> None:
    """Main application entry point for command line interface.

    Args:
        ctx: Current command line application context.
        debug: Run application in debug mode.
    """
    ctx.obj["app"] = init("activity", debug=debug)


cli.add_command(server, name="server")


if __name__ == "__main__":
    uvloop.install()

    cli(obj={})
