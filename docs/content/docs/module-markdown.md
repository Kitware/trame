# Markdown 

```python
from trame.html import markdown

initial_value = "# Some markdown..."

# UI Component 
# Renders extended markdown bound to v_model
markdown.Markdown(v_model=("myDocument", initial_value)) 
```

[![Markdown-it-vue](./markdown.gif)](http://www.aqcoder.com/markdown)
Markdown plugins are supported through [markdown-it-vue](http://www.aqcoder.com/markdown) including:

- Official markdown syntax
- [AsciiMath](http://asciimath.org/)
- Images with size-control
- Simple charts with [Apache echarts](https://echarts.apache.org/examples/en/index.html)
- Diagrams like flow charts and Gantt charts with [Mermaid diagrams](https://mermaid.live)
- And more!
