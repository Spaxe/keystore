#!/bin/sh
./setup.py check
./setup.py clean
rm -rf dist
./setup.py sdist bdist_wheel
twine upload dist/*