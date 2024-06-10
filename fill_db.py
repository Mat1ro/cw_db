import json

from sqlalchemy.orm import sessionmaker

from db import engine
from models import Company, Vacancy


def load_data(path):
    # Чтение данных из JSON файла
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


data = load_data("data/companies.json")

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Вставка данных о работодателях и вакансиях
for company_data in data:
    company_name = company_data["company_name"]

    # Проверка на дубликаты
    company = session.query(Company).filter_by(name=company_name).first()

    if company is None:
        company = Company(name=company_name)
        session.add(company)
        session.commit()

    for vacancy_data in company_data["vacancies"]:
        vacancy_name = vacancy_data["name"]
        salary_from = vacancy_data["salary"]["from"]
        salary_to = vacancy_data["salary"]["to"]
        currency = vacancy_data["salary"]["currency"]
        gross = vacancy_data["salary"]["gross"]
        url = vacancy_data["url"]

        # Проверка на дубликаты вакансий
        vacancy = session.query(Vacancy).filter_by(name=vacancy_name, company_id=company.id, url=url).first()

        if vacancy is None:
            vacancy = Vacancy(
                name=vacancy_name,
                salary_from=salary_from,
                salary_to=salary_to,
                currency=currency,
                gross=gross,
                url=url,
                company=company
            )
            session.add(vacancy)

# Подтверждение изменений
session.commit()

# Закрытие сессии
session.close()
