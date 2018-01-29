#!/bin/bash
git add .
git commit -m "$1"
git push
python setup.py sdist
twine upload dist/sentic-0.0."$2".tar.gz