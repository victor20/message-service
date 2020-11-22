from datetime import datetime
from messageservice import db


class User(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(40), unique=True, nullable=False)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    latest_message_id = db.Column(db.Integer, nullable=False, default=0)

    sent_messages = db.relationship('Message', backref='sender',
                                    lazy='select', foreign_keys='Message.sender_id')
    received_messages = db.relationship('Message', backref='receiver',
                                        lazy='select', foreign_keys='Message.receiver_id')

    def add_latest_message_id(self, message_id):
        if message_id > self.latest_message_id:
            self.latest_message_id = message_id

    def import_data(self, data):
        self.user_name = data['user_name']
        self.first_name = data['first_name']
        self.last_name = data['last_name']

    def export_data(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'latest_message_id': self.latest_message_id
        }

    def __repr__(self):
        return f"User('{self.id}','{self.user_name}', '{self.first_name}', '{self.last_name}')"


class Message(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True)
    message_text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    sender_deleted = db.Column(db.Boolean, nullable=False, default=False)
    receiver_deleted = db.Column(db.Boolean, nullable=False, default=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def import_data(self, data):
        self.message_text = data['message_text']

    def export_data(self):
        return {
            'id': self.id,
            'sender': self.sender.user_name,
            'receiver': self.receiver.user_name,
            'message_text': self.message_text,
            'date': self.date
        }

    def __repr__(self):
        return f"Message('{self.id}','{self.sender_id}', '{self.receiver_id}', '{self.message_text}', '{self.date}')"