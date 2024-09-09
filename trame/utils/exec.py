import asyncio


class Throttle:
    """
    Helper class that wrap a function with a given max execution rate.
    By default the rate is set to execute no more than once a second.

    :param fn: the function to call.
    :type fn: function

    :param ts: Number of seconds to wait before the next execution.
    :type ts: float
    """

    def __init__(self, fn, ts=1):
        self._ts = ts
        self._fn = fn
        self._requests = 0
        self._pending = False
        self._last_args = []
        self._last_kwargs = {}

    @property
    def rate(self):
        """Number of maximum executions per second"""
        return 1.0 / self._ts

    @rate.setter
    def rate(self, rate):
        """Update the maximum number of executions per seconds"""
        self._ts = 1.0 / rate

    @property
    def delta_t(self):
        """Number of seconds to wait between execution"""
        return self._ts

    @delta_t.setter
    def delta_t(self, seconds):
        """Update the number of seconds to wait between execution"""
        self._ts = seconds

    async def _trottle(self):
        self._pending = True
        if self._requests:
            self._fn(*self._last_args, **self._last_kwargs)
            self._requests = 0

        await asyncio.sleep(self._ts)
        if self._requests > 0:
            await self._trottle()
        self._pending = False

    def __call__(self, *args, **kwargs):
        """Function call wrapper that will throttle the actual function provided at construction"""
        self._requests += 1
        self._last_args = args
        self._last_kwargs = kwargs

        if not self._pending:
            asyncio.create_task(self._trottle())
