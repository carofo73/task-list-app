import mysql.connector


class Database:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host, user=user, password=password, database=database
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def create_table(self):
        """Create the tasks table if it doesn't exist."""
        try:
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    task_text VARCHAR(255) NOT NULL
                )
                """
            )
            self.connection.commit()
        except mysql.connector.Error as err:
            self.connection.rollback()
            print("Error occurred while creating table:", err)
            raise

    def fetch_all_tasks(self):
        """Retrieve all tasks from the database."""
        try:
            self.cursor.execute("SELECT id, task_text FROM tasks")
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print("Error occurred while fetching tasks:", err)
            raise

    def add_task(self, task_text):
        """Insert a new task into the database."""
        try:
            self.cursor.execute("INSERT INTO tasks (task_text) VALUES (%s)", (task_text,))
            self.connection.commit()
            return self.cursor.lastrowid
        except mysql.connector.Error as err:
            self.connection.rollback()
            print("Error occurred while adding task:", err)
            raise

    def update_task(self, task_text, task_id):
        """Update a task in the database."""
        try:
            self.cursor.execute(
                "UPDATE tasks SET task_text = %s WHERE id = %s", (task_text, task_id,)
            )
            self.connection.commit()
        except mysql.connector.Error as err:
            self.connection.rollback()
            print("Error occurred while updating task:", err)
            raise

    def delete_task(self, task_id):
        """Delete a task from the database."""
        try:
            self.cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            self.connection.commit()
        except mysql.connector.Error as err:
            self.connection.rollback()
            print("Error occurred while deleting task:", err)
            raise

    def close(self):
        """Close the database connection."""
        self.connection.close()
