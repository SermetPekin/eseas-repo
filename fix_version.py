import re

fname = "eseas/__init__.py"
content = open(fname).read()
if "__version__" not in content:
    content = content + "\n__version__ = '2.0.0'\n"
    open(fname, 'w').write(content)
