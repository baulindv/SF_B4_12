import re
from datetime import date

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# from faker import Faker
# from faker.providers import internet, date_time

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()


def gender_check():
    """
    Проверяет правильность вводимого пола, возвращает проверенное значение
    """
    while True:
        gender = input('Пол (м, m - мужской; ж, f - женский): ').lower()
        if gender in ['м', 'm']:
            gender = 'Male'
            break
        elif gender in ['ж', 'f']:
            gender = 'Female'
            break
        else:
            print('Неправильно указан пол!')
    return gender


def email_check():
    """
    Проверяет правильность формата вводимого email, возвращает проверенное значение
    """
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,})+$'

    while True:
        email = input('E-mail: ')
        if not re.match(regex, email):
            print('Неправильный формат e-mail адреса!')
        else:
            break
    return email


def range_check(param, min_number, max_number, dob=True):
    """
    Проверяет вводимые числа на правильность, возвращает проверенное значение
    """
    while True:
        if dob == True:
            val = input(f'{param} рождения (от {min_number} до {max_number}): ')
        else:
            val = input(f'{param} (от {min_number} до {max_number}): ')

        # Если не число - повторить ввод
        try:
            if dob == True:
                val = int(val)
            else:
                val = float(val)

            # Если число не находится в заданном диапазоне - повторить
            if val < min_number or val > max_number:
                print(f'Значение должно быть в диапазоне от {min_number} до {max_number}!')
            else:
                break
        except ValueError:
            print('Необходимо ввести число!')
    return val


class User(Base):
    """
    Описывает структуру таблицы user для хранения данных пользователей
    """
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.DATE)
    height = sa.Column(sa.REAL)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()


def request_data():
    """
    Запрашивает данные и сохранят в таблицу
    """
    print('Введите данные пользователя:')

    first_name = input('Имя: ')
    last_name = input('Фамилия: ')
    gender = gender_check()
    email = email_check()
    dob_day = range_check('Число', 1, 31)
    dob_month = range_check('Месяц', 1, 12)
    dob_year = range_check('Год', 1800, 2020)
    height = range_check('Рост в метрах', 1, 2.5, dob=False)

    # Для заполнения базы данных фейковыми значениями
    # fake = Faker()
    # first_name = fake.first_name()
    # last_name = fake.last_name()
    # gender = fake.random_element(elements=('Male', 'Female'))
    # email = fake.ascii_free_email()
    # birthdate = fake.date_between(start_date='-50y', end_date='today')
    # height = fake.pyfloat(right_digits=2, min_value=1, max_value=2)

    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=date(dob_year, dob_month, dob_day),
        # birthdate = birthdate,
        height=height
    )
    return user


def main():
    """
    Запускает скрипт в работу
    """
    session = connect_db()
    user = request_data()
    session.add(user)
    session.commit()
    print('Данные сохранены.')


if __name__ == '__main__':
    main()
