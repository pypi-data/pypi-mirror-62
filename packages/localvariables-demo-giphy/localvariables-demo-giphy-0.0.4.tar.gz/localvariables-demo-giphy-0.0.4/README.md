# Local Variables Giphy Demo

This is just a demo for a [Local Variables](https://localvariables.com) talk about publishing python packages.

Given a search string as the first argument, it'll search Giphy for a gif, and if you pass the `-o` flag, it'll automatically open your default browser up to the url.

## Usage

```usage
usage: demo.py [-h] [-v] [-o] [search_string]

Search through Giphy for whatever you want!

positional arguments:
  search_string  The search string

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  Display the current version
  -o, --open     Open the returned url in the webbrowser
```