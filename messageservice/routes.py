from flask import Blueprint, request, jsonify, abort
from marshmallow import ValidationError
from messageservice import db
from messageservice.models import Message, User
from messageservice.validate import validate_user, validate_message, validate_index, validate_delete_list

blueprint = Blueprint('api', __name__)


@blueprint.route("/api/users", methods=['POST'])
def add_user():
    validate_user(request.json)

    if User.query.filter_by(user_name=request.json['user_name']).first():
        abort(409, "Error username already in use")

    user = User()
    user.import_data(request.json)
    db.session.add(user)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

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

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return jsonify({"message": "Message successfully sent"}), 201


@blueprint.route("/api/messages", methods=['GET'])
def get_messages():
    messages = [message.export_data() for message in Message.query.all()]
    return jsonify(
        {'messages': messages})


@blueprint.route("/api/users/<string:user_name>/messages/received", methods=['GET'])
def get_messages_by_index(user_name):
    user = get_user_or_404(user_name)
    from_index = request.args.get('from')
    to_index = request.args.get('to')
    validate_index({'from_index': from_index, 'to_index': to_index})
    messages = [message.export_data() for message in user.received_messages[int(from_index)-1:int(to_index)-1]]

    if messages:
        user.add_latest_message_id(messages[-1]['id'])
        db.session.commit()

    return jsonify({'messages': messages})


@blueprint.route("/api/users/<string:user_name>/messages/received/new", methods=['GET'])
def get_new_messages(user_name):
    user = get_user_or_404(user_name)
    messages = [message.export_data() for message in
                Message.query.filter(Message.receiver==user, Message.id > user.latest_message_id).all()]

    if messages:
        user.add_latest_message_id(messages[-1]['id'])
        db.session.commit()

    return jsonify({'messages': messages})


@blueprint.route("/api/users/<string:user_name>/messages", methods=['DELETE'])
def delete_messages(user_name):
    user = get_user_or_404(user_name)
    validate_delete_list(request.json)
    Message.query.filter(Message.receiver==user, Message.id.in_(request.json['messages'])).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({}), 204


def get_user_or_404(user_name):
    return User.query.filter_by(user_name=user_name).first_or_404(description="User not found")





