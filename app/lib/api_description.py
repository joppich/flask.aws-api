
HEADER = "API for spawning and destroying ssh-capable aws-instances."

CREATE = "[POST] :: '/create/' ::"+\
"Post a dictionary with fields username and password. The instance will be accessible by these credentials."

DESTROY = "[GET] :: '/destroy/<instance-ip>' ::"+\
"Shutdown instance at given IP and clean up."


def get_api_description():
	return dict(api_description=HEADER,create=CREATE,destroy=DESTROY)
