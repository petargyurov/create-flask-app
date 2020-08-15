from backend import db, scheduler
from backend.models import User


def print_number_of_users():
	with scheduler.app.app_context():
		users_n = db.session.query(User).count()
		print(f"{users_n} users in database")
