from flask import url_for


# TODO: use a test db instance when making the assertions

def test_get_user_success(client):
	test_id = 1
	resp = client.get(f"{url_for('example.get_user')}?id={test_id}")
	assert resp.json['id'] == test_id


def test_get_user_failure(client):
	missing_id = 100
	resp = client.get(f"{url_for('example.get_user')}id={missing_id}")
	assert resp.json['code'] == 404
