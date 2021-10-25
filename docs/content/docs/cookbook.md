# Cook Book

Here are snippets of common tasks in Trame. See 'StartHere' examples which run these.

### How do I connect my code to a button?
```python

def runMyProcess():
  print("Running very cool code!")

layout.children += [VBtn("Please run my process", click=runMyProcess)]

```
### How do I read user input?
```python

initialGreeting = "Hello"

@change("myGreeting")
def greetConsole(myGreeting, **kwargs):
  print(myGreeting, " world!")

layout.children += [VTextField(
                      v_model=("myGreeting", initialGreeting),
                      label="How should we greet the console?",
                      placeholder="Bojour")
                   ]
```
### How do I read CLI arguments?
Trame uses python's `argparse` for CLI arguments. Examples are here: https://docs.python.org/3/library/argparse.html
```python
from trame import get_cli_parser

parser = get_cli_parser()
parser.add_argument("-o", "--output", help="Our working directory")
args = parser.parse_args()
```

### How do I debug the shared state?
...

### How do I display a chart?

### How do I upload a file to the server?

### How do I read a file to the frontend?


### How do I bind to the shared state without?
### How do I bind to the shared state with an initial value?
### How do I bind to a readonly string?
