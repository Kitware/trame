# How do I download a file

Sometime user has to download file from the server so the client can save it to its drive. In Trame we rely on the state to achieve file exchange.

## Code

```python
from trame import start
from trame.layouts import FullScreenPage
from trame.html import vuetify

layout = FullScreenPage("File upload")
layout.children += [
    vuetify.VBtn(
        "Download",
        click="download('my_file_name.csv', file_content, 'text/csv')",
    )
]

layout.state = {
    "file_content": """
a,b,c
1,2,3
4,5,6
7,8,9
    """,
}

if __name__ == "__main__":
    start(layout)
```
## Example

- [Code above](https://github.com/Kitware/trame/blob/master/examples/howdoi/download.py)