# Simput 
Simput is an easy way to manage data with simple, flexible form generation. See documentation [here](https://github.com/Kitware/py-simput).

```
from trame.html import simput

# Form element for item in data store
item = SimputItem(
  itemId=... # Simput reference. See simput docs
)

my_user_interface = #... build up layout including our item

simput.Simput(my_user_interface) # Wrapper makes simput available to children
```
