"""1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию. Добавить в решение
со сбором вакансий(продуктов) функцию, которая будет добавлять только новые вакансии/продукты в вашу базу."""

"""2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы 
   (необходимо анализировать оба поля зарплаты - минимальнную и максимульную). """

from pprint import pprint
from exchange_rates import exchange_rates
from hh import job_search_hh
import pymongo
from sshtunnel import SSHTunnelForwarder


MONGO_HOST = '192.168.1.73'
MONGO_DB = "hh"
MONGO_USER = "robot"
MONGO_PASS = "1111"

server = SSHTunnelForwarder(
    MONGO_HOST,
    ssh_username=MONGO_USER,
    ssh_password=MONGO_PASS,
    remote_bind_address=('127.0.0.1', 27017)
)
server.start()

client = pymongo.MongoClient('127.0.0.1', server.local_bind_port) # server.local_bind_port is assigned local port
db = client[MONGO_DB]
vacancy_hh = db.vacancy_hh

USD = exchange_rates('USD')
KZT = exchange_rates('KZT')
# print(USD, KZT)  # проверка
                            # Ф-я добавления новых вaкансий
def new_vacancy():
    data = job_search_hh('Python')   # парсиг данных
    print('Новая база загружена')
    n = 0
    for vacancies in data:
        if vacancy_hh.find({'Сылка на вакансию': {'$ne': vacancies.get('Сылка на вакансию')}}):
            # pprint(vacancies) # проверка выхода новых вакансий
            vacancy_hh.insert_one(vacancies) # добавление новых документов в базу
            n += 1
    print(f'Всего выканий: {vacancy_hh.find().count()}, Добавлено новых: {n}')



                            # Ф-я вывода зп по выкансии
def get_salry(num: int):

    result = vacancy_hh.find({'$or':
                                  [{'Оплата_min': {'$gt': num}, 'Валюта': 'руб.'},
                                   {'Оплата_max': {'$gt': num}, 'Валюта': 'руб.'},
                                   {'Оплата_min': {'$gt': num / USD}, 'Валюта': 'USD'},
                                   {'Оплата_max': {'$gt': num / USD}, 'Валюта': 'USD'},
                                   {'Оплата_min': {'$gt': num / KZT}, 'Валюта': 'KZT'},
                                   {'Оплата_max': {'$gt': num / KZT}, 'Валюта': 'KZT'}
                                   ]
                              })
    return list(result)


# new_vacancy()   # добавление выкансий

num = int(input('Укажите минимальную ЗП в рублях: ')) # сортировка по минимальному запросу в оплатеы
pprint(get_salry(num))



