import json
from typing import List, Dict, Any

import requests


class ApiClient:
    def __init__(self, url: str):
        self.base_url = url

    def get(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()


class VacancyFormatter:
    @staticmethod
    def format_vacancy(vacancy: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "name": vacancy.get("name", "Не указано"),
            "salary": vacancy.get("salary", "Не указано"),
            "url": vacancy.get("alternate_url", "Не указано"),
            "company_name": vacancy.get("employer", {}).get("name", "Не указано")
        }

    @staticmethod
    def format_data(vacancies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        company_dict = {}

        for vacancy in vacancies:
            salary = vacancy.get("salary")
            if salary and salary.get("currency") == 'RUR':
                formatted_vacancy = VacancyFormatter.format_vacancy(vacancy)
                company_name = formatted_vacancy["company_name"]

                if company_name not in company_dict:
                    company_dict[company_name] = {
                        "company_name": company_name,
                        "vacancies": []
                    }
                company_dict[company_name]["vacancies"].append(formatted_vacancy)

        return list(company_dict.values())


class HhApi:
    def __init__(self, base: ApiClient):
        self.client = base

    def get_companies_and_vacancies(self, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        endpoint = "vacancies"
        data = self.client.get(endpoint, params)
        return VacancyFormatter.format_data(data['items'])


if __name__ == "__main__":
    base_url = "https://api.hh.ru/"
    client = ApiClient(base_url)
    hh_api = HhApi(client)
    companies = hh_api.get_companies_and_vacancies({'per_page': 100})

    with open('./data/companies.json', 'w', encoding='utf-8') as f:
        json.dump(companies, f, ensure_ascii=False, indent=4)
