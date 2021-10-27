# Snippet
```python

initial_greeting = "Hello"

@change("myGreeting")
def greet_console(myGreeting, **kwargs):
  print(myGreeting, " world!")

VTextField(
    v_model=("myGreeting", initial_greeting),
    label="How should we greet the console?",
    placeholder="Bojour"
)
```

# Full example
