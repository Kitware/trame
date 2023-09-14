# Simput 
Simput is an easy way to manage data with simple, flexible form generation. See documentation [here](https://github.com/Kitware/py-simput).

```python
from trame.html import simput

# Method 1 - Use simput forms ----------------------------------------
# Must be descendant of simput.Simput component
item = simput.SimputItem(
  itemId=...,    # Simput reference to display form for
)

# Method 2 - Expose columns to other UI componentts ------------------
# Must be descendant of simput.Simput component
item = simput.SimputItem(        
  "{{FirstColumn}}",       # Componenent or Vue content referencing columns
  extract=["FirstColumn"], # Which columns to make available to children
  itemId=...,              # Simput reference. See simput docs 
  no_ui=True,              # Hide simput form, show only children
)

simput.Simput(
  item,
  ui_manager=..., # Get from separate simput library 
  prefix="...",   # Identifier for manager if multiple 
)
```

## Examples

- [API](https://trame.readthedocs.io/en/latest/trame.html.simput.html)
