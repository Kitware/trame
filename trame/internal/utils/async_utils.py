import asyncio
import logging

__all__ = [
    "create_task",
    "decorate_task",
    "create_state_queue_monitor_task",
    "StateQueue",
]

QUEUE_EXIT = "STOP"


def is_dunder(s):
    # Check if this is a double underscore (dunder) name
    return len(s) > 4 and s.isascii() and s[:2] == s[-2:] == "__"


def is_private(s):
    return s.isascii() and s[0] == "_"


def _handle_task_result(task: asyncio.Task) -> None:
    try:
        task.result()
    except asyncio.CancelledError:
        pass  # Task cancellation should not be logged as an error.
    except Exception:  # pylint: disable=broad-except
        logging.exception("Exception raised by task = %r", task)


def create_task(coroutine, loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()

    return decorate_task(loop.create_task(coroutine))


def decorate_task(task):
    task.add_done_callback(_handle_task_result)
    return task


async def _queue_update_state(queue, delay=1):
    from trame import state

    _monitor_queue = True
    while _monitor_queue:
        if queue.empty():
            await asyncio.sleep(delay)
        else:
            msg = queue.get_nowait()
            if isinstance(msg, str):
                if msg == QUEUE_EXIT:
                    _monitor_queue = False
            else:
                with state.monitor():
                    state.update(msg)


def create_state_queue_monitor_task(queue, delay=1):
    return create_task(_queue_update_state(queue, delay=delay))


class StateQueue:
    def __init__(self, queue, auto_flush=True):
        self._queue = queue
        self._pending_update = {}
        self._pushed_state = {}
        self._auto_flush = auto_flush
        self._ctx_count = 0

    @property
    def queue(self):
        return self._queue

    def __getitem__(self, key):
        return self._pending_update.get(key, self._pushed_state.get(key))

    def __setitem__(self, key, value):
        self._pending_update[key] = value
        if self._auto_flush:
            self.flush()

    def __getattr__(self, key):
        if is_dunder(key):
            # Forward dunder calls to object
            return getattr(object, key)

        if is_private(key):
            return self.__dict__.get(key)

        return self.__getitem__(key)

    def __setattr__(self, key, value):
        if is_private(key):
            self.__dict__[key] = value
        else:
            self.__setitem__(key, value)

    def update(self, _dict):
        self._pending_update.update(_dict)
        if self._auto_flush:
            self.flush()

    def flush(self):
        if len(self._pending_update):
            self._queue.put_nowait(self._pending_update)
            self._pushed_state.update(self._pending_update)
            self._pending_update = {}

    def exit(self):
        self._queue.put_nowait(QUEUE_EXIT)

    def __enter__(self):
        self._ctx_count += 1
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._ctx_count -= 1

        if self._ctx_count == 0:
            self.flush()
            self.exit()
