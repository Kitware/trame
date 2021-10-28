# How do I display interactive UI?
```python
initial_number = 5

def increment():
    (number,) = get_state("myNumber")
    update_state("myNumber", number + 1)

def decrement():
    (number,) = get_state("myNumber")
    update_state("myNumber", number - 1)

@change("myNumber")
def validateMyNumber(myNumber, **kwargs):
    try:
        newNumber = int(myNumber)
        update_state("myNumber", newNumber)
    except:
        update_state("myNumber", initial_number)

controls = [
    vuetify.VBtn("Increment", click=increment),
    vuetify.VTextField(v_model=("myNumber", initial_number)),
    vuetify.VBtn("Decrement", click=decrement),
    vuetify.VSlider(v_model=("myNumber",)),
]
```

[... link to full example]
