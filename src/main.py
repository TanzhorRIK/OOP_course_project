from classes import *

def main():
    print("Welcome to the Vacancy Management System!")
    api_choice = input(
        "Choose the API platform (HH - hh.ru, SJ - superjob.ru): ")
    vacancies = []

    if api_choice.lower() == 'hh':
        region_name = input(
            "In which region will we search?(Moscow, Saint Petersburg, Novosibirsk):")
        search_text = input("Enter the search text:")
        if region_name.lower() == "moscow":
            region = 1
        elif region_name == "saint petersburg":
            region = 2
        else:
            region = 1202

        api = HHVacancyAPI(search_text, region)
        api.connect()  # Подключение к API
        api.get_vacancies()  # Получение вакансий
        with open("../vacanci/hh.json", "r", encoding='utf8') as f:
            data = json.load(f)
            for item in data["items"]:
                title = item["name"]
                area = item["area"]["name"] if "name" in item["area"] and item["area"]["name"].lower() == region_name.lower() else None
                salary = item["salary"]["to"] if item["salary"] and "to" in item["salary"] else None
                employment = item["employment"]["name"]
                vacancy = Vacancy(title, area, salary, employment)
                if vacancy.validate():
                    vacancies.append(vacancy)

    elif api_choice.lower() == "sj":
        print("Get start in Moskow")
        search_text = input("Enter the search text:")
        api = SJVacancyAPI(search_text)
        api.connect()  # Подключение к API
        api.get_vacancies()  # Получение вакансий
        with open("../vacanci/superjob.json", "r", encoding='utf8') as f:
            data = json.load(f)
            for item in data["objects"]:
                title = item["profession"]
                area = item["town"]["title"]
                salary = item["payment_to"] if item["payment_to"] else None
                employment = item['type_of_work']['title']
                vacancy = Vacancy(title, area, salary, employment)
                if vacancy.validate():
                    vacancies.append(vacancy)

    print("Let's go through the vacancies")
    print(f"Total found {len(vacancies)}")
    number_to_view = int(input("How many pieces will we look at from them?(Specify the number):"))
    if len(vacancies) < number_to_view:
        number_to_view = len(vacancies)
    filemanager = JSONVacancyFileManager()
    print("Vacancies are sorted in descending order of salary")
    vacancies.sort(key=lambda x: x, reverse=True)
    for i in range(number_to_view):
        filemanager.add_vacancy(vacancies[i])
    list_index_to_remove = []
    for i in range(number_to_view):
        print(vacancies[i])
        print("Is this vacancy suitable for you?(Yes/No)")
        if input().lower() == "no":
            list_index_to_remove.append(i)

    filemanager.remove_vacancy(list_index_to_remove)
    print("Here is a list of suitable vacancies:")
    print(*filemanager.get_vacancies(), sep="\n")


if __name__ == "__main__":
    main()
