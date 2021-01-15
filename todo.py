import sys
import os
from datetime import date

arguments = sys.argv   # 1st argument will be filename, 2nd argument will be command

command = ""

if len(arguments) > 1:
    command = arguments[1]

if command.lower() == "help" or command == "":
    help_output = """
    Usage :-
$ ./todo add "todo item"  # Add a new todo
$ ./todo ls               # Show remaining todos
$ ./todo del NUMBER       # Delete a todo
$ ./todo done NUMBER      # Complete a todo
$ ./todo help             # Show usage
$ ./todo report           # Statistics
"""
    sys.stdout.buffer.write(help_output.encode('utf8'))
# using print() giving a middle dot(U+00B7) at the end of each strings and same in few other cases also.

elif command.lower() == "add":
    if len(arguments) > 2:
        with open("todo.txt", "a") as file:
            file.write(arguments[2]+"\n")
        print(f'Added todo: "{arguments[2]}"')
    else:
        print("Error: Missing todo string. Nothing added!")

elif command.lower() == "ls":
    if os.path.isfile('todo.txt'):
        with open("todo.txt", "r") as file:
            file_lines = file.readlines()
            file_lines.reverse()
        count = len(file_lines)+1
        for line in file_lines:
            count -= 1
            output = f"[{count}] {line.strip()}\n"
            sys.stdout.buffer.write(output.encode('utf8'))  # broken print()
    else:
        print("There are no pending todos!")

elif command.lower() == "del":
    if len(arguments) > 2:     # checking if "del" followed by a arg.
        try:
            if int(arguments[2]) > 0:      # removing dependency of "0" because "-1" is used
                file = open("todo.txt", "r")
                file_lines = file.readlines()
                del file_lines[int(arguments[2])-1]
                with open("todo.txt", "w") as edited_file:
                    for line in file_lines:
                        edited_file.write(line)
                print(f"Deleted todo #{arguments[2]}")
            else:
                print(f"Error: todo #{arguments[2]} does not exist. Nothing deleted.")

        except IndexError:
            print(f"Error: todo #{arguments[2]} does not exist. Nothing deleted.")
    else:
        print("Error: Missing NUMBER for deleting todo.")

elif command.lower() == "done":
    if len(arguments) > 2:    # checking if "done" followed by a arg.
        try:
            if int(arguments[2]) > 0:    # removing dependency of "0" because "-1" is used.
                today = date.today()
                formatted_date = today.strftime("%Y-%m-%d")

                file_todo = open("todo.txt", "r")
                file_todo_lines = file_todo.readlines()
                with open("done.txt", "a") as file_done:
                    file_done.write(f"x {formatted_date} {file_todo_lines[int(arguments[2])-1]}")

                del file_todo_lines[int(arguments[2])-1]
                with open("todo.txt", "w") as edited_file:
                    for line in file_todo_lines:
                        edited_file.write(line)
                print(f"Marked todo #{int(arguments[2])} as done.")
            else:
                print(f"Error: todo #{arguments[2]} does not exist.")
        except IndexError:
            print(f"Error: todo #{arguments[2]} does not exist.")
    else:
        print("Error: Missing NUMBER for marking todo as done.")

elif command.lower() == "report":
    today = date.today()
    formatted_date = today.strftime("%Y-%m-%d")

    if os.path.isfile("todo.txt"):
        file_todo = open("todo.txt", "r")
        file_todo_lines = file_todo.readlines()
        count_todo = 0
        for line in file_todo_lines:
            count_todo += 1  # pending_tasks = count_todo

        if os.path.isfile("done.txt"):
            file_done = open("done.txt", "r")
            file_done_lines = file_done.readlines()
            count_done = 0
            for line in file_done_lines:
                count_done += 1     # completed_tasks = count_done
            output = f"{formatted_date} Pending : {count_todo} Completed : {count_done}"
            sys.stdout.buffer.write(output.encode('utf8'))   # broken print()
        else:
            print(f"{formatted_date} Pending : {count_todo} Completed : 0")
    else:
        print(f"{formatted_date} Pending : 0 Completed : 0")
