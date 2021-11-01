# How do I upload a file

Sometime user has to push file to the server so the server can process it. In Trame we rely on the state to achieve that exchange.
In the example below we use [vuetify.VFileInput](https://vuetifyjs.com/en/components/file-inputs/) to set a JavaScript `File` into a state variable.

## Code

```python
from trame import start, change
from trame.layouts import FullScreenPage
from trame.html import vuetify

layout = FullScreenPage("File upload")
layout.children += [
    vuetify.VFileInput(
        v_model=("file_exchange", None),
    )
]

@change("file_exchange")
def file_uploaded(file_exchange, **kwargs):
    file_name = file_exchange.get("name")
    file_size = file_exchange.get("size")
    file_time = file_exchange.get("lastModified")
    file_mime_type = file_exchange.get("type")
    file_binary_content = file_exchange.get("content")
    print(f"Go file {file_name} of size {file_size}")

if __name__ == "__main__":
    start(layout)
```
## Example

- [Code above](https://github.com/Kitware/trame/blob/master/examples/howdoi/upload.py)