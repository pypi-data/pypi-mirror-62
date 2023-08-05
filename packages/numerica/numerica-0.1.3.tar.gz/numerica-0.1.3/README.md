# Numerica
My own experimental implementations of numerical methods as homework.

# Testing Package
##### Test Directly as Script
    python3.8 -m numerica
##### or Install Local Package
    pip3.8 install .
##### and Test It from REPL
    import numerica
    numerica.utils.function.fnx(2, [5, -6, 1], 1, 5) == 0

# Uploading to PyPI
##### Install Twine
    pip3.8 install twine
##### Build
    rm -rf build & rm -rf dist & rm -rf numerica.egg-info
    python3.8 setup.py sdist bdist_wheel
##### Upload
    twine upload dist/*

# Examples
## Solving Nonlinear Equations
### Graph
    import numerica as n
    print(n.graph(n.fnxp(2, [5, -6, 1], 1)))