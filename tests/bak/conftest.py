import pytest
from fastapi.testclient import TestClient

# from last.main import app
from last.types.db_engine import DBEngine


# @pytest.fixture(scope="session", autouse=True)
# def test_app():
#     client = TestClient(app)
#     yield client  # provide the test client to the tests
#     # teardown code goes here


@pytest.fixture(scope="function")
def test_db_engine():
    # Initialize the DBEngine in 'test' mode
    db_engine = DBEngine(mode="test")
    test_engine = db_engine.engine()
    yield test_engine
    db_engine.remove_db()
