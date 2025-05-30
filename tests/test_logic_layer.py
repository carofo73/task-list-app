# tests/test_logic_layer.py

import pytest
from app.logic_layer import TaskManager

class DBSuccess:
    """Dummy Database that never fails."""
    def __init__(self, **kw):
        self.created = False
        self.closed = False

    def create_table(self):
        self.created = True

    def fetch_all_tasks(self):
        return [{"id": 1, "task_text": "foo"}]

    def add_task(self, text):
        return 123

    def update_task(self, text, task_id):
        pass

    def delete_task(self, task_id):
        pass

    def close(self):
        self.closed = True

def test_init_success(monkeypatch):
    monkeypatch.setattr("app.logic_layer.Database", DBSuccess)
    tm = TaskManager(db_config={})
    assert isinstance(tm.db, DBSuccess)
    assert tm.db.created

def test_init_db_failure(monkeypatch):
    def bad_db(**kw):
        raise Exception("connect fail")
    monkeypatch.setattr("app.logic_layer.Database", bad_db)
    with pytest.raises(RuntimeError) as ei:
        TaskManager(db_config={})
    assert "Failed to initialize TaskManager" in str(ei.value)

def test_init_create_table_failure(monkeypatch):
    class DBBad(DBSuccess):
        def create_table(self):
            raise Exception("table fail")
    monkeypatch.setattr("app.logic_layer.Database", DBBad)
    with pytest.raises(RuntimeError) as ei:
        TaskManager(db_config={})
    assert "Failed to initialize TaskManager" in str(ei.value)

def test_load_tasks_success(monkeypatch):
    monkeypatch.setattr("app.logic_layer.Database", DBSuccess)
    tm = TaskManager(db_config={})
    assert tm.load_tasks() == [{"id": 1, "task_text": "foo"}]

def test_load_tasks_failure(monkeypatch):
    class DBBadFetch(DBSuccess):
        def fetch_all_tasks(self):
            raise Exception("fetch fail")
    monkeypatch.setattr("app.logic_layer.Database", DBBadFetch)
    tm = TaskManager(db_config={})
    with pytest.raises(RuntimeError) as ei:
        tm.load_tasks()
    assert "Failed to load tasks" in str(ei.value)

def test_add_task_success(monkeypatch):
    monkeypatch.setattr("app.logic_layer.Database", DBSuccess)
    tm = TaskManager(db_config={})
    assert tm.add_task("bar") == 123

def test_add_task_failure(monkeypatch):
    class DBBadAdd(DBSuccess):
        def add_task(self, text):
            raise Exception("add fail")
    monkeypatch.setattr("app.logic_layer.Database", DBBadAdd)
    tm = TaskManager(db_config={})
    with pytest.raises(RuntimeError) as ei:
        tm.add_task("bar")
    assert "Failed to add task" in str(ei.value)

@pytest.mark.parametrize("method,args,errmsg", [
    ("update_task", ("u", 5), "Failed to update task"),
    ("delete_task", (7,),     "Failed to delete task"),
])
def test_update_delete_error(method, args, errmsg, monkeypatch):
    class DBBad(DBSuccess):
        def update_task(self, text, task_id):
            raise Exception("upd fail")
        def delete_task(self, task_id):
            raise Exception("del fail")
    monkeypatch.setattr("app.logic_layer.Database", DBBad)
    tm = TaskManager(db_config={})
    with pytest.raises(RuntimeError) as ei:
        getattr(tm, method)(*args)
    assert errmsg in str(ei.value)

def test_close_success(monkeypatch):
    monkeypatch.setattr("app.logic_layer.Database", DBSuccess)
    tm = TaskManager(db_config={})
    tm.close()
    assert tm.db.closed

def test_close_failure(monkeypatch):
    class DBBadClose(DBSuccess):
        def close(self):
            raise Exception("close fail")
    monkeypatch.setattr("app.logic_layer.Database", DBBadClose)
    tm = TaskManager(db_config={})
    with pytest.raises(RuntimeError) as ei:
        tm.close()
    assert "Failed to close the database connection" in str(ei.value)
