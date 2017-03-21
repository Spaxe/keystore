#!/bin/sh
./setup.py clean
rm -rf dist
./setup.py sdist bdist_wheel
twine upload dist/*