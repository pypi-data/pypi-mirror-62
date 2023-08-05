#!/usr/bin/env bash 
cd /var/task/src
mkdir /tmp/.dep2layer && cat requirements.txt | grep -v ^\\s*boto3 >/tmp/.dep2layer/requirements.txt
pip install -r requirements.txt --target /tmp/python --no-cache-dir
code=$?
if [ $code != 0 ]; then
  echo Install faild. Exit code $code
  exit $code
fi
if [ -d /tmp/python ]; then
  cd /tmp/python
#  find . -name "*.pyc" -delete
  find . -name "*.egg-info" | xargs rm -rf
  # zip -9mrv packages.zip .
  # mv packages.zip ..
  # cd ..
  # rm -rf packages
fi
