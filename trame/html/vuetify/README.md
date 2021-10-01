# Vuetify module
The goal of this module is to make all vuetify components available in trame. Vuetify provides JSON describing their types, and from that we generate this module.

### Generation
We use the types provided [here](https://unpkg.com/vuetify@2.5.9/dist/json/web-types.json) to generate the module. 
```
python generator.py -i web-types.json -o __init__.py
black __init__.py # Recommended for formatting
```
