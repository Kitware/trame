# How do I display interactive UI?
slider, buttons, and input
```python
from trame.html import vuetify

def run_my_process():
  print("Running very cool code!")

vuetify.VBtn("Please run my process", click=run_my_process)
```

# How do I display and read forms?
```python
from trame.html import vuetify 

initial_greeting = "Hello"

@change("myGreeting")
def greet_console(myGreeting, **kwargs):
  print(myGreeting, " world!")

vuetify.VTextField(
    v_model=("myGreeting", initial_greeting),
    label="How should we greet the console?",
    placeholder="Bonjour"
)
```

