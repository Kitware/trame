from trame import start
from trame.layouts import FullScreenPage

html = """
<h3>Welcome to trame...</h3>

<div>
    <i>Hello</i> <b>World</b>
</div>
"""

layout = FullScreenPage("Hello")
layout.children += [html]

if __name__ == "__main__":
    start(layout)
