# Vega 
Vega is a visualization grammar, a declarative language for creating, saving, and sharing interactive visualization designs. 

[![Vega charts through altair](./vega.png)](https://altair-viz.github.io/index.html)

## VegaEmbed
The VegaEmbed component can add a chart to your interface. It is compatible with [Altair](https://altair-viz.github.io/gallery/index.html), a powerful and concise chart library built on top of Vega.

#### `chart`
Vega chart to display. 

#### `name`
Name used for referencing the chart.

Example usage:

```python
from vuetify.html import vega
from vega_datasets import data
import altair as alt

# Make chart from example dataset
cars = data.cars() 

alt.Chart(cars).mark_point().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
)
myChart = alt.Chart(chart_data)

# Make component
vega.VegaEmbed(chart=myChart)
```
