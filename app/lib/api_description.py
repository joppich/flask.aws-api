
HEADER = "API for spawning and destroying ssh-capable aws-instances."

CREATE = "[GET] :: '/create?pk=<public-key>' ::"+\
        "The instance will be accessible by key provided here."

DESTROY = "[GET] :: '/destroy?ip=<instance-ip>' ::"+\
        "Shutdown instance at given IP."


def get_api_description():
	return dict(api_description=HEADER,create=CREATE,destroy=DESTROY)
