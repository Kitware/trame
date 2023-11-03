import argparse
import asyncio
import importlib
import uuid

import aiohttp
import aiohttp.web as aiohttp_web


class MultiClientServer:
    def __init__(self, trame_app, max_msg_size=10000000, heartbeat=30):
        self._completion = None
        self.trame_app = trame_app
        self.ws_options = dict(max_msg_size=max_msg_size, heartbeat=heartbeat)
        self.web_server = aiohttp_web.Application()
        self.web_server.router.add_route("GET", "/", self._index_handler)

        routes = [aiohttp_web.get("/ws", self._ws_handler)]
        app_www = self.trame_app("__www__").server
        for route in sorted(app_www.serve.keys(), reverse=True):
            routes.append(
                aiohttp_web.static(
                    f"/{route}", app_www.serve[route], append_version=True
                )
            )
        routes.append(aiohttp_web.static("/", app_www._www, append_version=True))
        self.web_server.add_routes(routes)

    async def _index_handler(self, request):
        if request.query_string:
            return aiohttp.web.HTTPFound(f"index.html?{request.query_string}")
        return aiohttp.web.HTTPFound("index.html")

    async def _ws_handler(self, request):
        name = str(uuid.uuid4()).replace("-", "")

        # App setup
        print(f" + {name}")
        app = self.trame_app(name)
        task = app.server.start(backend="generic", exec_mode="task")
        await app.server.ready

        ws_network = aiohttp_web.WebSocketResponse(**self.ws_options)

        async def on_msg_from_server(binary, content):
            if binary:
                await ws_network.send_bytes(content)
            else:
                await ws_network.send_str(content)

        try:
            await ws_network.prepare(request)
            ws_app = app.server._server.ws
            connection = ws_app.connect()
            connection.on_message(on_msg_from_server)
            async for msg in ws_network:
                await connection.send(msg.type == aiohttp.WSMsgType.BINARY, msg)
        finally:
            connection.close()
            await app.server.stop()
            await task

        print(f" - {name}")
        return ws_network

    async def run(self, host="localhost", port=8080):
        self._completion = asyncio.get_event_loop().create_future()
        runner = aiohttp_web.AppRunner(
            self.web_server,
            handle_signals=True,
        )
        await runner.setup()

        site = aiohttp_web.TCPSite(runner, host, port)

        await site.start()
        await self._completion

    def stop(self):
        if self._completion is not None:
            self._completion.set_result(True)


def main():
    parser = argparse.ArgumentParser(description="Serve trame application")

    parser.add_argument(
        "--exec",
        default="trame.app.demo:Cone",
        help="Trame app to serve (default: trame.app.demo:Cone)",
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="IP or hostname to serve on (default: localhost)",
    )
    parser.add_argument(
        "--port",
        default=8080,
        type=int,
        help="Port to serve on (default: 8080)",
    )

    parser.add_argument(
        "--ws-heart-beat",
        default=30,
        type=int,
        help="WebSocket heart beat (default: 30)",
    )

    parser.add_argument(
        "--ws-max-size",
        default=10000000,
        type=int,
        help="WebSocket maximum message size (default: 10000000)",
    )

    args, _ = parser.parse_known_args()
    if args.exec is None or ":" not in args.exec:
        parser.print_help()
        return

    module_path, app_name = args.exec.split(":")
    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError:
        print(f"Invalid trame app to serve: {args.app}")
        parser.print_help()
        return

    print("Server configuration")
    print(f"  - host: {args.host}")
    print(f"  - port: {args.port}")
    print(f"  - app: {app_name} from {module_path}")
    print("Websocket configuration")
    print(f"  - heartbeat: {args.ws_heart_beat}")
    print(f"  - Max message size: {args.ws_max_size}")

    trame_app = getattr(module, app_name)
    web_server = MultiClientServer(
        trame_app, heartbeat=args.ws_heart_beat, max_msg_size=args.ws_max_size
    )
    asyncio.run(web_server.run(args.host, args.port))


if __name__ == "__main__":
    main()
