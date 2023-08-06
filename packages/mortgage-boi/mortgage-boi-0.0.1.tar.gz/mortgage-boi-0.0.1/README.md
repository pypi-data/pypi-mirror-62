# Description

mortgage-boi is a python package for calculating monthly mortgage cash flows.

# Usage

```
pip install mortgage-boi

...

import mortgage-boi.mortgage as mbm
mortgage = mbm.Mortgage(principal=100_000, apr=0.06)

# monthly CF data
mortgage.payments

# specific monthly CF data
mortgage.payments_interest
```

# Appendix

### Creating a build

First, update the version number in setup.py.

Then, in the root folder:

`python setup.py sdist bdist_wheel`

In the root folder:

### Uploading a build

Prod:
`python -m twine upload dist/*`

Test:
`python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*`

### Installing the package

See https://packaging.python.org/tutorials/packaging-projects/

### Useful information for building packages:

- [what is __init__.py for](https://stackoverflow.com/questions/448271/what-is-init-py-for)

### Running test suite

`python -m unittest discover tests`
