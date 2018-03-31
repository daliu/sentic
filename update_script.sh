#!/bin/bash
# Don't forget to modify setup.py with new version
git add .
git commit -m "$1"
git push
python setup.py sdist
twine upload dist/sentic-0.0."$2".tar.gz
twine upload dist/sentic-0.0.6.tar.gz
