from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    vacancies = relationship('Vacancy', back_populates='company')


class Vacancy(Base):
    __tablename__ = 'vacancies'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    salary_from = Column(Integer)
    salary_to = Column(Integer)
    currency = Column(String, nullable=False)
    gross = Column(Boolean)
    url = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'))
    company = relationship('Company', back_populates='vacancies')
