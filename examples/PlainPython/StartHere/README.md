# Starting Examples
These should illustrate the most important concepts of trame.

# Example 1 - Reading shared state
The buttons here trigger changes in the shared state, and UI responds.

# Example 2 - Binding to the shared state
Here we bind both a Vuetify component (VTextField) and a python function (validateMyNumber) to the shared state value "myNumber". Both have control to read and write from it seamlessly. A user can change the number through the buttons or through typing, but the value will be reset to 5 if it is not a number. 
