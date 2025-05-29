from Assignment4.app.db_layer import Database

class TaskManager:
    def __init__(self, db_config):
        """Initialize the task manager with a database connection."""
        try:
            self.db = Database(**db_config)
            self.db.create_table()
        except Exception as e:
            raise RuntimeError("Failed to initialize TaskManager: " + str(e))

    def load_tasks(self):
        """Load tasks from the database."""
        try:
            return self.db.fetch_all_tasks()
        except Exception as e:
            raise RuntimeError("Failed to load tasks: " + str(e))

    def add_task(self, task_text):
        """Add a new task to the database."""
        try:
            return self.db.add_task(task_text)
        except Exception as e:
            raise RuntimeError("Failed to add task: " + str(e))
    
    def update_task(self, task_text, task_id):
        """Update an existing task in the database."""
        try:
            return self.db.update_task(task_text, task_id)
        except Exception as e:
            raise RuntimeError("Failed to update task: " + str(e))

    def delete_task(self, task_id):
        """Delete a task from the database."""
        try:
            self.db.delete_task(task_id)
        except Exception as e:
            raise RuntimeError("Failed to delete task: " + str(e))

    def close(self):
        """Close the database connection."""
        try:
            self.db.close()
        except Exception as e:
            raise RuntimeError("Failed to close the database connection: " + str(e))
