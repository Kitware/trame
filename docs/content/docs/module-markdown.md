# Markdown Trame module
Trame has extensive support for markdown documents. 

[... image]

Markdown plugins are supported through [markdown-it-vue](http://www.aqcoder.com/markdown) including:

- Official markdown syntax
- [AsciiMath](http://asciimath.org/)
- Images with size-control
- Simple charts with [Apache echarts](https://echarts.apache.org/examples/en/index.html)
- Diagrams like flow charts and Gantt charts with [Mermaid diagrams](https://mermaid.live)
- And more!

Trame's `markdown` module exposes a `Markdown()` component which will render any markdown bound to it with `v_model`.
```python
from trame.html import markdown

markdown.Markdown(v_model="# Some markdown...")
```

Run the markdown example [here](https://github.com/Kitware/trame/blob/master/examples/PlainPython/Markdown/Simple.py) to see more Trame markdown features in action.
