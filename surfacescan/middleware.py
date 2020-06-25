import time
import typing

from starlette import types


class RequestStats:
    """Request statistics middleware which tracks duration of each request.
    """

    def __init__(
        self,
        app: types.ASGIApp,
        track: typing.Callable[[float], None],
    ) -> None:
        self.app = app
        self.track = track

    async def __call__(
        self,
        scope: types.Scope,
        receive: types.Receive,
        send: types.Send,
    ) -> None:
        started = time.time()
        await self.app(scope, receive, send)
        duration = time.time() - started
        self.track(duration)
