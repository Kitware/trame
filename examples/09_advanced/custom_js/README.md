This example load a JS file on disk to make it available for the trame template. 

For that we extend the existing `window.trame.utils` container with our helper functions to be used in our template expression as `utils.my_code.*`.

On top of that we illustrate some usage of JSEval component for executing custom JS.