from flask import Blueprint, request, jsonify
from messageservice.service.service import Service


blueprint = Blueprint('api', __name__)


@blueprint.route("/api/users", methods=['POST'])
def add_user():
    Service.add_user(request.json)
    return jsonify({"message": "User successfully created"}), 201


@blueprint.route("/api/users", methods=['GET'])
def get_users():
    return jsonify({'users': Service.get_users()})


@blueprint.route("/api/users/<string:user_name>/messages", methods=['POST'])
def add_message(user_name: str):
    Service.add_message(user_name, request.json)
    return jsonify({"message": "Message successfully sent"}), 201


@blueprint.route("/api/messages", methods=['GET'])
def get_messages():
    return jsonify({'messages': Service.get_messages()})


@blueprint.route("/api/users/<string:user_name>/messages/<string:sent_received>", methods=['GET'])
def get_user_messages(user_name, sent_received):
    from_index = request.args.get('from')
    to_index = request.args.get('to')
    return jsonify({'messages': Service.get_user_messages(user_name, sent_received, from_index, to_index)})


@blueprint.route("/api/users/<string:user_name>/messages/received/new", methods=['GET'])
def get_new_messages(user_name):
    return jsonify({'messages': Service.get_new_messages(user_name)})


@blueprint.route("/api/users/<string:user_name>/messages/<string:sent_received>", methods=['DELETE'])
def delete_messages(user_name, sent_received):
    Service.delete_messages(user_name, sent_received, request.json)
    return jsonify({}), 204







