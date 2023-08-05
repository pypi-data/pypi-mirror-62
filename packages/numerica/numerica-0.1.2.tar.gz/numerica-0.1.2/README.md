# Numerica
My own experimental implementations of numerical methods as homework.

# Uploading to PyPI
##### Install Twine
  pip3.8 install twine
##### Build
  rm -rf build & rm -rf dist & rm -rf numerica.egg-info
  python3.8 setup.py sdist bdist_wheel
##### Upload
  twine upload dist/*