"""Для базы данных, созданной по рассмотренным ранее моделям User и Jobs, нужно написать запрос.
Напишите программу, которая считывает из консоли имя базы данных, подключается к ней с использованием возможностей библиотеки sqlalchemy и выводит id колонистов, которые проживают в 1 модуле и ни профессия (speciality), ни должность (position) которых не содержат подстроку engineer, каждый с новой строки."""


from data.db_session import global_init, create_session
from data.users import User
from data.jobs import Jobs

fname = input()
global_init(fname)
session = create_session()
users = (
    session.query(User)
    .filter(
        User.address == "module_1",
        ~User.speciality.contains("engineer"),
        ~User.position.contains("engineer"),
    )
    .all()
)
for user in users:
    print(user.id)
