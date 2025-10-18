import os
import tempfile
import pytest

from app import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    # use a temporary CSV for tests
    tmp_csv = tmp_path / "test_submissions.csv"
    monkeypatch.setenv('AKASHIA_CSV_PATH', str(tmp_csv))
    monkeypatch.setenv('ADMIN_PASSWORD', 'testpass')
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_get(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Banco de Sue' in rv.data


def test_post_and_export(client):
    # post a submission
    rv = client.post('/', data={'name': 'Alice', 'email': 'a@b.c', 'region': 'Lima', 'message': 'Sue\u00f1o'})
    assert rv.status_code == 302  # redirect to success

    # unauthorized export
    rv = client.get('/export.csv')
    assert rv.status_code == 403

    # authorized via query
    rv = client.get('/export.csv?admin=testpass')
    assert rv.status_code == 200
    assert b'Alice' in rv.data
