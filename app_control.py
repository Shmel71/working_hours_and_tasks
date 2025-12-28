from connect_to_db import *
from classes import EmployeeManager, Task, TaskManager, Project
"""Тут куча всего. По сути, набор функций от главного меню до расчета зп и добавления новых проектов. 
Изначально, пытался уйти от простыни кода, разбив проект на модули.
В результате с простыней и остался....даже не с одной("""

def menu():
    """Главное меню приложения."""
    menu_items = {
        1: "Показать сотрудников",
        2: "Добавить сотрудника",
        3: "Удалить сотрудника",
        4: "Проекты",
        6: "Добавить отработанные часы",
        7: "Рассчитать зарплату сотрудника",
        0: "Выход"
    }

    print("\n" + "=" * 40)
    print("УПРАВЛЕНИЕ СОТРУДНИКАМИ И ПРОЕКТАМИ")
    print("=" * 40)

    for k, v in menu_items.items():
        print(f"{k}. {v}")

    try:
        choice = int(input("\nВведите номер пункта: "))
        if choice in menu_items:
            print(f"Вы выбрали: {menu_items[choice]}")
            return choice
        else:
            print("Ошибка! Нет такого пункта меню.")
            return None
    except ValueError:
        print("Ошибка! Введите число от 0 до 7.")
        return None


def projects_menu():
    print("\n--- УПРАВЛЕНИЕ ПРОЕКТАМИ ---")
    print("1. Список проектов")
    print("2. Детали проекта")
    print("3. Добавить проект")
    print("0. Вернуться в главное меню")

    try:
        choice = int(input("\nВведите номер пункта: "))
        return choice
    except ValueError:
        print("Ошибка! Введите число 0–3.")
        return None


def display_projects():
    projects = TaskManager.get_projects()
    if not projects:
        print("\nНет доступных проектов в базе данных.")
        return

    print("\n--- СПИСОК ПРОЕКТОВ ---")
    for i, proj_name in enumerate(projects, 1):
        project = Project.from_db(proj_name)
        if project:
            print(f"{i}. {project}")


def show_project_details():
    projects = TaskManager.get_projects()
    if not projects:
        print("\nНет проектов в базе данных.")
        return

    print("\nДоступные проекты:")
    for i, name in enumerate(projects, 1):
        print(f"{i}. {name}")

    choice = input(f"\nВведите номер проекта (1–{len(projects)}) или 0 для возврата: ").strip()
    if choice == "0":
        return
    elif choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(projects):
            proj_name = projects[idx]
            project = Project.from_db(proj_name)
            if project:
                print(f"\n--- ДЕТАЛИ ПРОЕКТА: {proj_name} ---")
                print(project)

                tasks = project.get_tasks()
                if tasks:
                    print("\nЗадачи проекта:")
                    for i, task in enumerate(tasks, 1):
                        print(f"{i}. {task.title} [{task.status}]")
                        if task.assigned_employee:
                            print(f"  Исполнитель: {task.assigned_employee}")
                else:
                    print("В проекте нет задач.")

                print("\n[5] Добавить задачу в этот проект")
                print("[6] Отметить задачу как завершённую")
                print("[0] Вернуться к списку проектов")

                action = input("\nВыберите действие (0–6): ").strip()

                if action == "5":
                    create_task_in_project(proj_name)
                elif action == "6":
                    if not tasks:
                        print("В проекте нет задач для отметки.")
                    else:
                        task_num = input(f"Номер задачи (1–{len(tasks)}): ").strip()
                        if task_num.isdigit():
                            num = int(task_num)
                            if 1 <= num <= len(tasks):
                                selected_task = tasks[num - 1]
                                if selected_task.mark_complete():
                                    if TaskManager.update_task_in_db(selected_task):
                                        print("Статус задачи успешно обновлён в БД.")
                                    else:
                                        print("Не удалось обновить статус в БД.")
                            else:
                                print("Неверный номер задачи.")
                        else:
                            print("Введите число.")
                elif action != "0":
                    print("Неверный выбор.")
        else:
            print(f"Введите число от 1 до {len(projects)}.")
    else:
        print("Введите корректный номер.")


def create_task_in_project(project_name):
    print(f"\n--- ДОБАВЛЕНИЕ ЗАДАЧИ В ПРОЕКТ '{project_name}' ---")

    title = input("Название задачи: ").strip()
    if not title:
        print("Название задачи не может быть пустым!")
        return

    description = input("Описание задачи: ").strip()

    statuses = ["In Progress", "Completed"]
    print("\nВыберите статус:")
    for i, s in enumerate(statuses, 1):
        print(f"{i}. {s}")
    choice = input(f"Номер статуса (по умолчанию 2 → 'In Progress'): ").strip()
    status = "In Progress"
    if choice.isdigit() and 1 <= int(choice) <= len(statuses):
        status = statuses[int(choice) - 1]

    employees = TaskManager.get_employees()
    if not employees:
        print("Нет доступных сотрудников в БД!")
        return
    print("\nДоступные сотрудники:")
    for i, (eid, name) in enumerate(employees, 1):
        print(f"{i}. {name} (ID: {eid})")
    emp_choice = input(f"Номер сотрудника (1–{len(employees)}): ").strip()
    if emp_choice.isdigit() and 1 <= int(emp_choice) <= len(employees):
        assigned_employee = employees[int(emp_choice) - 1][1]
    else:
        print("Неверный номер сотрудника!")
        return

    task = Task(title, description, project_name, status, assigned_employee)

    if TaskManager.save_task_to_db(task):
        print(f"\nЗадача '{title}' успешно добавлена в проект '{project_name}'!")
        print(f"Исполнитель: {assigned_employee}")
        print(f"Статус: {status}")
    else:
        print("Не удалось сохранить задачу в БД.")


def add_project():
    project_name = input("\nВведите название проекта: ").strip()
    if not project_name:
        print("Название проекта не может быть пустым.")
        return

    conn = connect_to_db()
    if not conn:
        print("Ошибка соединения с БД.")
        return

    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM projects WHERE title = ?", (project_name,))
    if cursor.fetchone():
        print(f"Проект '{project_name}' уже существует.")
        conn.close()
        return

    cursor.execute("INSERT INTO projects (title) VALUES (?)", (project_name,))
    conn.commit()
    conn.close()
    print(f"Проект '{project_name}' успешно добавлен!")


def add_hours_to_employee():
    employees = EmployeeManager.get_all_employees()
    if not employees:
        print("\nНет сотрудников в базе данных.")
        return

    print("\nСписок сотрудников:")
    for i, emp in enumerate(employees, 1):
        print(f"{i}. {emp.name} ({emp.position})")

    choice = input(f"\nВведите номер сотрудника (1–{len(employees)}) или 0 для возврата: ").strip()

    if choice == "0":
        return
    elif choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(employees):
            employee = employees[idx]
            print(f"\nСотрудник: {employee.name}")
            print(f"Отработано: {employee.hours_worked} ч.")

            hours_input = input("Сколько часов добавить? ").strip()
            if not hours_input:
                print("Ввод не может быть пустым.")
                return

            try:
                hours = float(hours_input)
                employee.add_hours(hours)
                if EmployeeManager.update_employee_in_db(employee):
                    print(f"Успешно добавлено {hours} ч. Теперь отработано: {employee.hours_worked} ч.")
                else:
                    print("Не удалось обновить данные в БД.")
            except ValueError:
                print("Ошибка: введите корректное число часов.")
            except Exception:
                print("Неизвестная ошибка при обновлении данных.")
        else:
            print(f"Введите число от 1 до {len(employees)}.")
    else:
        print("Введите число.")


def calculate_employee_pay():
    employees = EmployeeManager.get_all_employees()
    if not employees:
        print("\nНет сотрудников в базе данных.")
        return

    print("\nСписок сотрудников:")
    for i, emp in enumerate(employees, 1):
        print(f"{i}. {emp.name} ({emp.position}), зарплата: {emp.salary} руб.")

    choice = input(f"\nВведите номер сотрудника (1–{len(employees)}) или 0 для возврата: ").strip()

    if choice == "0":
        return
    elif choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(employees):
            employee = employees[idx]
            pay = employee.calculate_pay()
            print(f"\nРасчёт зарплаты для {employee.name}:")
            print(f"- Месячная ставка: {employee.salary} руб.")
            print(f"- Отработано часов: {employee.hours_worked} ч.")
            print(f"- Часовая ставка: {round(employee.salary / 160, 2)} руб./ч.")
            print(f"- Итого к выплате: {pay} руб.")
        else:
            print(f"Введите число от 1 до {len(employees)}.")
    else:
        print("Введите число.")


def start_app():
    print("Добро пожаловать в систему управления сотрудниками и проектами!")

    while True:
        choice = menu()

        if choice is None:
            continue

        if choice == 0:
            print("До свидания!")
            break

        elif choice == 1:
            EmployeeManager.print_all_employees()

        elif choice == 2:
            emp = EmployeeManager.create_employee()
            if emp and EmployeeManager.add_employee_to_db(emp):
                print("Сотрудник успешно добавлен в базу данных!")

        elif choice == 3:
            employees = EmployeeManager.get_all_employees()
            if not employees:
                print("Нет сотрудников для удаления.")
                continue

            print("\nСписок сотрудников:")
            for i, emp in enumerate(employees, 1):
                pay = emp.calculate_pay()
                print(f"{i}. {emp} → к выплате: {pay} руб.")

            num_input = input(f"\nВведите номер сотрудника для удаления (1–{len(employees)}): ").strip()
            if num_input.isdigit():
                num = int(num_input)
                if 1 <= num <= len(employees):
                    if EmployeeManager.remove_employee_from_db(employees[num - 1]):
                        print("Сотрудник успешно удалён!")
                    else:
                        print("Ошибка при удалении сотрудника.")
                else:
                    print(f"Введите число от 1 до {len(employees)}.")
            else:
                print("Введите корректное число.")

        elif choice == 4:
            while True:
                proj_choice = projects_menu()
                if proj_choice is None:
                    continue
                elif proj_choice == 0:
                    break
                elif proj_choice == 1:
                    display_projects()
                elif proj_choice == 2:
                    show_project_details()
                elif proj_choice == 3:
                    add_project()
                else:
                    print("Ошибка! Нет такого пункта меню.")

        elif choice == 6:
            add_hours_to_employee()

        elif choice == 7:
            calculate_employee_pay()

        else:
            print("Ошибка! Нет такого пункта меню.")
