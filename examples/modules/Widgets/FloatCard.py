from trame.layouts import SinglePage
from trame.html import widgets

layout = SinglePage("FloatCard Demo")
layout.title.set_text("FloatCard Demo")
layout.content.children += [
    widgets.FloatCard(
        "Drag the handle to move me anywhere",
        classes="pa-8",
    )
]

if __name__ == "__main__":
    layout.start()
