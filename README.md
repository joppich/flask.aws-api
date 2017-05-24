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
    # requires key-id and secret key with full ec2 authorization
    # choose location and output format
    $ aws configure
```
### 3. Prepare environment variables 
```lang=shell
    # If debugging is needed set this, otherwise don't set the variable 
    $ export APP_DEBUG=True
    # If this does not get set, the token will default to 'toomanysecrets'
    $ export APP_AUTH_TOKEN=<token of your liking>
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
    $ gunicorn -t 120 -b 0.0.0.0:5000 run:app
```
## Usage Example
Spawn instance
```lang=shell
$ curl -X POST -H "Authorization: Token <your token>" -H "Content-Type: application/json" -d '{"username":"<your-username>","password":"<your-password>"}' http://<server-address>/create
```
This command returns the public IP of the instance. It will be accessible by provided credentials.

Destroy instance
```lang=shell
$ curl -H "Authorization: Token <your token>" -H "Content-Type: application/json" http://<server-address>/destroy/<instance-ip>
```
NOTE: This will also remove the associated keypair, both locally and on the aws platform.
