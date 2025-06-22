from colorama import Fore, Style
from datetime import datetime, timedelta
from models import Task
from pathlib import Path
import logging
import json


def colorize_priority(priority: str) -> str:
    if priority == "High":
        return Fore.RED + priority + Style.RESET_ALL
    elif priority == "Medium":
        return Fore.YELLOW + priority + Style.RESET_ALL
    else:
        return Fore.GREEN + priority + Style.RESET_ALL


def colorize_deadline(deadline_str: str) -> str:
    try:
        deadline = datetime.strptime(deadline_str, "%d-%m-%Y").date()
        days_left = (deadline - datetime.today().date()).days

        if days_left < 0:
            return Fore.RED + deadline_str + Style.RESET_ALL
        elif days_left <= 3:
            return Fore.YELLOW + deadline_str + Style.RESET_ALL
        else:
            return Fore.GREEN + deadline_str + Style.RESET_ALL

    except Exception:
        return deadline_str


def colorize_status(done: bool) -> str:
    if done:
        return Fore.GREEN + '✅ Completed' + Style.RESET_ALL
    else:
        return Fore.RED + '❌ Not completed'+ Style.RESET_ALL


def style_tittle(title: str) -> str:
    return Style.BRIGHT + title + Style.RESET_ALL


def colored_aligned(text: str, width: int, color=Fore.RESET, align='^') -> str:
    formatted = f"{text:{align}{width}}"
    return f"{color}{formatted}{Style.RESET_ALL}"




logging.basicConfig(
    filename='todo.log',
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)


class TaskManager:
    def __init__(self):
        self.tasks = []


    def load_data(self):
        path = Path('tasks.json')
        logging.debug(f"Checking if file exists at {path.resolve()}")
        if path.exists():
            try:
                with open('tasks.json', 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
                logging.info(f"Loaded {len(self.tasks)} tasks from {path.name}")

            except json.JSONDecodeError as e:
                print('Error: tasks.json contained invalid JSON.')
                logging.error(f"JSONDecodeError while loading {path.name}: {e}")
            except OSError as e:
                print(f'Error: Failed to read file: {e}')
                logging.error(f"OSError while reading {path.name}: {e}")

        else:
            logging.warning(f"File {path.name} not found. Starting with empty task list.")




    def save_data(self):
        path = Path('tasks.json')
        try:
            with open('tasks.json', 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=4)
            logging.info(f"Saved {len(self.tasks)} tasks to {path.name}")

        except OSError as e:
            logging.error(f"Failed to write to {path.name}: {e}")




    def add_task(self):
        try:
            input_new_task_text = input('Input new task text or exit: ').strip()
            logging.debug(f"User entered task text: '{input_new_task_text}'")

            if input_new_task_text.lower() == 'exit':
                print('Returning to menu...')
                logging.info('User exited task addition.')
                return

            input_new_task_category = input('Input new task category: ').strip()
            logging.debug(f'User entered task category: "{input_new_task_category}"')

            print('Input new task priority:\n[1] Low\n[2] Medium\n[3] High')
            input_priority_choice = int(input('> '))
            logging.debug(f"User selected priority option: {input_priority_choice}")

            if input_priority_choice in range(1, 4):
                if input_priority_choice == 1:
                    selected_priority_level = 'Low'
                elif input_priority_choice == 2:
                    selected_priority_level = 'Medium'
                else:
                    selected_priority_level = 'High'
                logging.debug(f"Mapped priority level: {selected_priority_level}")
            else:
                print('Error: Input out of range.')
                logging.warning(f"Invalid priority input: {input_priority_choice}")
                return

            input_days_until_deadline = int(input('Input days until deadline: '))
            logging.debug(f"User entered deadline in days: {input_days_until_deadline}")

            deadline = datetime.today() + timedelta(days=input_days_until_deadline)
            deadline_str = deadline.strftime("%d-%m-%Y")
            logging.debug(f"Calculated deadline date: {deadline_str}")

            new_task = Task(input_new_task_text, input_new_task_category, selected_priority_level, deadline)
            self.tasks.append(new_task.to_dict())
            self.save_data()

            print(f'Task "{new_task.text}" added!')
            logging.info(f'Task added: {new_task.text}, Category: {new_task.category}, Priority: {new_task.priority}, Deadline: {deadline_str}')


        except ValueError as e:
            print('Error: Invalid input.')
            logging.error(f'ValueError in add_task: {e}')




    def delete_task(self):
        if len(self.tasks) == 0:
            print('Error: Task list is empty.')
            logging.warning('Attempted to delete task, but task list was empty.')
            return

        logging.debug(f"Task list loaded with {len(self.tasks)} tasks.")

        max_text_len = max(max([len(task["text"]) for task in self.tasks]), len("text"))
        max_category_len = max(max(len(task["category"]) for task in self.tasks), len("Category"))

        logging.debug(f"Calculated max_text_len={max_text_len}, max_category_len={max_category_len}")

        print('\n' + '=' * (max_text_len + max_category_len + 68))
        print('Task list'.center((max_text_len + max_category_len + 68)))
        print('=' * (max_text_len + max_category_len + 68))

        print(f'{"№":^3} | {"Text":^{max_text_len}} | {"Category":^{max_category_len}} | {"Priority":^10} | {"Date":^10} | {"Deadline":^10} | {"Status":^16}')
        print('-' * (max_text_len + max_category_len + 68))

        for index, task in enumerate(self.tasks):
            priority = task["priority"]
            color = Fore.RED if priority == "High" else Fore.YELLOW if priority == "Medium" else Fore.GREEN
            priority_colored = colored_aligned(priority, 10, color)
            deadline_colored = colorize_deadline(task["deadline"])
            status_colored = colorize_status(task["done"])
            print(
                f'{index + 1:^3} | {task["text"]:<{max_text_len}} | {task["category"]:^{max_category_len}} | {priority_colored:^10} | {task["date"]:<10} | {deadline_colored:<10} | {status_colored:^16}')


        input_index = input('\nEnter the task number to delete or exit: ').strip()
        logging.debug(f"User entered index: {input_index}")

        if input_index.lower() == 'exit':
            print('Returning to menu...')
            logging.info('User cancelled task deletion (exit).')
            return

        try:
            if 0 <= int(input_index) - 1 <= len(self.tasks):
                logging.debug(f"Selected task for deletion: {self.tasks[int(input_index) - 1]['text']}")
                input_choice = input(f'Are you sure to delete this task "{self.tasks[int(input_index) - 1]["text"]}" ? (y/n): ')
                logging.debug(f"User confirmation: {input_choice}")

                if input_choice.lower() == 'n' or input_choice.lower() == 'no':
                    print('Returning to menu...')
                    logging.info(f'Task deletion of "{self.tasks[int(input_index) - 1]['text']}" cancelled by user.')
                    return
                else:
                    self.tasks.pop(int(input_index) - 1)
                    print('The selected task has been deleted!')
                    self.save_data()
                    logging.info(f'Task "{self.tasks[int(input_index) - 1]['text']}" was successfully deleted.')

            else:
                print('Error: Invalid input.')
                logging.warning(f'User tried to delete invalid task index: {input_index}')

        except ValueError as e:
            print('Error: Invalid input.')
            logging.error(f'ValueError while parsing input index: {input_index}, Exception: {e}')




    def show_tasks(self):
        if len(self.tasks) == 0:
            print('Error: Task list is empty.')
            logging.warning("User attempted to view tasks, but task list is empty")
            return

        logging.info(f"Displaying {len(self.tasks)} tasks")

        max_text_len = max(max([len(task["text"]) for task in self.tasks]), len("text"))
        max_category_len = max(max(len(task["category"]) for task in self.tasks), len("Category"))

        print('\n' + '=' * (max_text_len + max_category_len + 68))
        print(style_tittle('Tasks list').center((max_text_len + max_category_len + 68)))
        print('=' * (max_text_len + max_category_len + 68))

        print(f'{"№":^3} | {"Text":^{max_text_len}} | {"Category":^{max_category_len}} | {"Priority":^10} | {"Date":^10} | {"Deadline":^10} | {"Status":^16}')
        print('-' * (max_text_len + max_category_len + 68))

        for index, task in enumerate(self.tasks):
            priority = task["priority"]
            color = Fore.RED if priority == "High" else Fore.YELLOW if priority == "Medium" else Fore.GREEN
            priority_colored = colored_aligned(priority, 10, color)
            deadline_colored = colorize_deadline(task["deadline"])
            status_colored = colorize_status(task["done"])
            print(f'{index + 1:^3} | {task["text"]:<{max_text_len}} | {task["category"]:^{max_category_len}} | {priority_colored:^10} | {task["date"]:<10} | {deadline_colored:<10} | {status_colored:^16}')




    def complete_task(self):
        if len(self.tasks) == 0:
            print('Error: Task list is empty.')
            logging.warning("Cannot complete task — list is empty")
            return

        uncompleted_tasks = [task for task in self.tasks if not task["done"]]

        if not uncompleted_tasks:
            print('Error: Uncompleted tasks list is empty.')
            logging.warning("No uncompleted tasks found")
            return

        logging.info(f"User is viewing {len(uncompleted_tasks)} uncompleted tasks")

        max_text_len = max(max([len(task["text"]) for task in self.tasks]), len("text"))
        max_category_len = max(max(len(task["category"]) for task in self.tasks), len("Category"))

        print('\n' + '=' * (max_text_len + max_category_len + 68))
        print(style_tittle('List of uncompleted tasks'.center((max_text_len + max_category_len + 68))))
        print('=' * (max_text_len + max_category_len + 68))

        print(f'{"№":^3} | {"Text":^{max_text_len}} | {"Category":^{max_category_len}} | {"Priority":^10} | {"Date":^10} | {"Deadline":^10} | {"Status":^16}')
        print('-' * (max_text_len + max_category_len + 68))

        for index, task in enumerate(self.tasks):
            if not task["done"]:
                priority = task["priority"]
                color = Fore.RED if priority == "High" else Fore.YELLOW if priority == "Medium" else Fore.GREEN
                priority_colored = colored_aligned(priority, 10, color)
                deadline_colored = colorize_deadline(task["deadline"])
                status_colored = colorize_status(task["done"])
                print(
                    f'{index + 1:^3} | {task["text"]:<{max_text_len}} | {task["category"]:^{max_category_len}} | {priority_colored:^10} | {task["date"]:<10} | {deadline_colored:<10} | {status_colored:^16}')

        input_index = input('\nEnter the task number to complete or exit: ').strip()
        if input_index.lower() == 'exit':
            print('Returning to menu...')
            logging.debug("User exited from task completion prompt")
            return

        try:
            if 0 <= int(input_index) - 1 <= len(self.tasks):
                input_choice = input(f'Are you sure to complete this task "{self.tasks[int(input_index) - 1]["text"]}" ? (y/n): ')
                if input_choice.lower() == 'n' or input_choice.lower() == 'no':
                    print('Returning to menu...')
                    logging.debug(f'User canceled completion of task: "{self.tasks[int(input_index) - 1]["text"]}"')
                    return
                else:
                    self.tasks[int(input_index) - 1]['done'] = True
                    print('The selected task has been completed!')
                    logging.info(f'Task marked as completed: "{self.tasks[int(input_index) - 1]["text"]}"')
                    self.save_data()


            else:
                print('Error: Invalid input.')
                logging.warning(f'Invalid task number entered: {input_index}')

        except ValueError:
            print('Error: Invalid input.')
            logging.error(f'ValueError during task completion — input was: "{input_index}"')




    def find_by_category(self):
        if len(self.tasks) == 0:
            print('Error: Task list is empty.')
            logging.warning("Cannot search by category — task list is empty")
            return

        input_category = input('\nEnter the task category to search for: ').strip()
        logging.info(f"User is searching for tasks in category: {input_category}")

        tasks_in_input_category = [task for task in self.tasks if task["category"].lower() == input_category.lower()]

        if not tasks_in_input_category:
            print('Error: No tasks in the given category.')
            logging.warning(f'No tasks found in category: {input_category}')
            return

        logging.info(f"Found {len(tasks_in_input_category)} task(s) in category '{input_category}'")

        max_text_len = max(max([len(task["text"]) for task in self.tasks]), len("text"))
        max_category_len = max(max(len(task["category"]) for task in self.tasks), len("Category"))

        print('\n' + '=' * (max_text_len + max_category_len + 68))
        print(style_tittle('List of tasks in the given category'.center((max_text_len + max_category_len + 68))))
        print('=' * (max_text_len + max_category_len + 68))

        print(f'{"№":^3} | {"Text":^{max_text_len}} | {"Category":^{max_category_len}} | {"Priority":^10} | {"Date":^10} | {"Deadline":^10} | {"Status":^16}')
        print('-' * (max_text_len + max_category_len + 68))

        for index, task in enumerate(self.tasks):
            if task["category"].lower() == input_category.lower():
                priority = task["priority"]
                color = Fore.RED if priority == "High" else Fore.YELLOW if priority == "Medium" else Fore.GREEN
                priority_colored = colored_aligned(priority, 10, color)
                deadline_colored = colorize_deadline(task["deadline"])
                status_colored = colorize_status(task["done"])
                print(f'{index + 1:^3} | {task["text"]:<{max_text_len}} | {task["category"]:^{max_category_len}} | {priority_colored:^10} | {task["date"]:<10} | {deadline_colored:<10} | {status_colored:^16}')




    def find_by_priority(self):
        if len(self.tasks) == 0:
            print('Error: Task list is empty.')
            logging.warning("Cannot search by priority — task list is empty")
            return

        try:
            print('Select a priority level')
            print('[1] Low\n[2] Medium\n[3] High')

            input_choice = int(input('> '))
            logging.debug(f"User selected priority option: {input_choice}")

            if input_choice in range(1, 4):
                if input_choice == 1:
                    input_priority = 'Low'
                elif input_choice == 2:
                    input_priority = 'Medium'
                else:
                    input_priority = 'High'

            else:
                print('Error: Input out of range.')
                logging.warning(f"Priority selection out of range: {input_choice}")
                return

            logging.info(f"User is searching tasks with priority: {input_priority}")

            tasks_with_input_priority = [task for task in self.tasks if task['priority'] == input_priority]

            if not tasks_with_input_priority:
                print('Error: No tasks in the given priority level.')
                logging.warning(f"No tasks found with priority: {input_priority}")
                return

            logging.info(f'Found {len(tasks_with_input_priority)} task(s) with priority "{input_priority}"')

            max_text_len = max(max([len(task["text"]) for task in self.tasks]), len("text"))
            max_category_len = max(max(len(task["category"]) for task in self.tasks), len("Category"))

            print('\n' + '=' * (max_text_len + max_category_len + 68))
            print(style_tittle('List of tasks in the given priority level'.center((max_text_len + max_category_len + 68))))
            print('=' * (max_text_len + max_category_len + 68))

            print(f'{"№":^3} | {"Text":^{max_text_len}} | {"Category":^{max_category_len}} | {"Priority":^10} | {"Date":^10} | {"Deadline":^10} | {"Status":^16}')
            print('-' * (max_text_len + max_category_len + 68))

            for index, task in enumerate(self.tasks):
                if task["priority"] == input_priority:
                    priority = task["priority"]
                    color = Fore.RED if priority == "High" else Fore.YELLOW if priority == "Medium" else Fore.GREEN
                    priority_colored = colored_aligned(priority, 10, color)
                    deadline_colored = colorize_deadline(task["deadline"])
                    status_colored = colorize_status(task["done"])
                    print(f'{index + 1:^3} | {task["text"]:<{max_text_len}} | {task["category"]:^{max_category_len}} | {priority_colored:^10} | {task["date"]:<10} | {deadline_colored:<10} | {status_colored:^16}')

        except ValueError as e:
            print('Error: Invalid input.')
            logging.error(f"ValueError during priority input: {e}")




    def find_overdue_tasks(self):
        if len(self.tasks) == 0:
            print('Error: Task list is empty.')
            logging.warning("Cannot search for overdue tasks — task list is empty")
            return

        overdue_tasks = []
        for task in self.tasks:
            try:
                deadline = datetime.strptime(task["deadline"], '%d-%m-%Y').date()
                if (deadline - datetime.today().date()).days < 0:
                    overdue_tasks.append(task)
            except (ValueError, TypeError) as e:
                print(f'Error: invalid deadline in task "{task['text']}"')
                logging.error(f'Invalid deadline format in task "{task['text']}": {e}')

        if not overdue_tasks:
            print('Error: No overdue tasks found.')
            logging.info("No overdue tasks found")
            return

        logging.info(f"Found {len(overdue_tasks)} overdue task(s)")

        max_text_len = max(max([len(task["text"]) for task in self.tasks]), len("text"))
        max_category_len = max(max(len(task["category"]) for task in self.tasks), len("Category"))

        print('\n' + '=' * (max_text_len + max_category_len + 68))
        print(style_tittle('List of overdue tasks'.center((max_text_len + max_category_len + 68))))
        print('=' * (max_text_len + max_category_len + 68))

        print(f'{"№":^3} | {"Text":^{max_text_len}} | {"Category":^{max_category_len}} | {"Priority":^10} | {"Date":^10} | {"Deadline":^10} | {"Status":^16}')
        print('-' * (max_text_len + max_category_len + 68))

        for index, task in enumerate(self.tasks):
            try:
                deadline = datetime.strptime(task["deadline"], '%d-%m-%Y').date()
                if (deadline - datetime.today().date()).days < 0:
                    priority = task["priority"]
                    color = Fore.RED if priority == "High" else Fore.YELLOW if priority == "Medium" else Fore.GREEN
                    priority_colored = colored_aligned(priority, 10, color)
                    deadline_colored = colorize_deadline(task["deadline"])
                    status_colored = colorize_status(task["done"])
                    print(f'{index + 1:^3} | {task["text"]:<{max_text_len}} | {task["category"]:^{max_category_len}} | {priority_colored:^10} | {task["date"]:<10} | {deadline_colored:<10} | {status_colored:^16}')

            except (ValueError, TypeError) as e:
                print(f'Error: invalid deadline in task "{task['text']}"')
                logging.error(f"Invalid deadline format in task '{task['text']}': {e}")