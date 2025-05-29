Overview
========

The Task List App is a Kivy-based GUI for managing simple to-do items.  
It persists tasks in a MySQL database via ``db_layer.Database`` :contentReference[oaicite:0]{index=0} and exposes a clean API in ``logic_layer.TaskManager`` :contentReference[oaicite:1]{index=1}.

Key features:

- Add, edit, delete tasks
- Persistent storage with MySQL
- Popup-based inline editing
- Modular architecture separating UI, logic, and DB layers
