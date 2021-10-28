# Markdown
Trame supports an extended version of markdown for formatting documents, drawing diagrams, and more.

```python
from trame.html import markdown

initial_value = "# Some markdown..."

# UI Component
markdown.Markdown(
  v_model=("myDocument", initial_value), # Shared state binding to markdown
)
```

![Simple example](markdown.jpg)

Markdown plugins are supported through markdown-it-vue (see documentation [here](http://www.aqcoder.com/markdown)) including:

- Official markdown syntax
- [AsciiMath](http://asciimath.org/)
- Images with size-control
- Simple charts with [Apache echarts](https://echarts.apache.org/examples/en/index.html)
- Diagrams like flow charts and Gantt charts with [Mermaid diagrams](https://mermaid.live)
- And more!
