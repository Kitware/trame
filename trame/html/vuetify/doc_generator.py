import argparse
import json

docs_header = """
<h1 id="Vuetify"> Vuetify </h1>
Trame wraps Vuetify as it's primary UI Component Library. The api for the wrappings are documented below. More examples are available at the [vuetify website](https://vuetifyjs.com/en/introduction/why-vuetify/), and [details](/vuetify-decoder.html) are available for web developers translating more vue into trame.
"""


def transform_name(name):
    return name.replace("-", "_")


def generate_docs(input_file, output_file):
    with open(input_file) as vuetify_input:
        loaded = json.loads(vuetify_input.read())
    tags = loaded.get("contributions", {}).get("html", {}).get("tags")

    generated_docs = ""

    # Extract information and generate class definitions
    for tag in tags:
        name = tag.get("name")

        generated_docs += f"<h1 id={name}>{name}</h1>"
        attributes = tag.get("attributes", [])
        if len(attributes):
            generated_docs += "<table>"
            for attribute in attributes:
                at_name = attribute.get("name")
                attribute_name = transform_name(at_name)
                description = attribute.get("description")
                attribute_type = attribute.get("value", {}).get("type", "string")
                generated_docs += f"""
                <tr>
                  <td>
                    <pre style="background: inherit;">
vuetify.{name}(
    {attribute_name} = ...
)
                    </pre>
                  </td>
                  <td>{description}</td>
                  <td>{attribute_type}</td>
                </tr>"""
            generated_docs += "</table>"
        else:
            generated_docs += "No attributes to document"

    with open(output_file, "w") as vuetify_docs:
        vuetify_docs.write(docs_header)
        vuetify_docs.write(generated_docs)


# ----------------------------------------
# Command line interface
# ----------------------------------------


def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]",
        description="Generate vuetify module for Trame",
    )
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output")
    return parser


if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()
    output = args.output or "_generated.md"

    try:
        generate_docs(args.input, output)
    except (FileNotFoundError, IsADirectoryError) as err:
        print(f"{sys.argv[0]}: {err.strerror}", file=sys.stderr)
