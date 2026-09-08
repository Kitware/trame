
# Your React Investment, Now Driven by Python

If your organization has spent years building a React-based front-end team — a
component library, a design system, in-house widgets your users already know
and trust — the idea of "rewrite it in something else" is usually where a good
project idea goes to die. Trame v4 removes that trade-off.

Starting with this release, **trame can drive React components natively**, with
the same single-language promise it has always made for its Vue.js core:
describe your application — and the binding between server-side logic and
client-side UI — entirely in Python.

## What's new in v4

Trame v4 adds a second, first-class client type: `client_type="react"`. Where
you previously wrote `client_type="vue3"`, you can now target React instead —
and everything else about how you build a trame app stays the same. Same
`TrameApp` base class, same reactive `state`, same event/trigger model, same
Python-only workflow.

Here's a small example using [MUI](https://mui.com/), one of the most widely
adopted React component libraries, driven entirely from Python:

```python
from trame.app import TrameApp
from trame.ui.html import DivLayout
from trame.widgets import mui, react


class MuiDemo(TrameApp):
    def __init__(self, server=None):
        super().__init__(server, client_type="react")
        
        with DivLayout(self.server) as self.ui:
            with mui.Card(elevation=4), mui.CardContent():
                mui.Typography(["count = ", react.Bind("count", count=3)], variant="h5")
                mui.Slider(
                    value=react.Bind("count"),
                    on_change=react.Callback("count = Number($event.target.value)"),
                    min=0, max=10, step=1,
                )
                mui.Button("Reset", variant="contained", on_click=react.Callback(self.reset))

    def reset(self):
        self.state.count = 0
        
```

No JavaScript build step, no separate front-end repo, no hand-rolled REST or
WebSocket plumbing to keep server state and UI in sync. `react.Bind` and
`react.Callback` do for React what trame's `v-model`-style bindings already do
for Vue — they're the two-way bridge between your Python state and the
component library your team already knows.

## Trame is opening its core to React developers

This isn't about trame becoming a React framework. It's about enabling your hard work under the trame umbrella.

- **Your React team's work doesn't get shelved.** Component libraries, design
  systems, and branded widgets built over years of product work carry forward
  into trame applications instead of being rewritten from scratch.
- **Faster delivery, not a parallel front-end project.** Application logic —
  the part that actually encodes your product's behavior — is written once, in
  Python, by the people who best understand it. There's no second codebase to
  keep in sync, no hand-off between a Python service and a separate React app.
- **Consistent branding across tools.** Internal tools, dashboards, and
  scientific/engineering applications can share the same look and feel as your
  customer-facing React product, because they're built from the same
  components.
- **Lower integration risk.** State synchronization between client and server —
  usually a significant source of bugs and ongoing maintenance in hand-built
  full-stack apps — is handled by trame's reactive state model instead of
  custom glue code.

## What's supported today

Trame v4's React support is deliberately scoped around *bringing your own
widgets*, not building a new framework from the ground up. Today, the React
path includes:

- **Plain HTML elements** — built into trame's core, no extra dependency.
- **[MUI](https://mui.com/)** — one of the most popular React component libraries, for polished, ready-made UI out of the box.
- **[trame-rca](https://github.com/Kitware/trame-rca)** — remote rendering, including VTK, streamed into your application.
- **[trame-vtklocal](https://github.com/Kitware/trame-vtklocal)** — local, in-browser VTK rendering using VTK.wasm.
- **[trame-dataclass](https://github.com/Kitware/trame-dataclass)** — a more flexible approach to state handling and data synchronization.

## Getting started

Trame v4 is a major release precisely because of what it opens up: a credible
path for React-invested teams to adopt trame's simplified, Python-first
application model without a rewrite. If that's your situation, this is the
moment to take a look.

Learn more [in our getting started with react guide](./getting_started).
