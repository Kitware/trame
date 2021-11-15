# trame

![trame](/trame/images/trame-concept.jpg)

The trame package provides a set of core functionality for designing your Python application with a Web UI.
trame is at heart a `shared state` that lets you bind UI elements to Python methods by allowing your code to react when the underlying data is changing.
On top of that `shared state` concept, you can simply bind `Python methods` to UI events such as a click. The binding of functions is done by defining triggers which tends to be done for you when using the `trame.html.*` modules.

## How to use it

trame really aims to be simple and to enable anyone to create a GUI to a Python based application.
The fact that the UI is web based should not matter for the user, I guess this could be seen as a add-on bonus in case you want to use your application remotely across the internet. But trame can definitely be levarged for local use cases too.

The anatomy of a trame application could be seen as follows:

1. Business logic on what you application is doing
2. Connect any method that should react to state change (i.e. slider changing a sampling parameter)
3. Define functions that should be called when someone click or do something in the UI
4. Pick a layout and fill it with some widgets
   1. When defining widgets, you could bind states to their model with their initial value
   2. When clicking on something, provide the function that should be called
5. Start your server/application
