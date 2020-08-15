import logging
import pathlib
import sys
import traceback

from flask import has_request_context, request

config = {
	'version'   : 1,
	'formatters': {
		'custom': {
			'()'    : 'backend.logger.CustomFormatter',
			'format': '%(asctime)s | %(levelname)s | %(source)s | %(method)s | %(path)s | %(params)s | %(message)s',
		}},
	'handlers'  : {
		'wsgi'         : {
			'class'    : 'logging.StreamHandler',
			'stream'   : 'ext://flask.logging.wsgi_errors_stream',
			'formatter': 'custom'
		},
		'rotating_file': {
			'class'      : 'logging.handlers.RotatingFileHandler',
			'filename'   : 'backend.log',
			'maxBytes'   : 1024 * 1024,
			'backupCount': 5,
			'formatter'  : 'custom'
		}
	},
	'root'      : {
		'level'   : 'INFO',
		'handlers': ['wsgi', 'rotating_file']
	}
}


class CustomFormatter(logging.Formatter):
	def format(self, record):
		exc_type, exc_value, exc_traceback = sys.exc_info()
		tb = traceback.extract_tb(exc_traceback)
		tb = tb[-1] if tb else None

		if tb:
			path = pathlib.PurePath(tb.filename)
			view = path.parts[-2]
			file_name = path.with_suffix('').parts[-1]
			func_name = tb.name
			line_no = tb.lineno
		else:
			path = pathlib.PurePath(record.pathname)
			view = path.parts[-2]
			file_name = path.with_suffix('').parts[-1]
			func_name = record.funcName
			line_no = record.lineno

		record.source = f"{view}.{file_name}.{func_name}::{line_no}"

		if has_request_context():
			record.url = request.url
			record.remote_addr = request.remote_addr
			record.path = request.path
			record.host = request.host
			record.method = request.method
			record.params = request.query_string.decode('utf-8') or None
		else:
			record.url = None
			record.remote_addr = None
			record.path = None
			record.host = None
			record.method = None
			record.params = None

		return super().format(record)
