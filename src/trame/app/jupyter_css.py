from IPython.display import HTML, display_html

display_html(
    HTML("""
        <style>
        .jp-LinkedOutputView .jp-OutputArea-child:has(iframe[id*='trame__template']) {
        height: 100%;
        }
        </style>
        """)
)


def fullscreen(app_or_ui):
    original = app_or_ui
    if hasattr(app_or_ui, "ui"):
        app_or_ui = app_or_ui.ui

    if hasattr(app_or_ui, "iframe_style"):
        app_or_ui.iframe_style = "border: none; width: 100%; height: 100%;"

    return original
