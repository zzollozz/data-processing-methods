"""1. Посмотреть документацию к API GitHub,
 разобраться как вывести список репозиториев для конкретного пользователя,
 сохранить JSON-вывод в файле *.json."""

import requests
def list_repo_user_gh(url):
    with open('list_repo_user_gh.json', 'w') as f:
        response = (requests.get(url)).json()
        # response = response.json()
        name = url.split('/')
        f.write(f"Список репозиториев пользователя {name[-2]}: {(response[0]).get('name')}, {(response[1]).get('name')} \n Результат запроса по API: \n {response}")
        # print(f"Список репозиториев пользователя {name[-2]}: {(response[0]).get('name')}, {(response[1]).get('name')} \n Результат запроса по API: \n {response}")
        print('Файл записан!')


repos_url = 'https://api.github.com/users/zzollozz/repos'
list_repo_user_gh(repos_url)
