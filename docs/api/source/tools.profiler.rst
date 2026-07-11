Application profiler
==============================

trame ships with a lightweight profiling helper for timing sections of your
application, and an interactive web viewer for exploring the resulting
traces.

Recording traces
-----------------

Traces are produced with ``trame_common.utils.profiler``. Instrumentation is
disabled by default, so timers left in your code cost nothing until you turn
them on:

.. code-block:: python

    from trame_common.utils import profiler

    # Turn instrumentation on (do this once, early in your app)
    profiler.enable()

    # Time a block of code
    with profiler.timer("my_module::compute"):
        do_expensive_work()

    # Time a block of code and also report an implied fps rate
    with profiler.timer("my_module::render", show_fps=True):
        render_frame()

The same instrumentation can be driven from arbitrary start/end callbacks
using the ``Timer`` class, which is how trame itself measures network
activity internally:

.. code-block:: python

    from trame_common.utils.profiler import Timer

    network_timer = Timer("trame.network")
    some_event_emitter.add_listener(network_timer.on_start, network_timer.on_end)

When instrumentation is scattered across a large codebase, ``include()`` and
``exclude()`` let you narrow down what actually gets recorded at runtime:

.. code-block:: python

    profiler.include("my_module::")        # only keep entries starting with that prefix
    profiler.exclude("my_module::debug")   # but drop that one

Each recorded entry is written as a single fixed-width line (name, start
timestamp, duration in ms), by default to ``stderr``. To capture a trace,
just redirect ``stderr`` to a file while running your application:

.. code-block:: bash

    python my_app.py 2> trace.log

Viewing traces
-----------------

Once you have one or more trace log files, explore them in an interactive
web UI with:

.. code-block:: bash

    python -m trame.tools.profiler --data trace.log
    # or compare several runs side by side
    python -m trame.tools.profiler --data trace-1.log trace-2.log

This starts a trame application that renders each trace as a track-based
timeline: every distinct name becomes its own row, and each recorded call is
drawn as a rectangle positioned and sized from its start time and duration
(hover over a rectangle to see its exact duration). Track rows can be
reordered with the up/down arrows next to their label, and the slider below
the timeline lets you scroll through time once the trace is wider than the
window.
