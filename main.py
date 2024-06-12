from db import create_tables
from fill_db import fill_database, load_data


def main():
    # Создание таблиц
    create_tables()
    # Загрузка данных из файла
    data = load_data("data/companies.json")
    # Заполнение базы данных
    fill_database(data)


if __name__ == "__main__":
    main()
