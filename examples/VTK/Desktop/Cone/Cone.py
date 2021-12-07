# from LocalRendering import layout
from RemoteRendering import layout

# from ClientView import layout


def main():
    layout.start_desktop_window(
        on_top=True,
        confirm_close=False,
    )


if __name__ == "__main__":
    main()
