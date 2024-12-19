import csv
import pickle

def load_table_csv(filename, detect_types=False):
    """
    This is an example of Google style.
    Args:
     filename: specifies the path to the csv file.
     detect_types: the function tries to determine the data types in each column.
    Returns:
        The function returns a dictionary `table` containing data from a CSV file.
    """
    #открывает файл как для чтения
    with open(filename, newline='') as f:
        #используется, чтобы csv файл открылся
        reader = csv.reader(f)
        #первая строка - заголовок файла
        headers = next(reader)
        rows = []
        for row in reader:
            #лишние пробелы, пустая строка и т.д.
            new_row = [item.strip() if item.strip() != '' else None for item in row]
            #добавляение в список row
            rows.append(new_row)
            #словарь, заголовки и данные
    table = {"headers": headers, "rows": rows}
    
    if detect_types:
        #вызывает фцекцию
        types = detect_column_types(table)
        #выводят на экран типы данных функцией
        print("Обнаруженные типы столбцов:")
        for col, col_type in types.items():
            print(f"{col}: {col_type}")
    #возвращаем словарь
    return table

def save_table_csv(table, filename):
    """
    This is an example of Google style.
    Args:
     table: a dictionary containing table data
     filename: a string indicating the name of the file to which the data will be saved.

    """
    #гарантия на закрытие, чтение
    with open(filename, 'w', newline='') as f:
        #создаем объект для записи данных csv
        writer = csv.writer(f)
        #запись заголовок на первую строку
        writer.writerow(table["headers"])
        #проверка на ошибки
        writer.writerows(
            [[item if item is not None else '' for item in row] for row in table["rows"]]
        )

def load_table_pickle(filename):
    """
    This is an example of Google style.
    Args:
     filename: a string containing the path to the pickle file
    """
    #гарантие на закрытие, чтение файла
    with open(filename, 'rb') as f:
        #расширение pickle
        table = pickle.load(f)
    #возвращаем значение
    return table

def save_table_pickle(table, filename):
    """
        This is an example of Google style.
        Args:
         table: a dictionary containing table data
         filename: a string indicating the name of the file to which the data will be saved.

        """
    # гарантия на закрытие, чтение
    with open(filename, 'wb') as f:
        # создаем объект для записи данных pickle
        pickle.dump(table, f)

def is_int(value):
    """
    This is an example of Google style.
    Args:
     value: an argument that can be of any type.
    Returns:
     when the number did not become an integer
    """
    try:
        #пытаемся из числа сделать целое
        int(value)
        #если работает True
        return True
    #проверка на ошибки
    except (ValueError, TypeError):
        #есть ошибка выводится False
        return False

def is_float(value):
    """
        This is an example of Google style.
        Args:
         value: an argument that can be of any type.
        Returns:
         when the number did not become an float
        """
    #пытаемся превратить в число с плавающей точкой
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False
#проверка является булевым знач. или строкой
def is_bool(value):
    """
    This is an example of Google style.
    Args:
     value: accepts any type of argument
    Returns:
     This is a description of what is returned.
    Raises:
     KeyError: Raises an exception.
    """
    #является ли value строкой
    if isinstance(value, str):
        #строка, функция преобразует ее в нижний регистр с помощью метода
        return value.lower() in ['true', 'false']
    else:
        return isinstance(value, bool)
#определяет тип данных каждого столбца
def detect_column_types(table):
    """
    This is an example of Google style.
    Args:
     table: dictionary
    """

    column_types = {}
    #проходимся по каждому знач. словаря и возвращаем индекс
    for col_index, header in enumerate(table["headers"]):
        #создает список `col_values`, содержащий значения из текущего столбца
        col_values = [row[col_index] for row in table["rows"] if len(row) > col_index and row[col_index] is not None]
        #проверка на преобразованние в целое число
        if all(is_int(value) for value in col_values):
            col_type = 'int'
        #точка с запятой
        elif all(is_float(value) for value in col_values):
            col_type = 'float'
        #булевые значения
        elif all(is_bool(value) for value in col_values):
            col_type = 'bool'
        else:
            #делаем строку
            col_type = 'str'
        #добавление ключей
        column_types[header] = col_type
    return column_types
#Определяет функцию `print_table`, которая принимает словарь `table` в качестве аргумента.
def print_table(table):
    """
    This is an example of Google style.
    Args:
     table: our list
    """
    if not table or not table["headers"] or not table["rows"]:
        print("Таблица пуста.")
        return
    # Форматирование таблицы без использования tabulate
    column_widths = [len(header) for header in table["headers"]]
    for row in table["rows"]:
        for i, cell in enumerate(row):
            if cell is not None:
                column_widths[i] = max(column_widths[i], len(str(cell)))
# Определяет функцию `format_row`, которая принимает одну строку таблицы
    def format_row(row):
        """
        This is an example of Google style.
        Args:
         row: list
        """
        #каждый элемент будет представлять ячейку отформатированной строки.
        return " | ".join(
            (str(cell) if cell is not None else "None").ljust(column_widths[i])
            for i, cell in enumerate(row)
        )
    #вызывает функцию `format_row` с заголовками таблицы (`table["headers"]`) в качестве аргумента.
    header_line = format_row(table["headers"])
    # создается разделительная линия под заголовками.
    separator = "-+-".join("-" * width for width in column_widths)
    print(header_line)
    print(separator)
    for row in table["rows"]:
        print(format_row(row))

def print_row(table, index):
    index -= 1
    if 0 <= index < len(table["rows"]):
        row = table["rows"][index]
        print('\t'.join(map(lambda x: str(x) if x is not None else "None", row)))
    else:
        print("Индекс вне диапазона строк.")
# Определяет функцию `print_row`, которая принимает два аргумента:
def print_column(table, index):
    """
    This is an example of Google style.
    Args:
     index: index in the table
     table: list
    """
    index -= 1
    #находится ли переданный индекс в допустимом диапазоне
    if 0 <= index < len(table["headers"]):
        #сохраняем d row
        print(table["headers"][index])
        for row in table["rows"]:
            if len(row) > index:
                # выводит строку на консоль. Разберем её по частям:
                item = row[index] if row[index] is not None else "None"
                print(item)
    else:
        print("Индекс вне диапазона столбцов.")
#бработка исключений
def get_value(table, row_index, col_index):
    """
    This is an example of Google style.
    Args:
     table: list
     row_index: index
     col_index: index
    Returns:
     table
    Raises:
     IndexError:
    """
    try:
        # Если `row_index` или `col_index` выходят за пределы диапазона, произойдет исключение `IndexError`.
        return table["rows"][row_index][col_index]
    except IndexError:
        return None
#Определяет функцию `set_value`, которая принимает четыре аргумента:
def set_value(table, row_index, col_index, value):
    """
    This is an example of Google style.
    Args:
     table : list
     row_index: index
     col_index:
     value: end abc this is a hten
    """
    #добавляет новые строки в таблицу, пока количество строк не станет больше или равно `row_index`
    while len(table["rows"]) <= row_index:
        table["rows"].append([None] * len(table["headers"]))
    while len(table["rows"][row_index]) < len(table["headers"]):
        table["rows"][row_index].append(None)
    table["rows"][row_index][col_index] = value
#Определяет функцию `concat`, которая принимает две таблицы
def concat(table1, table2):
    """
    This is an example of Google style.
    Args:
     table1: table one or is not value
     table2: table two or is not value
    """
    if table1["headers"] != table2["headers"]:
        raise ValueError("Таблицы имеют разные заголовки")
    combined_rows = table1["rows"] + table2["rows"]
    return {"headers": table1["headers"], "rows": combined_rows}
#Определяет функцию `split`, которая принимает два аргумента:
def split(table, row_number):
    """
    This is an example of Google style.
    Args:
     table: This is the first param.
     row_number: This is a second param.
    Returns:
     This is a description of what is returned.
    Raises:
     KeyError: Raises an exception.
    """
    #находится ли указанный номер строки в допустимом диапазоне
    if row_number < 0 or row_number >= len(table["rows"]):
        raise ValueError("Такой строки не существует")
    # Создает срез списка
    rows1 = table["rows"][:row_number]
    rows2 = table["rows"][row_number:]
    #сохраняем данные
    return {"headers": table["headers"], "rows": rows1}, {"headers": table["headers"], "rows": rows2}

def main():
    table = None
    while True:
        print("\nВы должны ввести номер команды!!!")
        print("\nВыберите действие:")
        print("1. Загрузить таблицу")
        print("2. Создать новую таблицу")
        print("3. Получить значение ячейки")
        print("4. Установить значение ячейки")
        print("5. Вывести строку")
        print("6. Вывести столбец")
        print("7. Вывести всю таблицу")
        print("8. Объединить таблицы")
        print("9. Разделить таблицу на две")
        print("10. Сохранить таблицу")
        print("11. Определить типы столбцов")
        print("12. Загрузить с автоопределением типов столбцов")
        print("13. Выход")

        action = input("Введите номер действия: ").strip()

        if action == "1":
            choice = input("Вывести таблицу из CSV или Pickle? (Вы должны написать 'csv' или 'pkl'): ").strip().lower()
            if choice == 'csv':
                filename = input("Введите имя файла: ").strip()
                filename += '.csv'
                table = load_table_csv(filename)
            elif choice == 'pkl':
                filename = input("Введите имя файла: ").strip()
                filename += '.pkl'
                table = load_table_pickle(filename)
            else:
                print("Неверный выбор.")
    
            if table:
                print("\nЗагруженная таблица:")
                print_table(table)
        
        # Определяем и выводим типы столбцов
                types = detect_column_types(table)
                print("\nОбнаруженные типы столбцов:")
                for col, col_type in types.items():
                    print(f"{col}: {col_type}")
        elif action == "2":
            print("Введите заголовки таблицы (через запятую):")
            headers = input().split(',')
            cleaned_headers = [header.strip() for header in headers]

            rows = []
            print("Введите строки данных (оставьте пустую строку, чтобы завершить ввод):")
            while True:
                row = input("Введите строку данных (разделяя элементы запятыми): ")
                if row == "":
                    break
                row_items = [item.strip() if item.strip() != '' else None for item in row.split(',')]
                rows.append(row_items)

            table = {"headers": cleaned_headers, "rows": rows}
        elif action == "3":
            if table:
                row = int(input("Введите номер строки: ")) - 1
                col = int(input("Введите номер столбца: ")) - 1
                value = get_value(table, row, col)
                print(f"Значение ячейки: {value if value is not None else 'None'}")
            else:
                print("Таблица не загружена.")
        elif action == "4":
            if table:
                row = int(input("Введите номер строки: ")) - 1
                col = int(input("Введите номер столбца: ")) - 1
                value = input("Введите новое значение (оставьте пустым для None): ")
                set_value(table, row, col, value if value != "" else None)
                print("Значение обновлено.")
            else:
                print("Таблица не загружена.")
        elif action == "5":
            if table:
                row_index = int(input("Введите номер строки: "))
                print_row(table, row_index)
            else:
                print("Таблица не загружена.")
        elif action == "6":
            if table:
                column_index = int(input("Введите номер столбца: "))
                print_column(table, column_index)
            else:
                print("Таблица не загружена.")
        elif action == "7":
            if table:
                print("\nТекущая таблица:")
                print_table(table)
            else:
                print("Таблица не загружена.")
        elif action == "8":
            if table:
                other_table = load_table_csv(input("Введите имя файла второй таблицы: ").strip())
                try:
                    table = concat(table, other_table)
                    print("\nТаблицы успешно объединены:")
                    print_table(table)
                except ValueError as e:
                    print(f"Ошибка: {e}")
            else:
                print("Таблица не загружена.")
        elif action == "9":
            if table:
                row_number = int(input("Введите номер строки для разделения: "))
                try:
                    table1, table2 = split(table, row_number)
                    print("\nПервая таблица:")
                    print_table(table1)
                    print("\nВторая таблица:")
                    print_table(table2)
                except ValueError as e:
                    print(f"Ошибка: {e}")
            else:
                print("Таблица не загружена.")
        elif action == "10":
            if table:
                base_filename = input("Введите имя файла (без расширения): ").strip()
                csv_filename = base_filename + ".csv"
                pkl_filename = base_filename + ".pkl"
                save_table_csv(table, csv_filename)
                save_table_pickle(table, pkl_filename)
                print(f"Таблица сохранена в файлы '{csv_filename}' и '{pkl_filename}'.")
            else:
                print("Таблица не загружена.")
        elif action == "11":
            if table:
                types = detect_column_types(table)
                print("\nТипы столбцов:")
                for col, col_type in types.items():
                    print(f"{col}: {col_type}")
            else:
                print("К сожалению, таблица не загрузилась.")
        elif action == "12":
            choice = input("Выберите формат файла для загрузки (csv или pkl): ").strip().lower()
            filename = input("Введите имя файла (без расширения): ").strip()

            if choice == 'csv':
                if not filename.endswith('.csv'):
                    filename += '.csv'
                table = load_table_csv(filename, detect_types=True)
            elif choice == 'pkl':
                if not filename.endswith('.pkl'):
                    filename += '.pkl'
                table = load_table_pickle(filename)
        # Определение типов столбцов для Pickle
                types = detect_column_types(table)
                print("Обнаруженные типы столбцов:")
                for col, col_type in types.items():
                    print(f"{col}: {col_type}")
            else:
                print("Неверный выбор формата.")
                continue  # Возвращаемся к основному меню
            if table:
                print("\nЗагруженная таблица:")
                print_table(table)
        elif action == "13":
            print("Выход.")
            break
        else:
            print("Неверный выбор, попробуйте еще раз.")
            
print(main())