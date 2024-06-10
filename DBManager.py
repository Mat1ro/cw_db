from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from models import Base, Company, Vacancy


class DBManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_companies_and_vacancies_count(self):
        result = self.session.query(
            Company.name,
            func.count(Vacancy.id).label('vacancies_count')
        ).join(Vacancy, isouter=True).group_by(Company.id).order_by(func.count(Vacancy.id).desc()).all()
        return result

    def get_all_vacancies(self):
        result = self.session.query(
            Company.name.label('company_name'),
            Vacancy.name.label('job_title'),
            Vacancy.salary_from,
            Vacancy.salary_to,
            Vacancy.url
        ).join(Company).all()
        return result

    def get_avg_salary(self):
        result = self.session.query(
            func.avg((Vacancy.salary_from + Vacancy.salary_to) / 2)
        ).filter(Vacancy.salary_from.isnot(None), Vacancy.salary_to.isnot(None)).scalar()
        return result

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        result = self.session.query(
            Company.name.label('company_name'),
            Vacancy.name.label('job_title'),
            Vacancy.salary_from,
            Vacancy.salary_to,
            Vacancy.url
        ).join(Company).filter(
            ((Vacancy.salary_from + Vacancy.salary_to) / 2) > avg_salary
        ).all()
        return result

    def get_vacancies_with_keyword(self, keyword):
        result = self.session.query(
            Company.name.label('company_name'),
            Vacancy.name.label('job_title'),
            Vacancy.salary_from,
            Vacancy.salary_to,
            Vacancy.url
        ).join(Company).filter(
            Vacancy.name.ilike(f'%{keyword}%')
        ).all()
        return result

    def close_connection(self):
        self.session.close()


# Пример использования класса
if __name__ == "__main__":
    db_url = 'postgresql://postgres:postgres@localhost/postgres'
    db_manager = DBManager(db_url)

    print("Companies and vacancies count:")
    print(db_manager.get_companies_and_vacancies_count())

    print("\nAll vacancies:")
    print(db_manager.get_all_vacancies())

    print("\nAverage salary:")
    print(db_manager.get_avg_salary())

    print("\nVacancies with higher salary than average:")
    print(db_manager.get_vacancies_with_higher_salary())

    print("\nVacancies with keyword 'менеджер':")
    print(db_manager.get_vacancies_with_keyword('менеджер'))

    db_manager.close_connection()
