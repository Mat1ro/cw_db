from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Company(Base):
    """
    Represents a company in the database.

    Attributes:
        id (int): The primary key of the company.
        name (str): The unique name of the company.
        vacancies (List[Vacancy]): The list of vacancies associated with the company.
    """
    __tablename__ = 'companies'
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, unique=True, nullable=False)
    vacancies: list['Vacancy'] = relationship('Vacancy', back_populates='company')


class Vacancy(Base):
    """
    Represents a vacancy in the database.

    Attributes:
        id (int): The primary key of the vacancy.
        name (str): The name of the vacancy.
        salary_from (int): The starting salary for the vacancy.
        salary_to (int): The maximum salary for the vacancy.
        currency (str): The currency of the salary.
        gross (bool): Indicates whether the salary is gross or net.
        url (str): The URL of the vacancy posting.
        company_id (int): The foreign key referencing the company.
        company (Company): The company associated with the vacancy.
    """
    __tablename__ = 'vacancies'
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, nullable=False)
    salary_from: int = Column(Integer)
    salary_to: int = Column(Integer)
    currency: str = Column(String, nullable=False)
    gross: bool = Column(Boolean)
    url: str = Column(String, nullable=False)
    company_id: int = Column(Integer, ForeignKey('companies.id'))
    company: Company = relationship('Company', back_populates='vacancies')
