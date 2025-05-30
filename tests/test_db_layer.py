# tests/test_db_layer.py

import pytest
import mysql.connector
from app.db_layer import Database

class DummyCursor:
    def __init__(self, fail=False, fetch_rows=None, lastrowid=1):
        self.fail = fail
        self.fetch_rows = fetch_rows or []
        self.lastrowid = lastrowid

    def execute(self, query, params=None):
        if self.fail:
            raise mysql.connector.Error("fail")

    def fetchall(self):
        # Note: in your current code, execute() would already have raised
        return self.fetch_rows

    def close(self):
        pass

class DummyConnection:
    def __init__(self, cursor):
        self._cursor = cursor
        self.committed = False
        self.rolled_back = False
        self.closed = False

    def cursor(self, **kwargs):
        return self._cursor

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True

    def close(self):
        self.closed = True

def make_db(monkeypatch, *, fail=False, fetch_rows=None, lastrowid=1):
    """
    Monkey-patch mysql.connector.connect to return a DummyConnection
    with a DummyCursor configured to fail/succeed.
    """
    cur = DummyCursor(fail=fail, fetch_rows=fetch_rows, lastrowid=lastrowid)
    conn = DummyConnection(cur)
    monkeypatch.setattr(
        "app.db_layer.mysql.connector.connect",
        lambda **kw: conn
    )
    db = Database(host="h", user="u", password="p", database="d")
    return db, conn

def test_create_table_success(monkeypatch):
    db, conn = make_db(monkeypatch, fail=False)
    db.create_table()
    assert conn.committed

def test_create_table_error(monkeypatch):
    db, conn = make_db(monkeypatch, fail=True)
    with pytest.raises(mysql.connector.Error):
        db.create_table()
    assert conn.rolled_back

def test_fetch_all_tasks_success(monkeypatch):
    rows = [{"id": 1, "task_text": "a"}]
    db, conn = make_db(monkeypatch, fail=False, fetch_rows=rows)
    assert db.fetch_all_tasks() == rows
    assert not conn.rolled_back

def test_fetch_all_tasks_error(monkeypatch):
    db, conn = make_db(monkeypatch, fail=True)
    with pytest.raises(mysql.connector.Error):
        db.fetch_all_tasks()
    # fetch errors do not trigger rollback in your code
    assert not conn.rolled_back

def test_add_task_success(monkeypatch):
    db, conn = make_db(monkeypatch, fail=False, lastrowid=42)
    assert db.add_task("foo") == 42
    assert conn.committed

def test_add_task_error(monkeypatch):
    db, conn = make_db(monkeypatch, fail=True)
    with pytest.raises(mysql.connector.Error):
        db.add_task("foo")
    assert conn.rolled_back

@pytest.mark.parametrize("method,args", [
    ("update_task", ("new text", 7)),
    ("delete_task", (7,)),
])
def test_update_delete_success(method, args, monkeypatch):
    db, conn = make_db(monkeypatch, fail=False)
    getattr(db, method)(*args)
    assert conn.committed

@pytest.mark.parametrize("method,args", [
    ("update_task", ("new text", 7)),
    ("delete_task", (7,)),
])
def test_update_delete_error(method, args, monkeypatch):
    db, conn = make_db(monkeypatch, fail=True)
    with pytest.raises(mysql.connector.Error):
        getattr(db, method)(*args)
    assert conn.rolled_back

def test_close(monkeypatch):
    db, conn = make_db(monkeypatch, fail=False)
    db.close()
    assert conn.closed
