When serving a trame application using apache/nginx or any other static file server you can use the following built-in utility to extract the client side needed for your trame application.

```
python \
    -m trame.tools.www \
    --output /path/to/output/directory \
    vuetify vtk router ... # List all the trame-XXX you use within your trame application.
```