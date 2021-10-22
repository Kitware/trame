# Your Trame Application
Let's say you are building a data intensive application. You have a python codebase organizing your workflows and processing, and now you'd like to add a user interface. Trame provides your app with straightforward state management and engaging user interfaces through Shared State and Reactive UI Components.

## Shared State
Trame integrates your application's browser interface with its server backend through a Shared State of key-value pairs. These keys will hold any inputs from the user that you'd like to set as parameters for your processing. They may then hold the results of your computation so that they can be displayed to the user. And they enable modules like Trame's vtk component add interactive 3d visuals to your interface. 

When your interface or your server updates one of the keys in the Shared State, the state is efficiently synchronized on both the server and the client. In cases where changes are difficult to notice, such as changing a value deep in a nested dictionary, Trame provides methods to mark the data dirty and force a synchronization.

## Reactive UI Components
When the Shared State is updated, This results in updates to your interface as well, thanks to the reactivity of the provided UI components. Under the hood, Trame uses Vue and its reactivity to reflect updates in values of the Shared State.

This reactivity goes the other way too. Trame provides decorators for python functions so they can be called whenever a value is updated, or when triggered by a button.
