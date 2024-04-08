# How does it work?

You might be wondering what more is needed as things are pretty simple so far. Well you may relize that while everything is working fine locally, when deployed in the cloud, it does not work anymore and you don't know why. This guide aims to cover how things works under the cover and what you can tune to make it work in your environment. 
Let's review the basic flow.

```python
from module import App  # Get the application class 

app = App()             # a) Instantiate application (with default server)
await app.ui.ready      # b) Wait for the UI to be ready
app.ui                  # c) Display UI in cell output
```

## Application instantiation

In the __(a)__ step, we instantiate the application but more importantly we lookup a trame server based on the constructor argument. 
When not provided, we get the default server. So instantiating the application twice will not lead to any isolation between them as they will reflect the exact same server state. 

## Waiting for the User Interface

In the __(b)__ step, we asynchronously wait for something before executing the following lines... 
But technically, we are waiting for the associated server to run as a task and be ready to accept connections.
This means that instead of running the server as the main process, we start it as a background task in the current asynchronous runtime. 

## Display the User Interface

In the __(c)__ step, we simply return the layout object which Jupyter will use its `_jupyter_content_` method to display it in the cell. But technically we are building an `<iframe />` pointing to our webserver (host:port) that is running as a task inside the Jupyter Kernel.

As you can imagine, when deployed in the cloud, such default behavior won't work due to missing network route. But several solutions are available and covered in the next guide.



