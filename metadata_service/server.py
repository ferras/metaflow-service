import asyncio
import os

from aiohttp import web
from aiohttp_swagger import *

from metadata_service.api.run import RunApi
from metadata_service.api.flow import FlowApi

from metadata_service.api.step import StepApi
from metadata_service.api.task import TaskApi
from metadata_service.api.artifact import ArtificatsApi
from metadata_service.api.admin import AuthApi

from metadata_service.api.metadata import MetadataApi
from metadata_service.data.postgres_async_db import AsyncPostgresDB


def app(loop=None):

    loop = loop or asyncio.get_event_loop()
    app = web.Application(loop=loop)
    async_db = AsyncPostgresDB()
    loop.run_until_complete(async_db._init())
    FlowApi(app)
    RunApi(app)
    StepApi(app)
    TaskApi(app)
    MetadataApi(app)
    ArtificatsApi(app)
    AuthApi(app)
    setup_swagger(app)
    return app


def main():
    loop = asyncio.get_event_loop()
    the_app = app(loop)
    handler = the_app.make_handler()
    port = os.environ.get("MF_METADATA_PORT", 8080)
    host = str(os.environ.get("MF_METADATA_HOST", "0.0.0.0"))
    f = loop.create_server(handler, host, port)

    srv = loop.run_until_complete(f)
    print("serving on", srv.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
    # loop = asyncio.get_event_loop()
    # the_app = app(loop)
    # handler = the_app.make_handler()
    # port = os.environ.get("MF_METADATA_PORT", 8080)
    # host = str(os.environ.get("MF_METADATA_HOST", "0.0.0.0"))
    # f = loop.create_server(handler, host, port)
    #
    # srv = loop.run_until_complete(f)
    # print("serving on", srv.sockets[0].getsockname())
    # try:
    #     loop.run_forever()
    # except KeyboardInterrupt:
    #     pass
