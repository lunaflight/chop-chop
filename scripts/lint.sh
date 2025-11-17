#!/bin/bash

PYTHONPATH=$(pwd) python -m src.linter.main "$@"
