pip install -q setuptools
echo "[distutils]
index-servers=pypi

[pypi]
repository = https://pypi.python.org/pypi
username = $PYPIUSER
password = $PYPIPW" > ~/.pypirc
echo Deploying coala `coala -v`...
sudo python3 setup.py register
sudo python3 setup.py sdist upload
rm ~/.pypirc
