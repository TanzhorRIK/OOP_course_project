import abstract_classes
import json


class Vacancy:
    """Класс для созданной вакансии"""

    def __init__(self, title=None, area=None, salary=None,
                 employment=None) -> None:
        self.title = title
        self.area = area
        self.salary = salary
        self.employment = employment

    def validate(self):
        """Метод проверки данных"""

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


class JSONVacancyFileManager(abstract_classes.VacancyFileManager):
    """Файловый менеджер"""

    def __init__(self, filename="../vacanci/result.json"):
        self.filename = filename
        open(filename, 'w').close()

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Метод для добавления вакансий в файл"""

        with open(self.filename, 'a', encoding="utf-8") as file:
            vacancy_data = {
                'title': vacancy.title,
                'area': vacancy.area,
                'salary': vacancy.salary,
                'employment': vacancy.employment
            }
            json.dump(vacancy_data, file, ensure_ascii=False)
            file.write('\n')

    def get_vacancies(self, criterion: str, requirement: str) -> list:
        """Метод для получения вакансий из файла"""

        vacancies = []
        with open(self.filename, 'r', encoding="utf-8") as file:
            for line in file:
                vacancy_data = json.loads(line)
                if (criterion == "зарплата" and int(requirement) >= vacancy_data['salary'] or
                        criterion == "название" and requirement.lower() in vacancy_data["title"].lower() or
                        criterion == "место" and requirement.lower() in vacancy_data['area'].lower() or
                        criterion == "занятость" and requirement.lower() in vacancy_data['employment'].lower()):
                    vacancies.append(Vacancy(
                        vacancy_data['title'],
                        vacancy_data['area'],
                        vacancy_data['salary'],
                        vacancy_data['employment']))
                else:
                    continue

        return vacancies

    def remove_vacancy(self, index_of_string_result_json: list) -> None:
        """Метод для удаления вакансий из файла"""

        with open(self.filename, "r", encoding="utf-8") as in_f:
            lines = [line for line in in_f]
        with open(self.filename, 'w', encoding="utf-8") as file:
            for index_line in range(len(lines)):
                if index_line not in index_of_string_result_json:
                    print(lines[index_line], file=file, end="")
