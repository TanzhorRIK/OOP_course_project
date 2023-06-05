import requests
import json
import os
import time
import abstract_classes

SUPERJOB_API_KEY = os.environ.get('SUPERJOB_API_KEY')

class HHVacancyAPI(abstract_classes.VacancyAPI):
    """Класс для подключения к API hh.ru"""

    def __init__(self, search_text, region=1202) -> None:
        self.search_text = search_text
        self.region = region

    def connect(self, page: int = 0) -> str:
        """Метод для подключения к API"""

        params = {
            'text': 'NAME:' + self.search_text,
            'area': self.region,
            'page': page,
            'per_page': 100
        }
        try:
            req = requests.get('https://api.hh.ru/vacancies', params)
            data = req.content.decode()
            req.close()
            return data
        except:
            print("failed to connect to the server")

    def get_vacancies(self) -> None:
        """метод для получения вакансий с API в файл"""

        try:
            os.mkdir("../vacanci")
        except:
            pass
        for page in range(0, 20):

            jsObj = json.loads(self.connect(page))

            f = open("../vacanci/hh.json", mode='w', encoding='utf8')

            with open("../vacanci/hh.json", mode='w', encoding='utf8') as f:
                f.write(json.dumps(jsObj, ensure_ascii=False, indent=4,
                                   separators=(",", ":")))

            #
            # with open("../vacanci/hh.json", "r", encoding="utf-8") as in_data:
            #     data = in_data.read()
            # data = data.replace("null", "None")
            # with open("../vacanci/hh.json", "w", encoding="utf-8") as out_f:
            #     print(data, file=out_f)
            if (jsObj['pages'] - page) <= 1:
                break

            # Необязательная задержка, но чтобы не нагружать сервисы hh
            time.sleep(0.25)


class SJVacancyAPI(abstract_classes.VacancyAPI):
    """Класс для подключения к API superjob.ru"""

    def __init__(self, search_text: str, region: int = 13) -> None:
        self.search_text = search_text
        self.region = region

    def connect(self, page: int = 0) -> str:
        """Метод для подключения к API"""

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

    def get_vacancies(self) -> None:
        """Метод для подключения к API"""

        try:
            os.mkdir("../vacanci")
        except:
            pass

        for page in range(0, 20):
            jsObj = json.loads(self.connect(page))
            filename = '../vacanci/superjob.json'
            with open(filename, mode='w', encoding='utf8') as f:
                f.write(json.dumps(jsObj, ensure_ascii=False, indent=4,
                                   separators=(",", ":")))

