from abc import ABC, abstractmethod
import requests
import json
import os
import time

SUPERJOB_API_KEY = os.environ.get('SUPERJOB_API_KEY')


class VacancyAPI(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class VacancyFileManager(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, criteria):
        pass

    @abstractmethod
    def remove_vacancy(self, vacancy):
        pass


class HHVacancyAPI(VacancyAPI):
    def __init__(self, search_text, region=1202):
        self.search_text = search_text
        self.region = region

    def connect(self, page=0):
        # Здесь можно добавить код для подключения к API сайта hh.ru
        params = {
            'text': 'NAME:' + self.search_text,
            # Текст фильтра. В имени должно быть слово "Аналитик"
            'area': self.region,
            # Поиск ощуществляется по вакансиям города Москва
            'page': page,  # Индекс страницы поиска на HH
            'per_page': 100  # Кол-во вакансий на 1 странице
        }
        try:
            req = requests.get('https://api.hh.ru/vacancies', params)
            data = req.content.decode()
            req.close()
            return data
        except:
            print("failed to connect to the server")

    def get_vacancies(self):
        try:
            os.mkdir("../vacanci")
        except:
            print("the folder has already been created")
        for page in range(0, 20):

            jsObj = json.loads(self.connect(page))

            f = open("../vacanci/hh.json", mode='w', encoding='utf8')

            with open("../vacanci/hh.json", mode='w', encoding='utf8') as f:
                f.write(json.dumps(jsObj, ensure_ascii=False, indent=4,
                                   separators=(",", ":")))
            f.close()

            if (jsObj['pages'] - page) <= 1:
                break

            # Необязательная задержка, но чтобы не нагружать сервисы hh
            time.sleep(0.25)


class SJVacancyAPI(VacancyAPI):
    def __init__(self, search_text, region=13):
        self.search_text = search_text
        self.region = region

    def connect(self, page=0):
        params = {'town': 14,
                  'count': 100,
                  'keyword': self.search_text

                  }
        headers = {'X-Api-App-Id': SUPERJOB_API_KEY}
        req = requests.get(
            'https://api.superjob.ru/2.0/vacancies/?t=4&count=100', params,
            headers=headers)
        data = req.content.decode()
        req.close()
        return data

    def get_vacancies(self):
        try:
            os.mkdir("../vacanci")
        except:
            print("the folder has already been created")

        for page in range(0, 20):
            jsObj = json.loads(self.connect(page))
            filename = '../vacanci/superjob.json'
            with open(filename, mode='w', encoding='utf8') as f:
                f.write(json.dumps(jsObj, ensure_ascii=False, indent=4,
                                   separators=(",", ":")))


class Vacancy:
    def __init__(self, title=None, area=None, salary=None, employment=None):
        self.title = title
        self.area = area
        self.salary = salary
        self.employment = employment

    def validate(self):
        if not self.title or not self.area or not self.salary or not self.employment:
            return False
        return True

    def __repr__(self):
        return f"Vacancy(title='{self.title}', salary='{self.salary}')"

    def __str__(self):
        return f"------------------\nНазвание: {self.title}\nГород: {self.area}\nЗарплата: {self.salary}\nЗанятость: {self.employment}"

    def __eq__(self, other):
        return self.salary == other.salary

    def __ne__(self, other):
        # !=
        return self.salary != other.salary

    def __lt__(self, other):
        return self.salary < other.salary

    def __gt__(self, other):
        # >
        return self.salary > other.salary

    def __le__(self, other):
        return self.salary <= other.salary

    def __ge__(self, other):
        return self.salary >= other.salary


class JSONVacancyFileManager(VacancyFileManager):
    def __init__(self, filename="../vacanci/result.json"):
        self.filename = filename

    def add_vacancy(self, vacancy):
        with open(self.filename, 'a', encoding="utf-8") as file:
            vacancy_data = {
                'title': vacancy.title,
                'area': vacancy.area,
                'salary': vacancy.salary,
                'employment': vacancy.employment
            }
            json.dump(vacancy_data, file, ensure_ascii=False)
            file.write('\n')

    def get_vacancies(self):
        vacancies = []
        with open(self.filename, 'r', encoding="utf-8") as file:
            for line in file:
                vacancy_data = json.loads(line)
                vacancies.append(Vacancy(
                    vacancy_data['title'],
                    vacancy_data['area'],
                    vacancy_data['salary'],
                    vacancy_data['employment']))

        return vacancies

    def remove_vacancy(self, index_of_string_result_json):
        with open(self.filename, "r", encoding="utf-8") as in_f:
            lines = [line for line in in_f]
        with open(self.filename, 'w', encoding="utf-8") as file:
            for index_line in range(len(lines)):
                if index_line not in index_of_string_result_json:
                    print(lines[index_line], file=file, end="")
