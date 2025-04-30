tasks = []  # This empty list will store our tasks

while True:
    tool_choice = input("What do you want to use? (calculator/todo/exit): ").lower()

    if tool_choice == "calculator":
        while True:
            num1 = float(input("Enter the first number: "))
            q = input("Enter the operation (+, -, *, /) or 'back' to choose tool: ").strip().lower()
            num2 = float(input("Enter the second number: "))
            
            if q == "back":
                break  # Go back to tool choice
            elif q == "+":
                print("here you go:", num1 + num2)
            elif q == "-":
                print("here you go:", num1 - num2)
            elif q == "hello":
                print("hello there")
            elif q == "*":
                print("here you go:", num1 * num2)
            
            elif q == "/":
                if num2 == 0:
                    print("Error: Division by zero is not allowed.")
                else:
                    print("here you go:", num1 / num2)
            elif q == "**":
                print("Here you go:", num1 ** num2)
            else:
                print("Sorry, invalid operation.")
    elif tool_choice == "todo":
        tasks = []  # Initialize an empty list
        try:
            print("Attempting to load tasks from todo.txt...")
            with open("todo.txt", "r") as file:
                for line in file:
                    task = line.strip()
                    tasks.append(task)
                    print(f"Loaded task: '{task}'")
            print("To-do list loaded from file.")
        except FileNotFoundError:
            print("No existing to-do list file found.")

        while True:
            todo_action = input("What do you want to do with the to-do list? (add/view/remove/remove all/back): ").lower()
            if todo_action == "add":
                task = input("Enter the task to add: ")
                tasks.append(task)
                try:
                    with open("todo.txt", "w") as file:
                        for item in tasks:
                            file.write(item + "\n")
                    print(f"Task '{task}' added and saved to todo.txt.")
                except Exception as e:
                    print(f"Error saving to todo.txt: {e}")
            elif todo_action == "view":
                if not tasks:
                    print("Your to-do list is empty.")
                else:
                    print("Your to-do list:")
                    for index, task in enumerate(tasks):
                        print(f"{index + 1}. {task}")
            elif todo_action == "remove":
                if not tasks:
                    print("Your to-do list is empty. Nothing to remove.")
                else:
                    print("Your to-do list:")
                    for index, task in enumerate(tasks):
                        print(f"{index + 1}. {task}")
                    try:
                        task_number = int(input("Enter the number of the task to remove: "))
                        if 1 <= task_number <= len(tasks):
                            removed_task = tasks.pop(task_number - 1)
                            with open("todo.txt", "w") as file:
                                for item in tasks:
                                    file.write(item + "\n")
                            print(f"Task '{removed_task}' removed and saved to todo.txt.")
                        else:
                            print("Invalid task number.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
            elif todo_action == "remove all":
                confirm = input("Are you sure you want to remove all tasks? (yes/no): ").lower()
                if confirm == "yes":
                    tasks = []  # Clear the tasks list in memory
                    try:
                        with open("todo.txt", "w") as file:
                            pass  # Open in write mode to clear the file
                        print("All tasks removed and todo.txt cleared.")
                    except Exception as e:
                        print(f"Error clearing todo.txt: {e}")
                else:
                    print("Remove all cancelled.")
            elif todo_action == "back":
                break  # Go back to the tool choice
            else:
                print("Invalid to-do list action. Please use 'add', 'view', 'remove', 'remove all', or 'back'.")
    elif tool_choice == "exit":
        print("Goodbye!")
        break  # Exit the entire program
    else:
        print("Invalid choice. Please enter 'calculator', 'todo', or 'exit'.")