[![Build Status](https://secure.travis-ci.org/haiwen/python-seafile.svg?branch=master)](http://travis-ci.org/haiwen/python-seafile)

python-seafile
==============

python client for seafile web api

Doc: https://github.com/haiwen/python-seafile/blob/master/doc.md

# If tests fails:
check SERVICE_URL and FILE_SERVER_URL, they must be "http://127.0.0.1:80" and "http://127.0.0.1/seafhttp" type, where 127.0.0.1 is your SEAFILE_SERVER_HOSTNAME

# You can debug, using docker image:
## run image:
docker run -d --name seafile \
  -e SEAFILE_SERVER_HOSTNAME=seafile.example.com \
  -v /opt/seafile-data:/shared \
  -p 80:80 \
  seafileltd/seafile:latest

## update hosts
add "127.0.0.1 seafile.example.com" to your /etc/hosts

## add new user
from tests/fixtures.py SEAFILE_TEST_USERNAME and SEAFILE_TEST_PASSWORD

## update fixture.py
set all vars to your local setting

## install requirements (optional add venv)
pip install -r requirements.txt

## run tests:
cd ./tests
pytest


# build lib:
python setup.py bdist_wheel
