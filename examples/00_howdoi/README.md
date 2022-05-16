# Getting started examples

This directory gather several examples introducing some concepts around trame.

## CLI

The cli example show how you can make use of Command Line Arguments to provide file to load and more.

## Download

The download example show how a button click can trigger a file download on the client side.

## Dynamic

The dynamic example leverage asyncio that dynamically update the state that get reflected on the client side at the discretion of the server change.

## Interactive

The interactive example show how method call can be linked to button click along with state modification directly from a widget.

## Static

The static example show how you can simply inject HTML content as string.

## Table

The table example show how you can display a table from a Pandas dataframe while enabling dynamic content filtering.

## Upload

The upload example show how the UI can select a file localy and make it available on the server side for processing.

## WWW client code to serve

When serving a trame application using apache/nginx or any other static file server you can use the following built-in utility to extract the client side needed for your trame application.

```
python \
    -m trame.tools.www \
    --output /path/to/output/directory \
    vuetify vtk router ... # List all the trame-XXX you use within your trame application.
```