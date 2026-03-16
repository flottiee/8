from flask import Flask, redirect, render_template
from flask_login import LoginManager, login_user, logout_user
from data.login_form import LoginForm
from data.job_form import AddJobForm
from data.register_form import RegisterForm
import datetime
from sqlalchemy.exc import IntegrityError

from data import db_session
from data.users import User
from data.jobs import Jobs


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)

@app.route("/")
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    #users = session.query(User).all()
    return render_template("index.html", jobs=jobs)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/add_job", methods=['GET', 'POST'])
def add_job():
    add_form = AddJobForm()
    if add_form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs(
            team_leader=add_form.team_leader.data,
            job=add_form.job.data,
            work_size=add_form.work_size.data,
            collaborators=add_form.collaborators.data or "",
            start_date=datetime.datetime.now(),
            is_finished=bool(add_form.is_finished.data),
            end_date=datetime.datetime.now() if add_form.is_finished.data else None,
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect("/")
    return render_template('add_job.html', title='Добавить работу', form=add_form)


def seed_db():
    session = db_session.create_session()

    def get_or_create_user(*, email: str, surname: str, name: str, age: int,
                           position: str, speciality: str, address: str, password: str) -> User:
        user = session.query(User).filter(User.email == email).first()
        if user:
            return user

        user = User(
            surname=surname,
            name=name,
            age=age,
            position=position,
            speciality=speciality,
            address=address,
            email=email,
        )
        user.set_password(password)
        session.add(user)
        try:
            session.commit()
        except IntegrityError:
            # Under Flask debug reloader two processes can race on the first run.
            session.rollback()
        return session.query(User).filter(User.email == email).first()

    scott = get_or_create_user(
        email="scott_chief@mars.org",
        surname="Scott",
        name="Ridley",
        age=21,
        position="captain",
        speciality="research engineer",
        address="module_1",
        password="cap",
    )
    get_or_create_user(
        email="durov@tg.com",
        surname="Durov",
        name="Pavel",
        age=42,
        position="CEO",
        speciality="engineer",
        address="module_3",
        password="durov",
    )

    if session.query(Jobs.id).first() is not None:
        return

    team_leader_id = scott.id if scott else 1
    for i, job_title in enumerate(["ремонт", "исследование", "готовка пищи"]):
        session.add(Jobs(
            team_leader=team_leader_id,
            job=job_title,
            work_size=i + 1,
            collaborators="",
            start_date=datetime.datetime.now(),
            is_finished=False,
        ))
    session.commit()


def main():
    db_session.global_init("db/mars_explorer.db")
    app.run(debug=True)
    seed_db()
        

if __name__ == '__main__':
    main()
