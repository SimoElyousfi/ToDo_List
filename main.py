import sqlite3
import sys


class My_EXECPTION(Exception):
    pass


class TODO:
    def __init__(self):
        # Connection
        try:
            self.conn = sqlite3.connect("TODO_DB.db")
            self.c = self.conn.cursor()
            self.create_tasks_table()

        except sqlite3.Error as s:
            print(s)

    def create_tasks_table(self):
        try:
            self.c.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            priority INTEGER NOT NULL
            );
            """)
        except sqlite3.Error as ce:
            print(ce)

    def set_task(self):
        name = input("Enter task name: ")
        priority = input("Enter priority:")

        #  check task name
        if name == "":
            raise My_EXECPTION("Task name can't be empty!")

        # Check priority
        try:
            priority = int(priority)
        except My_EXECPTION as we:
            print(we)
        else:
            if priority < 1:
                raise My_EXECPTION("The priority task accept greater than or equal to 1")

        # Check if Task exists
        if self.find_task(name):
            raise My_EXECPTION("Task already exists")

        try:
            self.c.execute(f"""
            INSERT INTO tasks(name, priority) VALUES('{name}', {priority});
            """)
            self.conn.commit()
            # self.conn.close()

        except sqlite3.Error as xe:
            print(xe)

    def find_task(self, name):
        return self.c.execute(f"SELECT * FROM tasks WHERE name ='{name}'").fetchone()

    def change_priority(self):
        id = input("Enter id: ")
        priority = input("Enter priority: ")

        # Check priority
        try:
            id = int(id)
            priority = int(priority)
        except My_EXECPTION as ew:
            print(ew)
        else:
            if priority < 1:
                raise My_EXECPTION("The priority task accept greater than or equal to 1")

        self.c.execute(f"UPDATE tasks SET priority={priority} WHERE id={id}")
        self.conn.commit()
        # self.conn.close()

    def delete_task(self):
        try:
            id = int(input("Enter id: "))
            self.c.execute(f"DELETE FROM tasks WHERE id={id}")
            self.conn.commit()
            # self.conn.close()
        except My_EXECPTION as m:
            print(m)

    def show_tasks(self):
        for row in self.c.execute("SELECT * FROM tasks"):
            print(row)


if __name__ == "__main__":
    app = TODO()
    # app.create_tasks_table()
    while True:
        print("""
        1. Show Tasks
        2. Add Task
        3. Change Priority
        4. Delete Task
        5. Exit
        """)

        try:
            action = int(input("Enter your Action by using a number from menu: "))
            match action:
                case 1:
                    app.show_tasks()
                case 2:
                    app.set_task()
                case 3:
                    app.change_priority()
                case 4:
                    app.delete_task()
                case 5:
                    sys.exit()
        except Exception as e:
            print(e)
