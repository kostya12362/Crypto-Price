from aiohttp import ClientSession
from starlette.requests import Request


def client_session_dep(request: Request) -> ClientSession:
    return request.app.state.client_session
