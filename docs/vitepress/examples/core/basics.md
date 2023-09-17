# Introduction

The examples presented below are meant to be executed and explored so you can understand the basic mechanic of trame.

## State management

::: code-group

<<< @/../../examples/core_features/state.py
<<< @/../../examples/core_features/reserved_state.py

:::

## Events management

<<< @/../../examples/core_features/events.py

## User Interface

::: code-group

<<< @/../../examples/core_features/dynamic_layout.py
<<< @/../../examples/core_features/multi_layout.py

:::

## Life Cycle 

<<< @/../../examples/core_features/life_cycle.py

## Hot Reload

Trame as opposed to many frameworks out there is stateful which make things more complicated on how we can dynamically update it at runtime.

For that reason, the "hot reload" is at the execution and not on file save.

Basically, with trame, you need to interact with the application in order to re-excute some new code rather than saving your file and getting the new app ready to go. In fact you can have pieces of your application that will properly execute the edited code, while other will be stuck with the original version. 

Once hot-reload is enabled by either using the `TRAME_HOT_RELOAD` environment variable or by using the extra `--hot-reload` arg, only the methods executed on the controller or via `@state.change` properly re-evaluate the new code version. If you want to enable such behavior on your own function, you can use the `@trame.decorators.hot_reload` decorator.

But in the following example, you can use `watchdog` to execute the UI update on file change.

<<< @/../../examples/core_features/hot_reload.py
