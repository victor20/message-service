from flask import Blueprint, jsonify
from marshmallow import ValidationError
from messageservice.service.errors import UsernameAlreadyExists, UserNotFound, SentReceivedError

blueprint = Blueprint('errors_handlers', __name__)

@blueprint.app_errorhandler(UserNotFound)
def user_not_found(e):
    response = jsonify({'status': 404, 'error': 'not found',
                        'message': e.args[0]})
    response.status_code = 404
    return response

@blueprint.app_errorhandler(SentReceivedError)
def user_not_found(e):
    response = jsonify({'status': 404, 'error': 'not found',
                        'message': e.args[0]})
    response.status_code = 404
    return response

@blueprint.app_errorhandler(UsernameAlreadyExists)
def user_name_exists(e):
    response = jsonify({'status': 409, 'error': 'bad request',
                        'message': e.args[0]})
    response.status_code = 409
    return response

@blueprint.app_errorhandler(ValidationError)
def bad_request(e):
    response = jsonify({'status': 400, 'error': 'bad request',
                        'message': e.args[0]})
    response.status_code = 400
    return response

@blueprint.app_errorhandler(400)
def bad_request(e):
    response = jsonify({'status': 400, 'error': 'not found',
                        'message': e.description})
    response.status_code = 400
    return response

@blueprint.app_errorhandler(404)
def not_found(e):
    response = jsonify({'status': 404, 'error': 'not found',
                        'message': e.description})
    response.status_code = 404
    return response

@blueprint.app_errorhandler(405)
def method_not_supported(e):
    response = jsonify({'status': 405, 'error': 'method not supported',
                        'message': 'the method is not supported'})
    response.status_code = 405
    return response

@blueprint.app_errorhandler(409)
def conflict(e):
    response = jsonify({'status': 409, 'error': 'conflict',
                        'message': e.description})
    response.status_code = 409
    return response

@blueprint.app_errorhandler(500)
def internal_server_error(e):
    response = jsonify({'status': 500, 'error': 'internal server error'})
    response.status_code = 500
    return response
