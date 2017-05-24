from flask import request, jsonify

from . import bp
from ..auth import auth
from ..lib.api_description import get_api_description
from ..lib.aws import AwsEc2

# Set up api-appropriate errorhandling

@bp.errorhandler(404)
def not_found():
    resp = jsonify({'code':404,'message':'Resource not found'})
    return resp, 404


@bp.errorhandler(500)
def internal_error():
    resp = jsonify({'code':500,
                    'message':'An internal Error occurred.'})
    return resp, 500


@bp.errorhandler(400)
def bad_request():
    resp = jsonify({'code':400,
                    'message':'Malformed request.'})
    return resp, 400


@auth.error_handler
def unauthorized():
    resp = jsonify({'code':403,
                    'error':'Forbidden'})
    return resp, 403


"""
API Endpoints
"""

@bp.before_request
@auth.login_required
def before_request():
    """
    Guard all api endpoints
    """
    pass


# Set up routes for api-description, aws instance deployment, aws instance shutdown

@bp.route('/')
def index():
    resp = jsonify(get_api_description())
    return resp, 200


@bp.route('/create', methods=['POST'])
def create_instance():
    credentials = request.get_json(force=True)
    try:
        username = credentials['username']
        password = credentials['password']
    except:
        return bad_request()
    aws = AwsEc2()
    try:
        result = aws.deploy_aws_instance(username,password)
    except:
        return internal_error()
    resp = jsonify({'booting':result})
    return resp, 200


@bp.route('/destroy/<string:ip>')
def destroy_instance(ip):
    aws = AwsEc2()
    try:
        id_ = aws.destroy_aws_instance(ip)
    except:
        return internal_error()
    resp = jsonify({'terminating':str(id_)})
    return resp, 200
