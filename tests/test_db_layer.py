import pytest
import mysql
from app.db_layer import Database

@pytest.fixture
def db(monkeypatch):
    # A cursor that always raises ProgrammingError
    class FakeCursor:
        def execute(self, *args, **kwargs):
            raise mysql.connector.ProgrammingError("fail")
        def close(self):
            pass

    # A fake connection that hands out our FakeCursor
    class FakeConnection:
        def __init__(self):
            self._cursor = FakeCursor()
        def cursor(self, **kwargs):
            return self._cursor
        def commit(self):
            pass
        def rollback(self):
            pass

    # Monkey-patch mysql.connector.connect → FakeConnection()
    monkeypatch.setattr(
        "app.db_layer.mysql.connector.connect",
        lambda **kw: FakeConnection()
    )

    # Now Database(...) will use our FakeConnection under the hood
    return Database(host="x", user="x", password="x", database="x")

def test_create_table_raises_on_error(db):
    with pytest.raises(mysql.connector.ProgrammingError):
        db.create_table()
