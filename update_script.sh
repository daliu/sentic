#!/bin/bash
git add .
git commit -am $0
git push
python setup.py sdist
twine upload dist/sentic-0.0.{$1}.tar.gz