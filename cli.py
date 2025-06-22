from utils import *
import logging


logging.basicConfig(
    filename='todo.log',
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)


my_tasks = TaskManager()

def menu():
    logging.debug('Program is started. Awaiting user input in menu...')
    while True:
        try:
            logging.debug('Main menu displayed')

            print('\nMenu:'
                  '\n[1] View Task list'
                  '\n[2] Add new task'
                  '\n[3] Delete task'
                  '\n[4] Complete task'
                  '\n[5] Find task by category'
                  '\n[6] Find task by priority level'
                  '\n[7] Find overdue tasks'
                  '\n[8] Exit')


            input_choice = int(input('> '))
            if input_choice in range(1, 9):
                if input_choice == 1:
                    logging.debug('User choice [1] View Task list')
                    my_tasks.load_data()
                    my_tasks.show_tasks()

                elif input_choice == 2:
                    logging.debug('User choice [2] Add new task')
                    my_tasks.load_data()
                    my_tasks.add_task()

                elif input_choice == 3:
                    logging.debug('User choice [3] Delete task')
                    my_tasks.load_data()
                    my_tasks.delete_task()

                elif input_choice == 4:
                    logging.debug('User choice [4] Complete task')
                    my_tasks.load_data()
                    my_tasks.complete_task()

                elif input_choice == 5:
                    logging.debug('User choice [5] Find task by category')
                    my_tasks.load_data()
                    my_tasks.find_by_category()

                elif input_choice == 6:
                    logging.debug('User choice [6] Find task by priority level')
                    my_tasks.load_data()
                    my_tasks.find_by_priority()

                elif input_choice == 7:
                    logging.debug('User choice [7] Find overdue tasks')
                    my_tasks.load_data()
                    my_tasks.find_overdue_tasks()

                else:
                    logging.debug('User choice [8] Exit')
                    input_exit_choice = input('Are you sure you want to exit? (y/n): ').lower()
                    if input_exit_choice == 'n' or input_exit_choice == 'no':
                        print('Returning to menu...')
                        logging.debug('User cancelled exit request')
                        continue

                    elif input_exit_choice == 'y' or input_exit_choice == 'yes':
                        print('Goodbye!')
                        logging.info('Program is finished')
                        break

                    else:
                        print('Error: Invalid input.')
                        print('Exiting...')
                        logging.debug('User cancelled exit request')


            else:
                print('Error: Input out of range.')
                logging.warning('User input out of range.')

        except ValueError as e:
            print('Error: Invalid input, expected int')
            logging.error(f'Error: {e}')

        except Exception as e:
            print(f'Error: {e}')
            logging.error(f'Error: {e}')

        except KeyboardInterrupt:
            print('\nGoodbye!')
            logging.info('Program is finished forcibly')
            break
