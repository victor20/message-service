from marshmallow import Schema, fields, validates_schema, ValidationError
from marshmallow.validate import Range, Length


def validate_user(data):
    errors = UserSchema().validate(data)
    if errors:
        raise ValidationError(errors)


def validate_message(data):
    errors = MessageSchema().validate(data)
    if errors:
        raise ValidationError(errors)


def validate_index(from_index, to_index):
    errors = IndexSchema().validate({'from_index': from_index, 'to_index': to_index})
    if errors:
        raise ValidationError(errors)


def validate_delete_list(data):
    errors = DeleteListSchema().validate(data)
    if errors:
        raise ValidationError(errors)


class UserSchema(Schema):
    user_name = fields.String(required=True, validate=Length(max=40))
    first_name = fields.String(required=True, validate=Length(max=40))
    last_name = fields.String(required=True, validate=Length(max=40))


class MessageSchema(Schema):
    receiver = fields.String(required=True)
    message_text = fields.String(required=True)


class IndexSchema(Schema):
    from_index = fields.Integer(required=True, validate=Range(min=1))
    to_index = fields.Integer(required=True, validate=Range(min=1))

    @validates_schema
    def validate_numbers(self, data, **kwargs):
        if data["from_index"] > data["to_index"]:
            raise ValidationError("from_index must be greater than to_index")


class DeleteListSchema(Schema):
    message_ids = fields.List(fields.Integer(), required=True)




