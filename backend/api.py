from functools import wraps

from flask import Blueprint, jsonify
from webargs import dict2schema
from webargs.flaskparser import FlaskParser
from werkzeug.wrappers import Response

parser = FlaskParser()
inputs = parser.use_kwargs


def outputs(output_dict):
	schema = dict2schema(output_dict)()

	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			result = func(*args, **kwargs)
			if isinstance(result, Response):
				return result
			result = schema.dump(result)
			return jsonify(result)

		return wrapper

	return decorator


class APIBlueprint(Blueprint):
	def api(self, http_path, http_method,
			input_schema=None, output_schema=None):
		def decorator(orig_func):
			func = orig_func
			func = outputs(output_schema or {})(func)

			location = 'querystring' if http_method.upper() == 'GET' else 'json'
			func = inputs(input_schema or {}, location=location)(func)

			func = self.route(http_path, methods=[http_method])(func)
			func = wraps(orig_func)(func)
			return func

		return decorator
