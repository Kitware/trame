utils
===================================================

The **utils** namespace is aiming to gather user friendly methods. Trame by default provide a couple of useful ones listed below.

.. function:: utils.download(filename, contentOrPromise, type = 'application/octet-stream')

    Trigger a file download within the browser.

    :param filename: Name that the file should have on your disk once downloaded
    :param contentOrPromise: File content or a promise which will return such content
    :param type: Mime type of the file which may affect how your browser will deal with it.


    .. code-block:: python

        import time
        from trame.app import get_server
        from trame.ui.vuetify import SinglePageLayout
        from trame.widgets import vuetify

        # -----------------------------------------------------------------------------
        # Trame setup
        # -----------------------------------------------------------------------------

        server = get_server()
        state, ctrl = server.state, server.controller


        @ctrl.trigger("generate_content")
        def generate_content():
            return f"Hello on the server is {time.time()}"


        # -----------------------------------------------------------------------------
        # UI setup
        # -----------------------------------------------------------------------------

        layout = SinglePageLayout(server)

        with layout:
            with layout.toolbar as toolbar:
                toolbar.clear()
                vuetify.VSpacer()
                vuetify.VBtn(
                    "Download",
                    click="utils.download('hello.txt', trigger('generate_content'), 'text/plain')",
                )


        # -----------------------------------------------------------------------------
        # start server
        # -----------------------------------------------------------------------------

        if __name__ == "__main__":
            server.start()

.. function:: utils.get(path, obj = window)

    This allow to lookup window nested JS path.

    .. code-block:: python

        # ...
        with layout:
            vuetify.VBtn("Print", click="utils.get('console.log')('hello')")

.. function:: utils.safe(obj)

    Sometime JavaScript object don't preoperly serialize due to circular references or else.
    That **safe** method will strip down anything that does not serialize in a transparent manner.
    This method is mainly meant for debugging or exploration as ideally you should only try to exchange between the server and the client only what is really required.

.. function:: utils.tree(obj)

    Helper function to convert a JavaScript object into a vuetify.VTreeView data structure.

    .. code-block:: python

        state.variable_name = { ... }
        
        # ...
        with layout:
            vuetify.VTreeview(items=("utils.tree(variable_name)",))

.. function:: utils.vtk.event(event)

    This decorator is to handle meaningful data extraction from an event of trame.widgets.vtk.Vtk{...}View into something that can be processed on the server side.

.. function:: utils.fmt.number(value, units=[], steps=1000, fixed=2)

    This formatter helper let you reduce a number based on some more appropriate unit for human readability.

    .. code-block:: javascript

        console.log(utils.fmt.number(5.234, ['B1', 'B2', 'B3'], 123, 2))
        // 5.23 B1
        console.log(utils.fmt.number(5.234 * 123, ['B1', 'B2', 'B3'], 123, 2))
        // 5.23 B2
        console.log(utils.fmt.number(5.234 * 123 * 123, ['B1', 'B2', 'B3'], 123, 4))
        // 5.2340 B3

.. function:: utils.fmt.bytes(value, fixed=2)

    Convert the provided value into a string with Bytes units while keeping 2 fixed number behind the comma by default.

    .. code-block:: javascript

        console.log(utils.fmt.bytes(5.234 * 1024))
        // 5.23 KB