from flask_rebar import ResponseSchema
from flask_rebar.errors import NotFound
from marshmallow import fields
from werkzeug.exceptions import NotFound

from backend import rebar, registry
from backend.models import User


class UserSchema(ResponseSchema):
	id = fields.Integer()
	username = fields.String()
	email = fields.String()


class GetUserSchema(ResponseSchema):
	id = fields.Integer()


@registry.handles(
	rule='/user',
	method='GET',
	query_string_schema=GetUserSchema(),
	response_body_schema=UserSchema()
)
def get_user():
	args = rebar.validated_args
	user = User.query.get(args['id'])
	if not user:
		raise NotFound

	return {
		'id'      : user.id,
		'username': user.username,
		'email'   : user.email,
	}
