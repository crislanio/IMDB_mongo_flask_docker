from app import app
import os
import tempfile

# Importamos a biblioteca de testes
import pytest

# pytest -v
def test_empty_db(client):
    rv = client.get('/')
    assert b'No entries here so far' in rv.data