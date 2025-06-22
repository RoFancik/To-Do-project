from datetime import datetime


class Task:
    def __init__(self, text, category, priority, deadline):
        self.text = text
        self.category = category
        self.priority = priority
        self.done = False
        self.date = datetime.today().date().strftime('%d-%m-%Y')
        self.deadline = deadline.strftime('%d-%m-%Y')


    def to_dict(self):
        return {
            'text': self.text,
            'category': self.category,
            'priority': self.priority,
            'date': self.date,
            'done': self.done,
            'deadline': self.deadline
        }