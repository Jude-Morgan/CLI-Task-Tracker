import sys
import json
import os
from datetime import datetime

# Path to the JSON file
TASKS_FILE = "tasks.json"

# Make sure the JSON file exists
if not os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, 'w') as file:
        json.dump([], file)

# Load tasks from the JSON file
def load_tasks():
    with open(TASKS_FILE, 'r') as file:
        return json.load(file)

# Save tasks to JSON file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# Generate a unique ID for a new task
def generate_task_id(tasks):
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1

# Add a new task
def add_task(description):
    tasks = load_tasks()
    task_id = generate_task_id(tasks)
    new_task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat(),
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")

# Update a task's description
def update_task(task_id, description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print("Task updated successfully")
            return
    print(f"Task with ID {task_id} not found")

# Delete a task
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    print("Task deleted successfully")

# Mark a task with a specific status
def mark_task(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task marked as {status}")
            return
    print(f"Task with ID {task_id} not found")

# List tasks, optionally filtered by status
def list_tasks(status=None):
    tasks = load_tasks()
    if status:
        tasks = [task for task in tasks if task["status"] == status]
    if tasks:
        for task in tasks:
            print(f"[{task['id']}] {task['description']} - {task['status']} (Created: {task['createdAt']}, Updated: {task['updatedAt']})")
    else:
        print("No tasks found")

# Main function to handle command-line arguments
def main():
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [<args>...]")
        return

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "add" and len(args) == 1:
        add_task(args[0])
    elif command == "update" and len(args) == 2:
        try:
            update_task(int(args[0]), args[1])
        except ValueError:
            print("Task ID must be a number")
    elif command == "delete" and len(args) == 1:
        try:
            delete_task(int(args[0]))
        except ValueError:
            print("Task ID must be a number")
    elif command == "mark-in-progress" and len(args) == 1:
        try:
            mark_task(int(args[0]), "in-progress")
        except ValueError:
            print("Task ID must be a number")
    elif command == "mark-done" and len(args) == 1:
        try:
            mark_task(int(args[0]), "done")
        except ValueError:
            print("Task ID must be a number")
    elif command == "list":
        if len(args) == 0:
            list_tasks()
        elif args[0] in {"done", "todo", "in-progress"}:
            list_tasks(args[0])
        else:
            print("Invalid status. Use 'done', 'todo', or 'in-progress'")
    else:
        print("Invalid command or arguments")


if __name__ == "__main__":
    main()
