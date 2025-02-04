def test_TrameApp():
    import asyncio
    from trame.decorators import TrameApp, change, controller
    from trame.app import get_server

    @TrameApp()
    class A:
        def __init__(self, server, e):
            """doc string"""
            self.server = server
            self.e = e

        @change("c")
        def c_changed(self, c, **kwargs):
            self.c = c

    class B(A):
        def __init__(self, server, e):
            super().__init__(server, e)

        @change("d")
        def d_changed(self, d, **kwargs):
            self.d = d

        @controller.set("on_server_ready")
        def on_server_ready(self, **kwargs):
            assert self.c == 10
            assert self.d == 15
            asyncio.create_task(self.server.stop())

    server = get_server()

    a = A(server, 1)
    assert type(a) is A
    assert a.__init__.__doc__ is not None

    b = B(server, 2)
    assert type(b) is B
    assert b.e == 2

    b.server.state.c = 10
    b.server.state.d = 15
    b.server.start()
