from abc import ABC, abstractmethod


class VacancyAPI(ABC):
    """Обстарктный класс"""

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class VacancyFileManager(ABC):
    """Обстрактный класс"""

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, criteria):
        pass

    @abstractmethod
    def remove_vacancy(self, vacancy):
        pass
