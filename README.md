# To-Do Project

A simple but powerful command-line To-Do list manager built with Python.  
Supports colored output, deadline tracking, priority filtering, task status, and detailed logging.

---

## 🛠 Features

- 📌 Add, view, delete, and complete tasks
- 🎨 Colored output for priorities, deadlines, and statuses
- 📁 Save tasks to `tasks.json`
- 🔍 Filter tasks by category or priority
- ⚠️ Show overdue tasks
- 📝 All actions are logged into `todo.log` using Python `logging`
- 🧩 Modular architecture (`main.py`, `cli.py`, `utils.py`, `models.py`)

---

## 📸 Demo

```bash
Menu:
[1] View Task list
[2] Add new task
[3] Delete task
[4] Complete task
[5] Find task by category
[6] Find task by priority level
[7] Find overdue tasks
[8] Exit
```

---

## 💡 Technologies

- Python 3.10+
- `colorama` for CLI coloring
- `logging` for structured logging
- Built-in modules: `datetime`, `json`, `pathlib`

---

## 🧱 Project Structure

```
To-Do-project/
│
├── main.py         # Entry point
├── cli.py          # Menu and user interface
├── utils.py        # TaskManager class and helper functions
├── models.py       # Task data class
├── tasks.json      # Task storage (optional)
├── todo.log        # Runtime logs (ignored or local)
├── .gitignore
└── LICENSE
```

---

## 📦 Installation

```bash
git clone https://github.com/your_username/To-Do-project.git
cd To-Do-project
pip install colorama
python main.py
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
