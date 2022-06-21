import logging

import pytest

from db.init import create_session

logging.getLogger('uvicorn.error')


def test_create_session():
    with create_session() as session:
        assert session is not None


def test_create_session_twice():
    with create_session() as session:
        assert session is not None
    with create_session() as session:
        assert session is not None


def test_create_session_and_rise_exception():
    with pytest.raises(Exception):
        with create_session() as session:
            assert session is not None
            raise Exception('test')

