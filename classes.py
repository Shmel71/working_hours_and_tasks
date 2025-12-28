from connect_to_db import connect_to_db
"""Модуль с классами. Добавил EmployeeManager и TaskManager потому что тогда в классах получалась каша из кода.
Теперь есть Employee и Task которые хранят данные и EmployeeManager и TaskManager которые с ними работают.
Стало лучше но все равно получилась каша."""

class Employee:
    def __init__(self, name, position, salary, hours_worked=0):
        self.name = name.strip()
        self.position = position
        self.salary = float(salary)
        self.hours_worked = int(hours_worked)

    def add_hours(self, hours):
        self.hours_worked += int(hours)

    def calculate_pay(self):
        hourly_rate = self.salary / 160
        return round(hourly_rate * self.hours_worked, 2)

    def __str__(self):
        return f"{self.name} ({self.position}), зарплата: {self.salary}, отработано: {self.hours_worked} ч."



class EmployeeManager:
    @staticmethod
    def create_employee():
        name = input("Введите имя и фамилию: ")
        position = input("Введите должность: ")
        salary = float(input("Введите зарплату: "))
        return Employee(name, position, salary)

    @staticmethod
    def get_all_employees():
        employees = []
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name, position, salary, hours_worked FROM workers')
            rows = cursor.fetchall()
            for row in rows:
                emp = Employee(row[0], row[1], row[2], row[3])
                employees.append(emp)
            conn.close()
        return employees

    @staticmethod
    def print_all_employees():
        employees = EmployeeManager.get_all_employees()
        if employees:
            for i, emp in enumerate(employees, 1):
                pay = emp.calculate_pay()
                print(f"{i}. {emp} → к выплате: {pay} руб.")
        else:
            print("Нет данных о сотрудниках.")

    @staticmethod
    def add_employee_to_db(employee):
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO workers (name, position, salary, hours_worked) VALUES (?, ?, ?, ?)",
                (employee.name, employee.position, employee.salary, employee.hours_worked)
            )
            conn.commit()
            conn.close()
            return True
        return False

    @staticmethod
    def remove_employee_from_db(employee):
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM workers WHERE name = ? AND position = ?",
                (employee.name, employee.position)
            )
            conn.commit()
            conn.close()
            print(f"Сотрудник {employee.name} успешно удалён из базы.")
            return True
        return False

    @staticmethod
    def update_employee_in_db(employee):
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE workers SET hours_worked = ? WHERE name = ? AND position = ?",
                (employee.hours_worked, employee.name, employee.position)
            )
            conn.commit()
            conn.close()
            return True
        return False



class Task:
    def __init__(self, title, description, project, status="New", assigned_employee=None):
        self.title = title.strip()
        self.description = description
        self.project = project
        self.status = status
        self.assigned_employee = assigned_employee

    def mark_complete(self):
        if self.status == "Completed":
            print("Задача уже отмечена как завершённая.")
            return False
        self.status = "Completed"
        print(f"Задача '{self.title}' отмечена как завершённая.")
        return True

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "project": self.project,
            "status": self.status,
            "assigned_employee": self.assigned_employee
        }

    def __str__(self):
        executor = self.assigned_employee if self.assigned_employee else "Не назначен"
        return f"Задача: {self.title}\nПроект: {self.project}\nСтатус: {self.status}\nИсполнитель: {executor}\nОписание: {self.description}"



class TaskManager:
    @staticmethod
    def get_projects():
        projects = []
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT title FROM projects")
            rows = cursor.fetchall()
            projects = [row[0] for row in rows]
            conn.close()
        return projects

    @staticmethod
    def get_employees():
        employees = []
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM workers ORDER BY name")
            employees = cursor.fetchall()
            conn.close()
        return employees

    @staticmethod
    def select_employee():
        employees = TaskManager.get_employees()
        if not employees:
            print("Нет доступных сотрудников в базе данных.")
            return None

        print("\nДоступные сотрудники:")
        for i, (emp_id, emp_name) in enumerate(employees, 1):
            print(f"{i}. {emp_name} (ID: {emp_id})")

        while True:
            choice = input(f"\nВведите номер сотрудника (1-{len(employees)}): ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(employees):
                    return employees[idx][1]
                else:
                    print(f"Введите число от 1 до {len(employees)}.")
            else:
                print("Введите число.")

    @staticmethod
    def create_task():
        projects = TaskManager.get_projects()
        if not projects:
            print("Нет доступных проектов в базе данных.")
            return None

        print("\nДоступные проекты:")
        for i, project_name in enumerate(projects, 1):
            print(f"{i}. {project_name}")

        while True:
            choice = input(f"\nВведите номер проекта (1-{len(projects)}): ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(projects):
                    project = projects[idx]
                    break
                else:
                    print(f"Введите число от 1 до {len(projects)}.")
            else:
                print("Введите число.")

        title = input("\nВведите название задачи: ").strip()
        description = input("Введите описание задачи: ").strip()

        print("\nВыберите статус:")
        statuses = ["In Progress", "Completed"]
        for i, status in enumerate(statuses, 1):
            print(f"{i}. {status}")
        status_choice = input(f"Номер статуса (1-{len(statuses)}, по умолчанию 1): ").strip()
        status = statuses[0]
        if status_choice.isdigit() and 1 <= int(status_choice) <= len(statuses):
            status = statuses[int(status_choice) - 1]

        assigned_employee = TaskManager.select_employee()

        return Task(title, description, project, status, assigned_employee)

    @staticmethod
    def save_task_to_db(task):
        conn = connect_to_db()
        if not conn:
            print("Ошибка соединения с БД.")
            return False

        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO tasks (title, description, project, status, assigned_employee)
            VALUES (?, ?, ?, ?, ?)""",
            (task.title, task.description, task.project, task.status, task.assigned_employee)
        )
        conn.commit()
        conn.close()
        print("Задача успешно добавлена в БД!")
        return True

    @staticmethod
    def update_task_in_db(task):
        conn = connect_to_db()
        if not conn:
            return False

        cursor = conn.cursor()
        cursor.execute(
            """UPDATE tasks
            SET status = ?
            WHERE title = ? AND project = ?""",
            (task.status, task.title, task.project)
        )
        if cursor.rowcount == 0:
            print("Ошибка: задача не найдена в БД.")
            return False
        conn.commit()
        conn.close()
        return True



class Project:
    def __init__(self, title):
        self.title = title
        self._tasks = []

    def add_task(self, task):
        if task.project != self.title:
            print(f"Ошибка: задача относится к проекту '{task.project}', а не к '{self.title}'")
            return
        self._tasks.append(task)

    def project_progress(self):
        if not self._tasks:
            return 0.0
        completed = sum(1 for task in self._tasks if task.status == "Completed")
        return round((completed / len(self._tasks)) * 100, 1)

    def get_tasks(self):
        return self._tasks

    def task_count(self):
        return len(self._tasks)

    @staticmethod
    def get_projects():
        projects = []
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM projects ORDER BY name")
            rows = cursor.fetchall()
            projects = [row[0] for row in rows]
            conn.close()
        return projects

    @classmethod
    def from_db(cls, project_name):
        project = cls(project_name)
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT title, description, project, status, assigned_employee FROM tasks WHERE project = ?",
                (project_name,)
            )
            rows = cursor.fetchall()
            for row in rows:
                task = Task(row[0], row[1], row[2], row[3], row[4])
                project.add_task(task)
            conn.close()
        return project

    def __str__(self):
        return f"Проект: {self.title} (Задачи: {self.task_count()}, Прогресс: {self.project_progress()}%)"

