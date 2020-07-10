from marshmallow import fields
from werkzeug.exceptions import NotFound

from backend.api import APIBlueprint
from backend.models import User

example = APIBlueprint('example', __name__)


@example.api(
	http_path='/user',
	http_method='GET',
	input_schema={
		'id': fields.Integer(),
	},
	output_schema={
		'id'      : fields.Integer(),
		'username': fields.String(),
		'email'   : fields.String(),
	}
)
def get_user(id):
	user = User.query.get(id)
	if not user:
		raise NotFound

	return {
		'id'      : user.id,
		'username': user.username,
		'email'   : user.email,
	}
