# Vega 
Trame supports powerful visualization grammars like Vega through easy-to-use libraries like Altair (see docs [here](https://altair-viz.github.io/gallery/index.html)) for concise visualization.

```python
from vuetify.html import vega
from vega_datasets import data
import altair as alt

# Make chart from example dataset
myChart = alt.Chart(data.cars()).mark_point().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
)

# Make component
vega.VegaEmbed(
  chart=myChart, # Chart to display
  name=...,      # Reference for Vega. Generated if left out
)
```

[![Vega charts through altair](./vega.png)](https://altair-viz.github.io/index.html)

