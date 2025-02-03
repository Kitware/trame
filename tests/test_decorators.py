def test_TrameApp():
    import asyncio
    from trame.decorators import TrameApp, change, controller
    from trame.app import get_server

    @TrameApp()
    class A:
        def __init__(self, server):
            self.server = server
            self.server.state.change("c")(self.c_changed)

    class B(A):
        def __init__(self, server):
            super().__init__(server)

        @change("c")
        def c_changed(self, c, **kwargs):
            self.c = c

        @controller.set("on_server_ready")
        def on_server_ready(self, **kwargs):
            assert self.c == 10
            asyncio.create_task(self.server.stop())

    b = B(get_server())
    b.server.state.c = 10
    b.server.start()
