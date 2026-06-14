import argparse
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

class Task:
    def __init__(self, title, completed=False):
        self.title = title
        self.completed = completed
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at
        }

class TaskManager:
    def __init__(self):
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as f:
                return json.load(f)
        return []

    def _save_tasks(self):
        with open(TASKS_FILE, "w") as f:
            json.dump(self.tasks, f, indent=2)

    def add_task(self, title):
        task = Task(title)
        self.tasks.append(task.to_dict())
        self._save_tasks()
        print(f"✅ Task added: '{title}'")

    def complete_task(self, title):
        for task in self.tasks:
            if task["title"].lower() == title.lower():
                task["completed"] = True
                self._save_tasks()
                print(f"🎉 Task marked complete: '{title}'")
                return
        print(f"❌ Task not found: '{title}'")

    def list_tasks(self):
        if not self.tasks:
            print("No tasks found.")
            return
        for i, task in enumerate(self.tasks, 1):
            status = "✔" if task["completed"] else "✘"
            print(f"{i}. [{status}] {task['title']} (added: {task['created_at']})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI Task Manager")
    subparsers = parser.add_subparsers(dest="command")

    # add-task command
    add_parser = subparsers.add_parser("add-task", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Task title")

    # complete-task command
    complete_parser = subparsers.add_parser("complete-task", help="Mark a task as complete")
    complete_parser.add_argument("title", type=str, help="Task title to complete")

    # list command
    subparsers.add_parser("list", help="List all tasks")

    args = parser.parse_args()
    manager = TaskManager()

    if args.command == "add-task":
        manager.add_task(args.title)
    elif args.command == "complete-task":
        manager.complete_task(args.title)
    elif args.command == "list":
        manager.list_tasks()
    else:
        parser.print_help()