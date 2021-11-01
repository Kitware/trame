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