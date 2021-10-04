import re
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

"""Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем должность) 
с сайтов HH(обязательно) и/или Superjob(по желанию). Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
 Получившийся список должен содержать в себе минимум:
Наименование вакансии.
Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
Ссылку на саму вакансию.
Сайт, откуда собрана вакансия.
Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv."""

def job_search_hh(vacancy):
    url = 'https://hh.ru'
    params = {
        'fromSearchLine': 'true',
        'st': 'searchVacancy',
        'text': vacancy,
        'from': 'suggest_post',
        'page': 1
    }
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

    vacancy_result = []
    while True:
        response = requests.get(url + '/search/vacancy', params=params, headers=headers)
        dom = bs(response.text, 'html.parser')
        list_of_vacancies = dom.find_all('div', attrs={'class': 'vacancy-serp-item'})
        if not list_of_vacancies or not response.ok:
            break

        for vacancies in list_of_vacancies:
            vacancies_data = {}
            vacancies_name = vacancies.find('a', attrs={'class': 'bloko-link'}).text
            vacancies_link = vacancies.find('a', attrs={'class': 'bloko-link'})['href']
            source = url

            payment = vacancies.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})

            if not payment:
                payment_min = None
                payment_max = None
                payment_currency = None
            else:
                payment = payment.getText() \
                    .replace(u'\xa0', u'')

                payment = re.split(r'\s|-', payment)

                if payment[0] == 'до':
                    payment_min = None
                    payment_max = int(payment[1])
                elif payment[0] == 'от':
                    payment_min = int(payment[1])
                    payment_max = None
                else:
                    payment_min = int(payment[0])
                    payment_max = int(payment[3])

                payment_currency = payment[-1]

            vacancies_data['Вакансия'] = vacancies_name
            vacancies_data['Оплата_min'] = payment_min
            vacancies_data['Оплата_max'] = payment_max
            vacancies_data['Валюта'] = payment_currency
            vacancies_data['Сылка на вакансию'] = vacancies_link
            vacancies_data['Источник'] = source
            vacancy_result.append(vacancies_data)
            # vacancies_payment = vacancies.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
            #
            # if not vacancies_payment:
            #     vacancies_payment = None
            # else:
            #     vacancies_payment = vacancies_payment.getText()
            #     vacancies_payment = " ".join(re.split(r'\s|-', vacancies_payment))
            #
            # vacancies_data['Вакансия'].append(vacancies_name)
            # vacancies_data['Оплата'].append(vacancies_payment)
            # vacancies_data['Сылка'].append(vacancies_link)
            # vacancies_data['Источник'].append(source)

        params['page'] += 1

        dataFrame = pd.DataFrame(vacancy_result)
    print(dataFrame[['Вакансия', 'Оплата_min', 'Оплата_max', 'Валюта']])
    # print(vacancy_result)
    with open('hh.csv', 'w'):
         dataFrame.to_csv('hh.csv')



job_search_hh('Python')

