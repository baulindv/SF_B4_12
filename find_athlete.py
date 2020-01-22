import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()


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


class Athlete(Base):
    """
    Описывает структуру таблицы athlete для доступа к данным атлетов
    """
    __tablename__ = 'athelete'
    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.DATE)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)


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


session = connect_db()


def check_user_input():
    """
    Проверяет что введено правильное число и возвращает его
    """
    while True:
        user_id = input('Введите идентификатор пользователя для поиска: ')
        try:
            user_id = int(user_id)
            break
        except ValueError:
            print('Необходимо ввести число!')
    return user_id


def find():
    user_id = check_user_input()
    # session = connect_db()
    query = session.query(User).filter(User.id == user_id)
    if query.count() != 1:
        print('Пользователя с таким идентификатором не существует.')
        return
    user = query.first()
    user_birthdate = user.birthdate
    user_height = user.height
    print(f'Дата рождения выбранного пользователя: {user_birthdate}\n'
          f'Рост выбранного пользователя: {user_height}')
    # Список найденных атлетов
    athletes = [select_near_athlete('birthdate', user_birthdate), select_near_athlete('height', user_height)]
    print('-' * 50)
    print('Найденные атлеты, ближайшие по дате рождения(1) и росту(2):')
    for ath in athletes:
        print(f'Идентификатор: {ath.id}\n'
              f'Имя: {ath.name}\n'
              f'Дата рождения: {ath.birthdate}\n'
              f'Возраст: {ath.age}\n'
              f'Пол: {ath.gender}\n'
              f'Рост: {ath.height}\n'
              f'Вес: {ath.weight}\n'
              f'Вид спорта: {ath.sport}\n'
              f'Страна: {ath.country}\n'
              f'Число золотых медалей: {ath.gold_medals}\n'
              f'Число серебрянных медалей: {ath.silver_medals}\n'
              f'Число бронзовых медалей: {ath.bronze_medals}\n'
              f'Общее число медалей: {ath.total_medals}\n')


def select_near_athlete(criteria, search_value):
    """
    Ищет атлета, максимально близкого по росту или дате рождения, в зависимости от того, что передаётся в функцию
    """
    # В зависимости от переданного аргумента искать по росту или дате рождения
    if criteria == 'height':
        criteria = Athlete.height
    elif criteria == 'birthdate':
        criteria = Athlete.birthdate

    # Сначала искать точное совпадение, затем того, кто выше и ниже
    query_eq = session.query(Athlete).filter(criteria == search_value).first()
    if query_eq:
        athlete = query_eq
    else:
        query_gt = session.query(Athlete).filter(criteria > search_value).order_by(criteria).first()
        if query_gt:
            athlete = query_gt
        else:
            query_lt = session.query(Athlete).filter(criteria < search_value).order_by(criteria.desc()).first()
            athlete = query_lt
    return athlete


def main():
    find()


if __name__ == '__main__':
    main()
