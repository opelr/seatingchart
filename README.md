# Seating Chart

<a href="https://github.com/psf/black"><img alt="Code style: black"
   src="https://img.shields.io/badge/code%20style-black-000000.svg"> </a>
![Run Checks](https://github.com/opelr/seatingchart/workflows/Run%20Checks/badge.svg)

> What do you _mean_ we're not sitting together?

_SeatingChart_ helps solve the complicated problem of grouping people together
(_and keeping them separated_ 🙃).

So many uses! Classrooms, wedding receptions, family reunions, field trips,
ferris wheel rides, ski lifts! The list goes on...

___

_Contents_:  
**[Installation and Usage](#installation-and-usage)** |
**[Contributing](#contributing)**
___

## Installation and Usage

### Installation

`pip install seatingchart`

### Usage

```python

>>> from seatingchart import SeatingChart

>>> roster = ["Amy", "Bob", "Cara", "Dan", "Emma", "Felix", "Gail", "Hank"]
>>> together = [["Amy", "Bob"], ["Gail", "Hank"]]
>>> apart = [["Amy", "Dan"]]

>>> sc = SeatingChart(roster=roster, together=together, apart=apart, max_size=3)
>>> sc.chart
[["Amy", "Bob", "Cara"], ["Gail", "Hank", "Dan"], ["Emma", "Felix"]]

>>> sc.new()
[["Amy", "Bob", "Felix"], ["Gail", "Hank", "Dan"], ["Emma", "Cara"]]

>>> print(sc.pretty())
"""
Seating Chart:
    Group 1: Amy, Bob, and Felix
    Group 2: Gail, Hank, and Dan
    Group 3: Emma and Cara
"""
```

## Contributing

### Requirements

This package uses [Poetry][poetry] for dependency management. You **must have**
this tool installed to contribute.

### Getting Started

After cloning the repository, run `poetry install` to set up your machine. This
command creates a virtual environment and install both product and development
dependencies.

After you make your change, run `make` and make sure the tests pass. In
addition to running tests, this command formats files using [`black`][black] and
lints the repository using [`flake8`][flake8].

Finally, push your changes and [submit a pull request][pr]!

### General Development Practices

Use `poetry run <command>` to invoke commands using the managed virtual
environment, or use `poetry shell` to open a shell directly in the virtual
environment. See this repository's Makefile for examples. For further
information, please reference the [Poetry documentation][poetry-docs].

[poetry]: https://github.com/python-poetry/poetry
[black]: https://github.com/psf/black
[flake8]: https://github.com/PyCQA/flake8
[pr]: https://github.com/opelr/seatingchart/compare/
[poetry-docs]: https://python-poetry.org/docs/
