# How do I render static content?

This example illustrates how you can simply add static HTML content to your page.

## Code

```python
from trame.layouts import FullScreenPage

html = """
<h3>Welcome to trame...</h3>

<div>
    <i>Hello</i> <b>World</b>
</div>
"""

layout = FullScreenPage("Hello")
layout.children += [html]

if __name__ == "__main__":
    layout.start()
```

## Example

- [Code above](https://github.com/Kitware/trame/blob/master/examples/v1/howdoi/static.py)
