from flask import Blueprint, request, jsonify, abort
from marshmallow import ValidationError
from sqlalchemy import desc

from messageservice import db
from messageservice.models import Message, User
from messageservice.validate import validate_user, validate_message, validate_index, validate_delete_list

blueprint = Blueprint('api', __name__)


@blueprint.route("/api/users", methods=['POST'])
def add_user():
    validate_user(request.json)
    if User.query.filter_by(user_name=request.json['user_name']).first():
        abort(409, "Username already in use")
    user = User()
    user.import_data(request.json)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User successfully created"}), 201


@blueprint.route("/api/users", methods=['GET'])
def get_users():
    users = [user.export_data() for user in User.query.all()]
    return jsonify({'users': users})


@blueprint.route("/api/users/<string:user_name>/messages", methods=['POST'])
def add_message(user_name: str):
    user = get_user_or_404(user_name)
    validate_message(request.json)
    receiver = User.query.filter_by(user_name=request.json['receiver']).first()
    if not receiver:
        raise ValidationError("Receiver not found")
    message = Message(sender=user, receiver=receiver)
    message.import_data(request.json)
    db.session.add(message)
    db.session.commit()
    return jsonify({"message": "Message successfully sent"}), 201


@blueprint.route("/api/messages", methods=['GET'])
def get_messages():
    messages = [message.export_data() for message in Message.query.all()]
    return jsonify({'messages': messages})


@blueprint.route("/api/users/<string:user_name>/messages/<string:sent_received>", methods=['GET'])
def get_user_messages(user_name, sent_received):
    user = get_user_or_404(user_name)
    query_parameters = sent_received_or_404(sent_received)
    from_index = request.args.get('from')
    to_index = request.args.get('to')
    validate_index({'from_index': from_index, 'to_index': to_index})
    query_result = Message.query.filter(query_parameters[0] == user, query_parameters[1] == False).order_by(desc(Message.id)).all()[int(from_index)-1:int(to_index)-1]
    messages = [message.export_data() for message in query_result]
    if messages:
        user.add_latest_message_id(messages[0]['id'])
        db.session.commit()
    return jsonify({'messages': messages})


@blueprint.route("/api/users/<string:user_name>/messages/received/new", methods=['GET'])
def get_new_messages(user_name):
    user = get_user_or_404(user_name)
    query_result = Message.query.filter(Message.receiver == user, Message.id > user.latest_message_id).order_by(desc(Message.id)).all()
    messages = [message.export_data() for message in query_result]
    if messages:
        user.add_latest_message_id(messages[0]['id'])
        db.session.commit()
    return jsonify({'messages': messages})


@blueprint.route("/api/users/<string:user_name>/messages/<string:sent_received>", methods=['DELETE'])
def delete_messages(user_name, sent_received):
    user = get_user_or_404(user_name)
    query_parameters = sent_received_or_404(sent_received)
    validate_delete_list(request.json)
    message_ids = request.json['message_ids']
    for message_id in message_ids:
        if Message.query.filter(query_parameters[0] == user, query_parameters[1] == False, Message.id == message_id).update({query_parameters[1]: True}) == 0:
            raise ValidationError("Message id: " + str(message_id) + " not found")
    db.session.commit()
    return jsonify({}), 204


def get_user_or_404(user_name):
    return User.query.filter_by(user_name=user_name).first_or_404(description="User not found")


def sent_received_or_404(sent_received):
    query_parameters = []
    if sent_received == "sent":
        query_parameters.append(Message.sender)
        query_parameters.append(Message.sender_deleted)
    elif sent_received == "received":
        query_parameters.append(Message.receiver)
        query_parameters.append(Message.receiver_deleted)
    else:
        abort(404)
    return query_parameters






