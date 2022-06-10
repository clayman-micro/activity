import socket

import pkg_resources
from aiohttp import web

from activity.web import meta


def init(app_name: str) -> web.Application:
    """Create application instance.

    Args:
        app_name: Application name.

    Return:
        New application instance.
    """
    app = web.Application()

    app["hostname"] = socket.gethostname()
    app["distribution"] = pkg_resources.get_distribution(app_name)

    app.router.add_get("/-/meta", handler=meta.index, name="meta", allow_head=False)
    app.router.add_get("/-/health", handler=meta.health, name="health", allow_head=False)

    return app
