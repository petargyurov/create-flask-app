import pytest

from backend import create_app, scheduler


@pytest.fixture
def app():
    app = create_app()
    yield app
    # teardown
    scheduler.shutdown()


@pytest.fixture
def client(app):
    return app.test_client()
