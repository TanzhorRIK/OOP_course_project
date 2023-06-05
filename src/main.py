from classes import Vacancy, JSONVacancyFileManager
from classes_api import HHVacancyAPI, SJVacancyAPI
import json


def main():
    """Основная функция"""

    print("Welcome to the Vacancy Management System!")
    # Предлагаем пользователю выбрать нужную площадку для поиска вакансий
    api_choice = input(
        "Choose the API platform (HH - hh.ru, SJ - superjob.ru): ")

    # Создаём список из будущих экземпляров класса Vacancy
    vacancies = []
    if api_choice.lower() == 'hh':
        # Предлагаем пользователю выбрать город поиска
        region_name = input(
            "In which region will we search?(Москва, Санкт-Петербург, Новосибирск):")
        # Предлагаем пользователю выбрать вакасию для поиска
        search_text = input("Enter the search text:")
        if region_name == "москва":
            region = 1
        elif region_name == "Санкт-Петербург":
            region = 2
        else:
            region = 1202

        # создаем экземпляр класс
        api = HHVacancyAPI(search_text, region)
        # Подключение к API
        api.connect()
        # Получение вакансий
        api.get_vacancies()
        with open("../vacanci/hh.json", "r", encoding='utf8') as f:
            data = json.load(f)
            for item in data["items"]:
                title = item["name"]
                area = item["area"]["name"]
                if item["salary"]:
                    salary_from = item['salary']['from'] if item['salary'][
                        'from'] else 0
                    salary_to = item['salary']['to'] if item['salary'][
                        'to'] else 0
                    salary = abs(salary_to - salary_from)
                else:
                    salary = None
                employment = item["employment"]["name"]
                vacancy = Vacancy(title, area, salary, employment)
                if vacancy.validate():
                    vacancies.append(vacancy)

    elif api_choice.lower() == "sj":
        print("Get start in Moskow")
        # Предлагаем пользователю выбрать вакасию для поиска
        search_text = input("Enter the search text:")

        # создаем экземпляр класс
        api = SJVacancyAPI(search_text)
        # Подключение к API
        api.connect()
        # Получение вакансий
        api.get_vacancies()
        # Открываем файл и начинаем обработку данных
        with open("../vacanci/superjob.json", "r", encoding='utf8') as f:
            data = json.load(f)
            for item in data["objects"]:
                title = item["profession"]
                area = item["town"]["title"]
                salary = abs(item["payment_to"] - item["payment_from"])
                employment = item['type_of_work']['title']
                vacancy = Vacancy(title, area, salary, employment)

                # отсеиваем вакансии без нужных параметров
                if vacancy.validate():
                    vacancies.append(vacancy)

    # Ведем основную работу по уже готовым вакансиям с пользователем
    print(f"Total found {len(vacancies)}")
    if len(vacancies):
        print("Let's go through the vacancies")
        print(f"Total found {len(vacancies)}")
        # Предлагаем посмотреть какое-то число вакансий
        number_to_view = int(input(
            "How many pieces will we look at from them?(Specify the number):"))
        if len(vacancies) < number_to_view:
            number_to_view = len(vacancies)
        # Создаем файловый менеджер для дальнейшей работы с ним
        filemanager = JSONVacancyFileManager()
        # Сортируем данные для удобства по убыванию зарплаты
        print("Vacancies are sorted in descending order of salary")
        vacancies.sort(key=lambda x: x, reverse=True)
        # Заполняем результирующий json-файл с подходящими вакансиями
        for i in range(number_to_view):
            filemanager.add_vacancy(vacancies[i])
        list_index_to_remove = []
        # Предлагаем убрать неподходящие вакансии
        for i in range(number_to_view):
            print(vacancies[i])
            print("Is this vacancy suitable for you?(Да/Нет)")
            if input().lower() == "нет":
                list_index_to_remove.append(i)
        # Убираем все неподходящие вакансии
        filemanager.remove_vacancy(list_index_to_remove)
        # Предлагае отфильтровать только те вакансии, которые нужны пользователю
        # в данный момент из результирующего json-файла
        print(
            "По каким критериям хочешь получить вакансии?(название/место/зарплата/занятость: ")
        criterion = input().lower()
        if criterion == "зарплата":
            requirement = input("Укажи предел(число):")
        elif criterion == "название":
            requirement = input("какое слово будем искать в должности?")
        elif criterion == "место":
            requirement = input("Какой город нужен?")
        else:
            requirement = input("Какая занятость нужна?")
        # Выводим отфильтрованные вакансии
        print("Here is a list of suitable vacancies:")
        print(*filemanager.get_vacancies(criterion, requirement), sep="\n")
    else:
        print("try another later")

if __name__ == "__main__":
    main()
