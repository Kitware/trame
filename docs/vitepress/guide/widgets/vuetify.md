# Vuetify

Vuetify is a UI Library with beautifully handcrafted Material Components. No design skills required — everything you need to create amazing applications is at your fingertips.

[![Vuetify WebSite](/assets/images/widgets/module-vuetify.jpg)](https://vuetifyjs.com/en/)

## How to use it?

trame wraps Vuetify as it's primary UI Component Library. The [Vuetify website](https://vuetifyjs.com/en/) is very well made for exploring components and understanding components' parameters and controls, while a reference to our wrapper API is available [here](https://trame.readthedocs.io/en/latest/trame.html.vuetify.html).

The way trame translate Vue templates into plain Python code is by doing the following.

### Material Components

First you need to import the `vuetify` module so you can instantiate the various Material Components like illustrated below. Moreover, in the documentation the component names use dashes as separators while in Python we use the Camelcase notation for the class name.

```python
from trame.html import vuetify

# <v-btn>Hello World</v-btn>
btn = vuetify.VBtn("Hello World")
```

### Boolean attributes

Implicit attribute values must be made explicit in Python by assigning `True` to them.

```python
# <v-text-field disabled />
vuetify.VTextField(disabled=True)
```

### Dash and colon separators

Any special characters (`-` and `:`) become `_` in Python.

```python
# <v-text-field v-model="myText" />
vuetify.VTextField(v_model=("myText",))
```

### Events

Events in vue are prefixed with a `@` but in Python we declare them the same way we declare regular attributes.

```python
def runMethod():
    pass

# <v-btn @click="runMethod" />
vuetify.VBtn(click=runMethod)
```

## Examples

Vuetify is the core of any widgets structure we use inside our examples.
- [API](https://trame.readthedocs.io/en/latest/trame.html.vuetify.html)
- [VTK/ContourGeometry](https://github.com/Kitware/trame/blob/master/examples/v1/VTK/ContourGeometry/DynamicLocalRemoteRendering.py#L96-L132) has a Toggle buttons group, switch, slider and a button.
- [PlainPython/Markdown](https://github.com/Kitware/trame/blob/master/examples/v1/PlainPython/Markdown/Simple.py#L27-L32) has a drop down to select which file to load.
- [GeoMaps/UberPickupsNYC](https://github.com/Kitware/trame/blob/master/examples/v1/PlainPython/GeoMaps/UberPickupsNYC/app.py#L38-L44) use Row and Cols to manage content in a grid layout.

<!--
## Evaluating properties
trame evaluates properties if they are wrapped in a tuple.
```python
from trame.html import vuetify

# This sets the label to "myLabel"
vuetify.VTextField(label="myLabel")

# This evaluates "myLabel" in trame's Shared State for a value to set
vuetify.VTextField(label=("myLabel",))

# This evaluates "myLabel", which was initially set to "Initial Label"
vuetify.VTextField(label=("myLabel", "Initial Label"))
```
-->
