# How do I download a file

Sometimes a user has to download a file from the server so the client can save it to its drive. In trame we rely on the shared state to achieve that file exchange.

## Code

```python
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
    layout.start()
```
## Example

- [Code above](https://github.com/Kitware/trame/blob/master/examples/howdoi/download.py)
