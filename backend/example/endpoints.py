from backend.api import APIBlueprint
from marshmallow import fields
from webargs import dict2schema
from werkzeug.exceptions import NotImplemented

example = APIBlueprint('example', __name__)


@example.api(
	http_path='/example_get',
	http_method='GET',
	input_schema={
		'animal': fields.String(),
	},
	output_schema={
		'animal': fields.Nested(dict2schema({
			'name': fields.String(),
			'type': fields.String(),
			'age': fields.Integer()
		}))
	}
)
def example_get(animal):
	if animal == 'cat':
		info = {
			'name': 'Mr. Tibbles',
			'type': 'Cat',
			'age': 8
		}
	elif animal == 'dog':
		info = {
			'name': 'Floofy',
			'type': 'Dog',
			'age' : 7
		}
	else:
		raise NotImplemented

	return {
		'animal': info
	}
