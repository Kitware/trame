# Vuetify
Trame wraps Vuetify as it's primary UI Component Library. We encourage Trame developers to consult [Vuetify's website](https://vuetifyjs.com/en/introduction/why-vuetify/) for API documentation, usage, and examples.

When writing Trame based on the Vuetify documentation keep the following in mind.

## Evaluating properties 
Trame evaluates properties if they are wrapped in a tuple.
```python
from trame.html import vuetify 

# This sets the label to "myLabel"
vuetify.VTextField(label="myLabel") 

# This evaluates "myLabel" in Trame's Shared State for a value to set
vuetify.VTextField(label=("myLabel",)) 

# This evaluates "myLabel", which was initially set to "Initial Label"
vuetify.VTextField(label=("myLabel", "Initial Label")) 
```

## Syntax changes
Wrapping Vuetify with Python was accomplished by making these syntax changes.
```python
from trame.html import vuetify

#----------------------------------------------------------------------
# Explicit boolean properties
#----------------------------------------------------------------------

## Vuetify implicitly sets properties to True
# <v-text-field disabled></v-text-field> 

## Trame requires explicitly setting True
vuetify.VTextField(disabled=True) 

#----------------------------------------------------------------------
# Property name changes
#----------------------------------------------------------------------

## Vuetify writes properties with -
# <v-text-field v-model="myText"> </v-text-field>

## Trame writes properties with _
vuetify.VTextField(v_model=("myText",)) 

## Vuetify writes events with @
# <v-btn @click="runMethod"> </v-button>

## Trame doesn't
vuetify.VBtn(click=runMethod)

```
