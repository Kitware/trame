# How do I display interactive UI?

This example illustrates how the shared state works by having a method modifing it along with several components showing its value and letting the user edit it.

## Code

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

## Example

- [Code above](https://github.com/Kitware/trame/blob/master/examples/howdoi/interactive.py)
