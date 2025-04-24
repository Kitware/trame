from trame.app import get_server
from trame.ui.html import DivLayout
from trame.widgets import html

# -----------------------------------------------------------------------------
# Trame app
# -----------------------------------------------------------------------------

server = get_server()

# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

line_count = 1


def update_first_line():
    global line_count
    with server.ui.first_line:
        server.ui.first_line.clear()
        html.Div(f"First line: {line_count}")
    line_count += 1


# Start with some UI to control a
with DivLayout(server) as layout:
    server.ui.first_line(layout)  # Insert place holder

    def add_line():
        global line_count
        with layout:
            html.Div(f"Line: {line_count}")
        line_count += 1

    html.Button("Add line", click=add_line)
    html.Button("Update first line", click=update_first_line)

# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
