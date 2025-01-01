import json
import os
import sys
from datetime import datetime

# Path to the JSON file
TASKS_FILE = "Tasks.json"

def load_tasks():
    """Load tasks from the JSON file."""
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'w') as file:
            json.dump([], file)
    with open(TASKS_FILE, 'r') as file:
        return json.load(file)

def save_tasks(tasks):
    """Save tasks to the JSON file."""
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

def add_task(description):
    """Add a new task."""
    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_task['id']})")

def update_task(task_id, description):
    """Update the description of an existing task."""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print("Task updated successfully")
            return
    print(f"No task found with ID: {task_id}")

def delete_task(task_id):
    """Delete a task by ID."""
    tasks = load_tasks()
    updated_tasks = [task for task in tasks if task["id"] != task_id]
    if len(tasks) == len(updated_tasks):
        print(f"No task found with ID: {task_id}")
    else:
        save_tasks(updated_tasks)
        print("Task deleted successfully")

def mark_task(task_id, status):
    """Mark a task as in-progress or done."""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task marked as {status}")
            return
    print(f"No task found with ID: {task_id}")

def list_tasks(filter_status=None):
    """List all tasks or tasks filtered by status."""
    tasks = load_tasks()
    if filter_status:
        tasks = [task for task in tasks if task["status"] == filter_status]
    if not tasks:
        print("No tasks found")
        return
    for task in tasks:
        print(f"[{task['id']}] {task['description']} ({task['status']})")

def main():
    """Main CLI logic."""
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [options]")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Usage: task-cli add <description>")
            return
        description = sys.argv[2]
        add_task(description)

    elif command == "update":
        if len(sys.argv) < 4:
            print("Usage: task-cli update <id> <description>")
            return
        task_id = int(sys.argv[2])
        description = sys.argv[3]
        update_task(task_id, description)

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: task-cli delete <id>")
            return
        task_id = int(sys.argv[2])
        delete_task(task_id)

    elif command == "mark-in-progress":
        if len(sys.argv) < 3:
            print("Usage: task-cli mark-in-progress <id>")
            return
        task_id = int(sys.argv[2])
        mark_task(task_id, "in-progress")

    elif command == "mark-done":
        if len(sys.argv) < 3:
            print("Usage: task-cli mark-done <id>")
            return
        task_id = int(sys.argv[2])
        mark_task(task_id, "done")

    elif command == "list":
        if len(sys.argv) == 2:
            list_tasks()
        else:
            filter_status = sys.argv[2]
            list_tasks(filter_status)

    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
