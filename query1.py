
from data import db_session
from data.users import User
from data.jobs import Jobs

fname = input()
db_session.global_init(fname)
session = db_session.create_session()
users = session.query(User).filter(User.address == '1').all()
for user in users:
    print(user)
    
    
"""Итак, у нас есть база данных, созданная по рассмотренным ранее моделям User и Jobs, начнем с ней работать. Для более понятного вывода у модели User переопределен метод __repr__, чтобы объекты класса выводились в виде строки: <Colonist> {id} {surname} {name}

Напишите программу, которая считывает из консоли имя базы данных, подключается к ней с использованием возможностей библиотеки sqlalchemy и выводит всех колонистов, проживающих в первом модуле, каждого с новой строки."""