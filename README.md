## Requirements

* python3
* python-virtualenv
* python-pip

## Setup

### 1. Set up virtualenv
```lang=shell
    $ virtualenv -p /path/to/python3 venv
    $ . venv/bin/activate
    $ pip install -r requirements.txt
```
### 2. Set up aws-client config
```lang=shell
    # requires key-id and secret key
    # choose location and output format
    $ aws configure
```
### 3. Prepare environment variables 
```lang=shell
    # If debugging is needed set this, otherwise don't set the variable 
    $ export APP_DEBUG=True
    $ export AWS_AMI=ami-060cde69 # or choose a different linux ami of your liking
```

## Start api
For builtin werkzeug dev server, run
```lang=shell
    $ python run.py 
    # If the debug flag is not set it will listen on 0.0.0.0:5000
    # otherwise on localhost:5000
```
Or with gunicorn, configured to your liking, do
```lang=shell
    $ gunicorn -b 0.0.0.0:5000 run:app
```

