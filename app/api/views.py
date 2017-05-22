from flask import request, jsonify

from . import bp
from app.lib.api_description import get_api_description
from app.lib.aws import AwsEc2

# Set up api-appropriate errorhandling

@bp.errorhandler(404)
def not_found(error):
    resp = jsonify({'code':404,'message':'Resource not found'})
    return resp, 404

@bp.errorhandler(500)
def internal_error(error):
    resp = jsonify({'code':500,
                    'message':'An internal Error occurred.\
                     Please contact an administrator.'})
    return resp, 500


# Set up routes for api-description, aws instance deployment, aws instance shutdown

@bp.route('/')
def index():
    resp = jsonify(get_api_description())
    return resp, 200


@bp.route('/create/<string:pubkey>')
def create_instance(pubkey):
    aws = AwsEc2()
    try:
        id_ = aws.deploy_aws_instance(pubkey)
    except:
        return 500
    resp = jsonify({'booting':str(id_)})
    return resp, 200


@bp.route('/destroy/<string:ip>')
def destroy_instance(ip):
    aws = AwsEc2()
    try:
        id_ = aws.destroy_aws_instance(ip)
    except:
        return 500
    resp = jsonify({'terminating':str(id_)})
    return resp, 200
