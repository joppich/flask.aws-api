from flask import request, jsonify

from . import bp
from app.lib.api_description import get_api_description
from app.lib.aws import deploy_aws_instance, destroy_aws_instance


# Set up api-appropriate errorhandling

@bp.errorhandler(404)
def not_found(error):
	resp = jsonify({'code':404,'message':'Resource not found'})
	return resp, 404

@bp.errorhandler(400)
def bad_request(error):
	resp = jsonify({'code':400,'message':'Request could not be understood'})
	return resp, 400

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


@bp.route('/create')
def create_instance():
	try:
		pubkey = str(request.args.get('pk'))
	except:
		return 400
	try:
		result = deploy_aws_instance(pubkey)
	except:
		return 500
	resp = jsonify(result)
	return resp, 200


@bp.route('/destroy')
def destroy_instance():
	try:
		ip = str(request.args.get('ip'))
	except:
		return 400
	try:
		result = destroy_aws_instance(ip)
	except:
		return 500
	resp = jsonify(result)
	return resp, 200
