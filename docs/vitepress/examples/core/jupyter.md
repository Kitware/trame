# Exposing a trame application into Jupyter

## Define application

<<< @/../../examples/core_features/jupyter.py

## Use application within Jupyter

```python
cone = Cone()
cone
```

![Trame in Jupyer](/assets/images/deployment/jupyter.png)

## Edit state in another cell

```python
cone.resolution = 4
```
