from requests import get
from requests import post
from requests import delete
from requests import put

print("Все работы: ", get('http://localhost:5000/api/jobs').json())
print("Одна работа: ", get('http://localhost:5000/api/jobs/1').json())
print("Несуществующая работа: ", get('http://localhost:5000/api/jobs/3141592653').json()) #нахождение несуществующей работы с id равным первым 10 цифрам числа pi
print("Проверка GET-запроса: ", get('http://localhost:5000/api/jobs/1', json={'job': 'Проверка работы API'}).json()) #проверка невозможности изменить работу через GET-запрос
print("Неверный ID: ", get('http://localhost:5000/api/jobs/три').json())


'''Напишите файл тестирования корректного запроса и нескольких некорректных (не менее трех). В файле должны присутствовать комментарии, в чем именно заключается некорректность запроса.

Добавьте запрос на получение всех работ, чтобы убедиться, что работа добавлена.'''

print("Пустой запрос :", post('http://localhost:5000/api/jobs/2', json={}).json())
print("Отсутствует ключ: ", post('http://localhost:5000/api/jobs/2', json={'team_leader': 1, 'job': 'Проверка работы API', 'work_size': 10, 'collaborators': '2, 3'}).json())
print("Неверный тип данных: ", post('http://localhost:5000/api/jobs/2', json={'team_leader': 1, 'job': 'Проверка работы API', 'work_size': 'десять', 'collaborators': '2, 3', 'is_finished': False}).json())
print("Уже существующий ID: ", post('http://localhost:5000/api/jobs/1', json={'team_leader': 1, 'job': 'Проверка работы API', 'work_size': 10, 'collaborators': '2, 3', 'is_finished': False}).json())
print("Проверка добавленной работы: ", get('http://localhost:5000/api/jobs').json())

'''Напишите файл тестирования корректного запроса на удаление и нескольких некорректных. Добавьте запрос на получение всех работ, чтобы убедиться, что работа удалена.'''
print("Удаление работы: ", delete('http://localhost:5000/api/jobs/2').json())
print("Проверка удаленной работы: ", get('http://localhost:5000/api/jobs/2').json())
print("Проверка всех работ: ", get('http://localhost:5000/api/jobs').json())

"""Напишите файл тестирования корректного запроса на редактирование и нескольких некорректных. Добавьте запрос на получение всех работ, чтобы убедиться, что работа изменена."""
print("Редактирование работы: ", put('http://localhost:5000/api/jobs/1', json={'job': 'Проверка редактирования работы API'}).json())
print("Провверка некорректного запроса(неверный тип данных): ", put('http://localhost:5000/api/jobs/1', json={'work_size': 'десять'}).json())
print("Проверка некорректного запроса(несуществующий ID): ", put('http://localhost:5000/api/jobs/3141592653', json={'job': 'Проверка редактирования работы API'}).json())
print("Проверка некорректного запроса(пустой запрос): ", put('http://localhost:5000/api/jobs/1', json={}).json())
print("Проверка отредактированной работы: ", get('http://localhost:5000/api/jobs/1').json())