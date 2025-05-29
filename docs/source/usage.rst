
### ``docs/source/usage.rst``

Usage guide
===========

Once the app is running, you can:

- **Add** a task by typing into the input field and hitting “Add”.
- **Edit** an existing task by clicking the pencil icon; a popup will appear.
- **Delete** by clicking the trash icon.

Example code snippet showing how the UI calls into ``TaskManager.add_task``:  
.. code-block:: python
   
   task_id = self.task_manager.add_task("Buy milk")
