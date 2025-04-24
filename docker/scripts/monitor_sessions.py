# pip install psutil watchdog

import argparse
import asyncio
import os
import pwd
from functools import partial
from pathlib import Path

import psutil
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


def cli():
    parser = argparse.ArgumentParser(
        prog="Trame session monitoring",
        description="This application will monitor Python processes listening to network",
    )
    parser.add_argument(
        "--port-range",
        nargs=2,
        help="Inclusive port range to check",
        type=int,
        default=[9001, 9500],
    )
    parser.add_argument(
        "--user", help="User name", default=pwd.getpwuid(os.getuid())[0]
    )
    parser.add_argument("--watch", help="File to watch for new sessions")
    parser.add_argument(
        "--target",
        help="Directory to fill with empty file matching active port",
        required=True,
    )
    parser.add_argument(
        "--refresh",
        help="Time in second for refresh",
        type=int,
        default=60,  # 60 seconds
    )
    options, _ = parser.parse_known_args()
    return options


def update_running(user, port_range, target_directory):
    # Gather current sessions
    target_directory = Path(target_directory)
    current_ports = set()
    for f in target_directory.iterdir():
        if f.is_file():
            try:
                port = int(f.name)
                current_ports.add(port)
            except ValueError:
                pass

    # Check active processes + port
    file_to_delete = set(current_ports)
    for pid in psutil.pids():
        try:
            p = psutil.Process(pid)
        except psutil.NoSuchProcess:
            continue

        if p.username() == user and "python" in p.name():
            conns = p.net_connections(kind="tcp")
            for con in conns:
                port = con.laddr.port
                if port_range[0] <= port <= port_range[1]:
                    file_to_delete.discard(port)
                    (target_directory / f"{port}").touch()

    # Cleaning up dead sessions
    for port in file_to_delete:
        (target_directory / f"{port}").unlink()


async def run_forever(fn, delta_t):
    while True:
        fn()
        await asyncio.sleep(delta_t)


class ExecOnChange(FileSystemEventHandler):
    def __init__(self, fn, file_path):
        super().__init__()
        self._fn = fn
        self._file_path = file_path

    def on_modified(self, event):
        if event.src_path == self._file_path:
            self._fn()


def main():
    args = cli()
    update = partial(
        update_running,
        user=args.user,
        port_range=args.port_range,
        target_directory=args.target,
    )

    print("- target directory:", args.target)
    print("- user:", args.user)
    print("- port range:", args.port_range)
    print("- refresh:", args.refresh)

    if args.watch and Path(args.watch).exists():
        watch_file = Path(args.watch).resolve()
        print("- watch:", watch_file)

        observer = Observer()
        observer.schedule(
            ExecOnChange(update, str(watch_file)),
            str(watch_file.parent),
            recursive=False,
        )
        observer.start()

    asyncio.run(run_forever(update, args.refresh))


if __name__ == "__main__":
    main()
