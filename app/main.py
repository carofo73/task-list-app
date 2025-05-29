from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from app.logic_layer import TaskManager
from kivy.factory import Factory
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

Builder.load_file("ui.kv")
Builder.load_file("popup.kv")

# Configure your MySQL connection
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}


class ToDoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.task_manager = TaskManager(DB_CONFIG)
        except Exception as e:
            print("Error initializing TaskManager:", e)
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from the database and display them in the UI."""
        try:
            tasks = self.task_manager.load_tasks()
            for task in tasks:
                task_item = TaskItem(task_id=task["id"], text=task["task_text"])
                self.ids.task_list.add_widget(task_item)
        except Exception as e:
            print("Error loading tasks:", e)

    def add_task(self):
        """Add a new task to the database and UI."""
        task_text = self.ids.task_input.text.strip()
        if task_text:
            try:
                task_id = self.task_manager.add_task(task_text)
                task_item = TaskItem(task_id=task_id, text=task_text)
                self.ids.task_list.add_widget(task_item)
                self.ids.task_input.text = ""
            except Exception as e:
                print("Error adding task:", e)

    def update_task(self, task, new_text):
        """Update a task in both the database and UI."""
        try:
            self.task_manager.update_task(new_text, task.task_id)
            task.ids.task_label.text = new_text
        except Exception as e:
            print("Error updating task:", e)

    def delete_task(self, task):
        """Delete a task from the database and UI."""
        try:
            self.task_manager.delete_task(task.task_id)
            self.ids.task_list.remove_widget(task)
        except Exception as e:
            print("Error deleting task:", e)

    def open_popup(self, task):
        """Open the update popup for a specific task."""
        try:
            popup = Factory.UpdatePopup()
            popup.task = task
            popup.current_text = task.ids.task_label.text
            popup.open()
        except Exception as e:
            print("Error opening popup:", e)

    def on_stop(self):
        """Close the task manager when the app stops."""
        try:
            self.task_manager.close()
        except Exception as e:
            print("Error closing TaskManager:", e)


class TaskItem(BoxLayout):
    """Custom widget representing a task item."""

    def __init__(self, task_id, text, **kwargs):
        super().__init__(**kwargs)
        self.task_id = task_id
        try:
            self.ids.task_label.text = text
        except Exception as e:
            print("Error setting task label text:", e)


class ToDoApp(App):
    def build(self):
        return ToDoScreen()


if __name__ == "__main__":
    ToDoApp().run()
