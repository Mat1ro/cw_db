import json
from typing import List, Dict, Any, Optional

import requests


class ApiClient:
    """
    A client for interacting with an API.

    Attributes:
        base_url (str): The base URL for the API.
    """

    def __init__(self, url: str):
        """
        Initializes the ApiClient with the given base URL.

        Args:
            url (str): The base URL for the API.
        """
        self.base_url = url

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sends a GET request to the specified endpoint with optional parameters.

        Args:
            endpoint (str): The API endpoint to send the GET request to.
            params (Optional[Dict[str, Any]]): The query parameters for the GET request.

        Returns:
            Dict[str, Any]: The JSON response from the API.
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()


class VacancyFormatter:
    """
    A utility class for formatting vacancy data.
    """

    @staticmethod
    def format_vacancy(vacancy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formats a single vacancy.

        Args:
            vacancy (Dict[str, Any]): The raw vacancy data.

        Returns:
            Dict[str, Any]: The formatted vacancy data.
        """
        return {
            "name": vacancy.get("name", "Не указано"),
            "salary": vacancy.get("salary", "Не указано"),
            "url": vacancy.get("alternate_url", "Не указано"),
            "company_name": vacancy.get("employer", {}).get("name", "Не указано")
        }

    @staticmethod
    def format_data(vacancies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Formats a list of vacancies and groups them by company.

        Args:
            vacancies (List[Dict[str, Any]]): The raw vacancies data.

        Returns:
            List[Dict[str, Any]]: The formatted data grouped by company.
        """
        company_dict: Dict[str, Dict[str, Any]] = {}

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
    """
    A class for interacting with the HeadHunter API.

    Attributes:
        client (ApiClient): The API client to use for requests.
    """

    def __init__(self, base: ApiClient):
        """
        Initializes the HhApi with the given API client.

        Args:
            base (ApiClient): The API client to use for requests.
        """
        self.client = base

    def get_companies_and_vacancies(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Retrieves companies and their vacancies from the API.

        Args:
            params (Optional[Dict[str, Any]]): The query parameters for the request.

        Returns:
            List[Dict[str, Any]]: The list of companies and their vacancies.
        """
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
