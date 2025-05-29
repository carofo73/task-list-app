import pytest
from app.logic_layer import TaskManager


class DummyDB:
    def __init__(self):
        self.created = False

    def create_table(self):
        self.created = True

    def fetch_all_tasks(self):
        return [{"id": 1, "task_text": "foo"}]

    def add_task(self, text):
        return 42

    def update_task(self, text, id):
        pass

    def delete_task(self, id):
        pass

    def close(self):
        pass


@pytest.fixture
def tm(monkeypatch):
    monkeypatch.setattr("app.logic_layer.Database", DummyDB)
    return TaskManager(db_config={})


def test_load_tasks(tm):
    tasks = tm.load_tasks()
    assert tasks == [{"id": 1, "task_text": "foo"}]


def test_add_update_delete(tm):
    new_id = tm.add_task("bar")
    assert new_id == 42
    # these should not raise
    tm.update_task("baz", 42)
    tm.delete_task(42)
