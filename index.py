import json
import os

TASK_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, 'r') as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(TASK_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

def add_task(title, description):
    tasks = load_tasks()
    new_id = max([task['id'] for task in tasks], default=0) + 1
    task = {
        'id': new_id,
        'title': title,
        'description': description,
        'status': 'not done'
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task '{title}' added.")

def update_task(task_id, title=None, description=None):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            if title is not None:
                task['title'] = title
            if description is not None:
                task['description'] = description
            save_tasks(tasks)
            print(f"Task {task_id} updated.")
            return
    print(f"Task {task_id} not found.")

def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    print(f"Task {task_id} deleted.")

def change_status(task_id, status):
    if status not in ['not done', 'in progress', 'done']:
        print("Invalid status.")
        return
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
            save_tasks(tasks)
            print(f"Task {task_id} marked as '{status}'.")
            return
    print(f"Task {task_id} not found.")

def list_tasks(status=None):
    tasks = load_tasks()
    filtered_tasks = [task for task in tasks if status is None or task['status'] == status]
    if filtered_tasks:
        for task in filtered_tasks:
            print(f"ID: {task['id']}, Title: {task['title']}, Status: {task['status']}, Description: {task.get('description', '')}")
    else:
        print("No tasks found.")


import argparse

def main():
    parser = argparse.ArgumentParser(description='Task Tracker')
    parser.add_argument('command', choices=['add', 'update', 'delete', 'status', 'list'], help='Command to execute')
    parser.add_argument('--id', type=int, help='Task ID')
    parser.add_argument('--title', help='Title of the task')
    parser.add_argument('--description', help='Description of the task')
    parser.add_argument('--status', choices=['not done', 'in progress', 'done'], help='Status of the task')
    parser.add_argument('--list-status', choices=['not done', 'in progress', 'done'], help='Filter tasks by status')
    
    args = parser.parse_args()
    
    if args.command == 'add':
        if args.title is None:
            print("Title is required to add a task.")
            return
        add_task(args.title, args.description)
    
    elif args.command == 'update':
        if args.id is None:
            print("Task ID is required to update a task.")
            return
        update_task(args.id, args.title, args.description)
    
    elif args.command == 'delete':
        if args.id is None:
            print("Task ID is required to delete a task.")
            return
        delete_task(args.id)
    
    elif args.command == 'status':
        if args.id is None or args.status is None:
            print("Task ID and status are required to update task status.")
            return
        change_status(args.id, args.status)
    
    elif args.command == 'list':
        list_tasks(args.list_status)

if __name__ == '__main__':
    main()
