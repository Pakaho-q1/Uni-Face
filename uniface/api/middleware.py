import sys
import os
import base64
from functools import wraps
from uniface.core.state import state

# Silence asyncio Proactor connection reset errors (WinError 10054) on websocket disconnect
if sys.platform == 'win32':
    from asyncio.proactor_events import _ProactorBasePipeTransport
    
    def silence_event_loop_closed(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except (ConnectionResetError, RuntimeError):
                pass
        return wrapper
        
    _ProactorBasePipeTransport._call_connection_lost = silence_event_loop_closed(_ProactorBasePipeTransport._call_connection_lost)

class BasicAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] not in ["http", "websocket"]:
            return await self.app(scope, receive, send)
            
        if not state.auth:
            return await self.app(scope, receive, send)

        headers = dict(scope.get("headers", []))
        auth_header = headers.get(b"authorization", b"").decode("utf-8")
        
        parts = state.auth.split(":", 1)
        if len(parts) == 2:
            expected_user, expected_pass = parts
        else:
            expected_user, expected_pass = "admin", state.auth
            
        expected = f"Basic {base64.b64encode(f'{expected_user}:{expected_pass}'.encode()).decode()}"
        
        if auth_header != expected:
            if scope["type"] == "http":
                await send({
                    "type": "http.response.start",
                    "status": 401,
                    "headers": [(b"www-authenticate", b'Basic realm="Uni-Face"')]
                })
                await send({
                    "type": "http.response.body",
                    "body": b"Unauthorized",
                })
                return
            elif scope["type"] == "websocket":
                await send({"type": "websocket.close", "code": 1008})
                return
                
        await self.app(scope, receive, send)
