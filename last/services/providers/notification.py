import typing

from fastapi import WebSocket
from starlette.requests import Request
from starlette.websockets import WebSocketDisconnect

from last.services.providers import Provider
from last.services.template import templates
from last.services.websockets import ConnectionManager

if typing.TYPE_CHECKING:
    from last.services.app import FastAPIAdmin


class NotificationProvider(Provider):
    name = "notification_provider"

    def __init__(self):
        self.manager = ConnectionManager()

    async def broadcast(self, data: dict):
        content = templates.get_template("providers/notification/item.html").render(
            **data
        )
        await self.manager.broadcast(content)

    async def register(self, app: "FastAPIAdmin"):
        await super(NotificationProvider, self).register(app)

        @app.post("/notification")
        async def send_notification(request: Request):
            """
            {
                "title": "test",
                "content": "//avatars.githubusercontent.com/u/13377178?v=4",
                "image": "https://avatars.githubusercontent.com/u/13377178?v=4",
                "link": "https://fastapi-admin.github.io"
            }
            """
            data = await request.json()
            await self.broadcast(data)

        @app.websocket("/notification")
        async def notification(websocket: WebSocket):
            await self.manager.connect(websocket)
            try:
                while True:
                    await websocket.receive_text()
            except WebSocketDisconnect:
                self.manager.disconnect(websocket)
