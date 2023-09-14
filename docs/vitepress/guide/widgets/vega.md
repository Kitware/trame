# Vega

Vega is a visualization grammar, a declarative language for creating, saving, and sharing interactive visualization designs. With Vega, you can describe the visual appearance and interactive behavior of a visualization in a JSON format, and generate web-based views using Canvas or SVG.

Vega works well with Altair. Altair’s API is simple, friendly and consistent. This elegant simplicity produces beautiful and effective visualizations with a minimal amount of code.

[![Vega charts through altair](/assets/images/widgets/module-vega.jpg)](https://altair-viz.github.io/index.html)

## How to use it?

The best and easiest way to create charts for [Vega](https://vega.github.io/vega/) is to use [Altair](https://altair-viz.github.io/index.html). And with trame, the `Altair` chart can be passed directly to the component. The code snippet below illustrate such usage.

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
```

Then you can either pass the `chart` directly at build time and then update it via another instance later.

```python
chart_component = vega.VegaEmbed(myChart)
chart_component.update(myChart2) # Make change
```

Or assign a name to use inside your shared state and update it by either updating the state directly or calling `chart_ui.update(chart_inst)` on the component itself.

```python
chart_component2 = vega.VegaEmbed(
    name="myChart", # Shared state name for vega chart
)
chart_component2.update(myChart)  # Set chart
chart_component2.update(myChart2) # Make change
```

By default, if no `name` is provided, one will be automatically generated. This can be seen in the [GeoMaps/UberPickupsNYC](https://github.com/Kitware/trame/blob/master/examples/v1/PlainPython/GeoMaps/UberPickupsNYC/app.py#L18) example.

## Examples

Vega is used in the following set of examples:
- [API] (https://trame.readthedocs.io/en/latest/trame.html.vega.html)
- [GeoMaps/UberPickupsNYC](https://github.com/Kitware/trame/blob/master/examples/v1/PlainPython/GeoMaps/UberPickupsNYC/app.py#L18)
- more to come...
