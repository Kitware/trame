# How do I render static content?
<!--
```python
from trame import start 
from trame.layouts import SinglePage
from trame.html import Div

greeting = "Hello world"

layout = SinglePage("Hello")
layout.title.content = "Hello"
layout.content.children += [ Div( greeting, classes="ma-8") ]

if __name__ == "__main__":
    start(layout)
```
-->
