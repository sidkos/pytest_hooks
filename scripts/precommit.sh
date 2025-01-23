#!/bin/bash

isort .
black .
flake8 .
pycodestyle .
mypy .
yamllint . --no-warnings