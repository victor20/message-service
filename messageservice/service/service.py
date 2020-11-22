from messageservice import db
from sqlalchemy import desc
from messageservice.model.models import User, Message
from messageservice.service.errors import UsernameAlreadyExists, UserNotFound, SentReceivedError
from messageservice.service.validate import validate_user, validate_message, validate_index, validate_delete_list
from marshmallow import ValidationError


class Service:

    def __init__(self):
        pass

    @staticmethod
    def add_user(user_dict):
        validate_user(user_dict)
        if User.query.filter_by(user_name=user_dict['user_name']).first():
            raise UsernameAlreadyExists("Username already in use")
        user = User()
        user.import_data(user_dict)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def get_users():
        return [user.export_data() for user in User.query.all()]

    @staticmethod
    def add_message(user_name, message_dict):
        user = Service.get_current_user(user_name)
        validate_message(message_dict)
        receiver = User.query.filter_by(user_name=message_dict['receiver']).first()
        if not receiver:
            raise ValidationError("Receiver not found")
        message = Message(sender=user, receiver=receiver)
        message.import_data(message_dict)
        db.session.add(message)
        db.session.commit()

    @staticmethod
    def get_messages():
        return [message.export_data() for message in Message.query.all()]

    @staticmethod
    def get_user_messages(user_name, sent_received, from_index, to_index):
        user = Service.get_current_user(user_name)
        query_parameters = Service.sent_received_or_error(sent_received)
        validate_index(from_index, to_index)
        query_result = Message.query.filter(query_parameters[0] == user, query_parameters[1] == False).order_by(
            desc(Message.id)).all()[int(from_index) - 1:int(to_index) - 1]
        messages = [message.export_data() for message in query_result]
        if messages:
            user.add_latest_message_id(messages[0]['id'])
            db.session.commit()
        return messages

    @staticmethod
    def get_new_messages(user_name):
        user = Service.get_current_user(user_name)
        query_result = Message.query.filter(Message.receiver == user, Message.id > user.latest_message_id).order_by(
            desc(Message.id)).all()
        messages = [message.export_data() for message in query_result]
        if messages:
            user.add_latest_message_id(messages[0]['id'])
            db.session.commit()
        return messages

    @staticmethod
    def delete_messages(user_name, sent_received, message_ids_dict):
        user = Service.get_current_user(user_name)
        if not user:
            raise UserNotFound("User not found")
        query_parameters = Service.sent_received_or_error(sent_received)
        validate_delete_list(message_ids_dict)
        for message_id in message_ids_dict['message_ids']:
            if Message.query.filter(query_parameters[0] == user, query_parameters[1] == False,
                                    Message.id == message_id).update({query_parameters[1]: True}) == 0:
                raise ValidationError("Message id: " + str(message_id) + " not found")
        db.session.commit()

    @staticmethod
    def get_current_user(user_name):
        user = User.query.filter_by(user_name=user_name).first()
        if not user:
            raise UserNotFound("User not found")
        return user

    @staticmethod
    def sent_received_or_error(sent_received):
        query_parameters = []
        if sent_received == "sent":
            query_parameters.append(Message.sender)
            query_parameters.append(Message.sender_deleted)
        elif sent_received == "received":
            query_parameters.append(Message.receiver)
            query_parameters.append(Message.receiver_deleted)
        else:
            raise SentReceivedError("Specify sent or received")
        return query_parameters
