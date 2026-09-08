
# Why trame is built on Vue

Trame's core client is powered by [Vue.js](https://vuejs.org/) — the default
`client_type` behind every `TrameApp`, with nothing extra to install or opt
into. At Kitware, we chose Vue because its design gets out of the way: a
gentle learning curve, a clear reactivity model, and an approachable template
syntax that reads naturally even if you've never written a line of
JavaScript.

Rather than hide that syntax behind a Python abstraction, trame exposes Vue's
capabilities as natively as possible — `v-model`, `v-if`, `v-for`, scoped
slots, refs, and event modifiers are all just a Python kwarg away. The goal is
to never limit what you can build on the web just because you're driving it
from Python.

The result: full access to the Vue ecosystem's expressiveness, a mature and
battle-tested production client, and a single language — Python — to
describe your entire application.

Ready to write some code? [Follow the getting started guide](./getting_started)
to build your first trame + Vue3 app, from a minimal "Hello, world" to a
full interactive example.
