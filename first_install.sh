#!/bin/bash
set +x
virtualenv env
source ./env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
