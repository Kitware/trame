# Markdown

Markdown is a lightweight markup language that you can use to add formatting elements to plaintext text documents. Created by John Gruber in 2004, Markdown is now one of the world’s most popular markup languages.

Inside Trame it might be usefull to use markdown to simplify the writing of long description and help when some formatting is expected.

![Simple example](markdown.jpg)

## How to use it?

Trame supports an extended version of markdown for formatting documents, drawing diagrams, and more. Since Markdown could contains caracters that can conflict with the HTML syntax, a variable must be used to pass the markdown content to the UI component like in the snippet below.

```python
from trame.html import markdown

initial_value = """
# Some markdown...

Welcome to "Trame"!
"""

# UI Component
markdown.Markdown(
  v_model=("md_content", initial_value), # variable binding with initial value
)
```

Trame rely on markdown-it-vue (see documentation [here](http://www.aqcoder.com/markdown)) which support the following set of plugins:
- Official markdown syntax
- [AsciiMath](http://asciimath.org/)
- Images with size-control
- Simple charts with [Apache echarts](https://echarts.apache.org/examples/en/index.html)
- Diagrams like flow charts and Gantt charts with [Mermaid diagrams](https://mermaid.live)
- And more!

## Examples

- [PlainPython/Markdown](https://github.com/Kitware/trame/blob/master/examples/PlainPython/Markdown/Simple.py) reads Markdown files and display them