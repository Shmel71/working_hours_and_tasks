from classes import *
from app_menu import render_menu
from logger import create_logger

logger = create_logger()


def start_app():
    logger.info("Старт приложения")
    print("Добро пожаловать в систему управления сотрудниками и проектами!")

    while True:
        render_menu("main")
        try:
            choice = input("\nВыберите пункт (0–2): ").strip()

            if not Validator.validate_menu_choice(choice, 0, 2):
                logger.warning(f"Некорректный ввод в главном меню: '{choice}'")
                print("Ошибка: введите число от 0 до 2.")
                continue

            if choice == "0":
                print("До свидания!")
                return True

            elif choice == "1":
                while True:
                    render_menu("workers")
                    emp_choice = input("\nВыберите пункт (0–5): ").strip()

                    if not Validator.validate_menu_choice(emp_choice, 0, 5):
                        logger.warning(f"Некорректный выбор в меню сотрудников: '{emp_choice}'")
                        print("Ошибка: нет такого пункта меню.")
                        continue

                    if emp_choice == "0":
                        logger.debug("Выход из меню сотрудников.")
                        break

                    elif emp_choice == "1":
                        logger.info("Просмотр списка сотрудников")
                        EmployeeManager.print_all_employees()

                    elif emp_choice == "2":
                        logger.info("Добавление сотрудника")
                        emp = EmployeeManager.create_employee()
                        if emp and EmployeeManager.add_employee_to_db(emp):
                            print("Сотрудник успешно добавлен в базу данных!")
                        else:
                            print("Ошибка при добавлении сотрудника.")

                    elif emp_choice == "3":
                        logger.info("Удаление сотрудника")
                        employees = EmployeeManager.get_all_employees()
                        if not employees:
                            print("Нет сотрудников для удаления.")
                            continue

                        print("\nСписок сотрудников:")
                        for i, emp in enumerate(employees, 1):
                            pay = emp.calculate_pay()
                            print(f"{i}. {emp} → к выплате: {pay} руб.")

                        num_input = input(f"\nВведите номер сотрудника (1–{len(employees)}): ").strip()

                        idx = Validator.validate_employee_index(num_input, len(employees))
                        if idx is None:
                            logger.warning(f"Некорректный номер сотрудника: '{num_input}'")
                            print(f"Введите число от 1 до {len(employees)}.")
                            continue

                        if EmployeeManager.remove_employee_from_db(employees[idx]):
                            print("Сотрудник успешно удалён!")
                        else:
                            print("Ошибка при удалении сотрудника.")

                    elif emp_choice == "4":
                        add_hours_to_employee()

                    elif emp_choice == "5":
                        calculate_employee_pay()

            elif choice == "2":
                while True:
                    render_menu("projects")
                    proj_choice = input("\nВыберите пункт (0–3): ").strip()

                    if not Validator.validate_menu_choice(proj_choice, 0, 3):
                        logger.warning(f"Некорректный выбор в меню проектов: '{proj_choice}'")
                        print("Ошибка: нет такого пункта меню.")
                        continue

                    if proj_choice == "0":
                        logger.debug("Выход из меню проектов.")
                        break

                    elif proj_choice == "1":
                        display_projects()

                    elif proj_choice == "2":
                        show_project_details()

                    elif proj_choice == "3":
                        add_project()

        except KeyboardInterrupt:
            print("\nОстановлено пользователем.")
            return False
        except Exception as e:
            logger.exception(e)
            print(f"Ошибка: {e}")


def display_projects():
    projects = TaskManager.get_projects()
    if not projects:
        logger.info("Нет доступных проектов в базе данных.")
        print("\nНет доступных проектов в базе данных.")
        return

    logger.info(f"Найдено {len(projects)} проектов для отображения.")
    print("\n--- СПИСОК ПРОЕКТОВ ---")
    for i, proj_name in enumerate(projects, 1):
        project = Project.from_db(proj_name)
        if project:
            print(f"{i}. {project}")
            logger.debug(f"Выведен проект: {proj_name}")
        else:
            logger.warning(f"Не удалось загрузить проект из БД: {proj_name}")


def show_project_details():
    logger = create_logger()
    projects = TaskManager.get_projects()

    if not projects:
        logger.info("Нет проектов в базе данных.")
        print("\nНет проектов в базе данных.")
        return

    logger.info(f"Доступно {len(projects)} проектов для выбора.")
    print("\nДоступные проекты:")
    for i, name in enumerate(projects, 1):
        print(f"{i}. {name}")

    choice = input(f"\nВведите номер проекта (1–{len(projects)}) или 0 для возврата: ").strip()

    if choice == "0":
        logger.debug("Пользователь выбрал возврат в меню проектов.")
        return

    proj_idx = Validator.validate_project_index(choice, len(projects))
    if proj_idx is None:
        logger.warning(f"Некорректный номер проекта: '{choice}'")
        print(f"Введите число от 1 до {len(projects)}.")
        return

    proj_name = projects[proj_idx]
    project = Project.from_db(proj_name)

    if not project:
        logger.error(f"Не удалось загрузить проект из БД: {proj_name}")
        print(f"Ошибка: не удалось загрузить проект '{proj_name}'.")
        return

    logger.info(f"Отображение деталей проекта: {proj_name}")
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

    if not Validator.validate_menu_choice(action, 0, 6):
        logger.warning(f"Некорректный выбор действия: '{action}'")
        print("Неверный выбор. Введите число от 0 до 6.")
        return

    if action == "5":
        logger.info("Пользователь выбрал добавление задачи в проект.")
        create_task_in_project(proj_name)

    elif action == "6":
        if not tasks:
            logger.info("Попытка отметить задачу, но задач нет.")
            print("В проекте нет задач для отметки.")
            return

        task_num = input(f"Номер задачи (1–{len(tasks)}): ").strip()
        task_idx = Validator.validate_task_index(task_num, len(tasks))
        if task_idx is None:
            logger.warning(f"Некорректный номер задачи: '{task_num}'")
            print(f"Введите число от 1 до {len(tasks)}.")
            return

        selected_task = tasks[task_idx]
        if selected_task.mark_complete():
            if TaskManager.update_task_in_db(selected_task):
                logger.info(f"Статус задачи '{selected_task.title}' обновлён в БД.")
                print("Статус задачи успешно обновлён в БД.")
            else:
                logger.error("Не удалось обновить статус задачи в БД.")
                print("Не удалось обновить статус в БД.")
        else:
            logger.warning("Не удалось отметить задачу как завершённую.")
            print("Ошибка при обновлении статуса задачи.")

    elif action == "0":
        logger.debug("Пользователь вернулся к списку проектов.")
        return


def create_task_in_project(project_name):
    logger = create_logger()
    print(f"\n--- ДОБАВЛЕНИЕ ЗАДАЧИ В ПРОЕКТ '{project_name}' ---")

    title = input("Название задачи: ").strip()
    if not Validator.validate_non_empty_string(title, "название задачи"):
        logger.warning("Пустое название задачи.")
        print("Название задачи не может быть пустым!")
        return

    description = input("Описание задачи: ").strip()

    statuses = ["In Progress", "Completed"]
    print("\nВыберите статус:")
    for i, s in enumerate(statuses, 1):
        print(f"{i}. {s}")

    choice = input(f"Номер статуса (по умолчанию 1 → 'In Progress'): ").strip()
    status = "In Progress"

    if choice:
        status_idx = Validator.validate_status_choice(choice, statuses)
        if status_idx is not None:
            status = status_idx
        else:
            logger.warning(f"Некорректный номер статуса: '{choice}'")
            print("Используется статус по умолчанию: 'In Progress'.")

    employees = TaskManager.get_employees()
    if not employees:
        logger.warning("Нет доступных сотрудников в БД.")
        print("Нет доступных сотрудников в БД!")
        return

    print("\nДоступные сотрудники:")
    for i, (eid, name) in enumerate(employees, 1):
        print(f"{i}. {name} (ID: {eid})")

    emp_choice = input(f"Номер сотрудника (1–{len(employees)}): ").strip()
    assigned_employee = Validator.validate_employee_choice(emp_choice, employees)

    if assigned_employee is None:
        logger.warning(f"Некорректный номер сотрудника: '{emp_choice}'")
        print("Неверный номер сотрудника!")
        return

    task = Task(title, description, project_name, status, assigned_employee)

    if TaskManager.save_task_to_db(task):
        logger.info(f"Задача '{title}' успешно добавлена в проект '{project_name}'.")
        print(f"\nЗадача '{title}' успешно добавлена в проект '{project_name}'!")
        print(f"Исполнитель: {assigned_employee}")
        print(f"Статус: {status}")
    else:
        logger.error("Не удалось сохранить задачу в БД.")
        print("Не удалось сохранить задачу в БД.")


def add_project():
    logger = create_logger()
    project_name = input("\nВведите название проекта: ").strip()

    if not Validator.validate_non_empty_string(project_name, "название проекта"):
        logger.warning("Пустое название проекта.")
        print("Название проекта не может быть пустым.")
        return

    conn = connect_to_db()
    if not conn:
        logger.error("Ошибка соединения с БД при добавлении проекта.")
        print("Ошибка соединения с БД.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM projects WHERE title = ?", (project_name,))
        if cursor.fetchone():
            logger.info(f"Проект '{project_name}' уже существует в БД.")
            print(f"Проект '{project_name}' уже существует.")
            conn.close()
            return

        cursor.execute("INSERT INTO projects (title) VALUES (?)", (project_name,))
        conn.commit()
        logger.info(f"Проект {project_name} успешно добавлен в БД.")
        print(f"Проект '{project_name}' успешно добавлен!")

    except Exception as e:
        logger.exception(f"Ошибка при добавлении проекта '{project_name}': {e}")
        print("Произошла ошибка при сохранении проекта в БД.")
    finally:
        conn.close()


def add_hours_to_employee():
    logger = create_logger()
    employees = EmployeeManager.get_all_employees()

    if not employees:
        logger.info("Нет сотрудников в базе данных.")
        print("\nНет сотрудников в базе данных.")
        return

    print("\nСписок сотрудников:")
    for i, emp in enumerate(employees, 1):
        print(f"{i}. {emp.name} ({emp.position})")

    choice = input(f"\nВведите номер сотрудника (1–{len(employees)}) или 0 для возврата: ").strip()

    if choice == "0":
        logger.debug("Пользователь вернулся из меню добавления часов.")
        return

    emp_idx = Validator.validate_employee_index(choice, len(employees))
    if emp_idx is None:
        logger.warning(f"Некорректный номер сотрудника: '{choice}'")
        print(f"Введите число от 1 до {len(employees)}.")
        return

    employee = employees[emp_idx]
    print(f"\nСотрудник: {employee.name}")
    print(f"Отработано: {employee.hours_worked} ч.")

    hours_input = input("Сколько часов добавить? ").strip()

    if not Validator.validate_non_empty_string(hours_input, "количество часов"):
        logger.warning("Пустой ввод количества часов.")
        print("Ввод не может быть пустым.")
        return

    try:
        hours = float(hours_input)
        if hours < 0:
            logger.warning(f"Отрицательное количество часов: {hours}")
            print("Количество часов не может быть отрицательным.")
            return

        employee.add_hours(hours)
        if EmployeeManager.update_employee_in_db(employee):
            logger.info(f"Добавлено {hours}ч.для сотрудника {employee.name}.Итого: {employee.hours_worked} ч.")
            print(f"Успешно добавлено {hours} ч. Теперь отработано: {employee.hours_worked} ч.")
        else:
            logger.error(f"Не удалось обновить данные сотрудника {employee.name} в БД.")
            print("Не удалось обновить данные в БД.")

    except ValueError:
        logger.warning(f"Некорректный формат часов: '{hours_input}'")
        print("Ошибка: введите корректное число часов.")
    except Exception as e:
        logger.exception(f"Неожиданная ошибка при добавлении часов для {employee.name}: {e}")
        print("Произошла непредвиденная ошибка.")


def calculate_employee_pay():
    logger = create_logger()
    employees = EmployeeManager.get_all_employees()

    if not employees:
        logger.info("Нет сотрудников в базе данных.")
        print("\nНет сотрудников в базе данных.")
        return

    print("\nСписок сотрудников:")
    for i, emp in enumerate(employees, 1):
        print(f"{i}. {emp.name} ({emp.position}), зарплата: {emp.salary} руб.")

    choice = input(f"\nВведите номер сотрудника (1–{len(employees)}) или 0 для возврата: ").strip()

    if choice == "0":
        logger.debug("Пользователь вернулся из меню расчёта зарплаты.")
        return

    emp_idx = Validator.validate_employee_index(choice, len(employees))
    if emp_idx is None:
        logger.warning(f"Некорректный номер сотрудника: '{choice}'")
        print(f"Введите число от 1 до {len(employees)}.")
        return

    employee = employees[emp_idx]
    pay = employee.calculate_pay()

    logger.info(f"Расчёт зарплаты для сотрудника {employee.name}: {pay} руб.")
    print(f"\nРасчёт зарплаты для {employee.name}:")
    print(f"- Месячная ставка: {employee.salary} руб.")
    print(f"- Отработано часов: {employee.hours_worked} ч.")
    print(f"- Часовая ставка: {round(employee.salary / 160, 2)} руб./ч.")
    print(f"- Итого к выплате: {pay} руб.")
