import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm as orm
import sqlalchemy

from sqlalchemy.orm import Session

SqlAlchemyBase = dec.declarative_base()


class DataBase:
    def __init__(self, db_file):
        self.factory = None
        self.main_init(db_file)

    def main_init(self, db_file):
        if self.factory:
            return
        conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
        engine = sqlalchemy.create_engine(conn_str, echo=False)
        self.factory = orm.sessionmaker(bind=engine)
        SqlAlchemyBase.metadata.create_all(engine)

    def create_session(self) -> Session:
        return self.factory()

    def create_user(self, user_id):
        session = self.create_session()
        if session.query(User).filter(User.id == user_id).first() is None:
            user = User(user_id)
            session.add(user)
            session.commit()
            return True
        return False

    def subscribe(self, user_id):
        session = self.create_session()
        user = session.query(User).filter(User.id == user_id).first()
        if user is not None:
            user.mode = True
            session.commit()

    def unsubscribe(self, user_id):
        session = self.create_session()
        user = session.query(User).filter(User.id == user_id).first()
        if user is not None:
            user.mode = False
            session.commit()

    def return_users(self):
        session = self.create_session()
        users = session.query(User).filter(User.mode == 1).all()
        return list(map(lambda user: user.id, users))

    def create_news(self, name):
        session = self.create_session()
        if session.query(News).filter(News.name == name).first() is None:
            news = News(name)
            session.add(news)
            session.commit()

    def len_news(self):
        session = self.create_session()
        news = session.query(News).all()
        return len(news)

    def del_news(self):
        session = self.create_session()
        session.query(News).delete()
        session.commit()

    def return_news(self):
        session = self.create_session()
        all_news = session.query(News).all()
        return list(map(lambda news: news.name, all_news))


class User(SqlAlchemyBase):
    __tablename__ = "users"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, nullable=False)
    mode = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    view = sqlalchemy.Column(sqlalchemy.Text, nullable=False)

    def __init__(self, user_id):
        self.id = int(user_id)
        self.mode = True
        self.view = "User"


class News(SqlAlchemyBase):
    __tablename__ = "news"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    name = sqlalchemy.Column(sqlalchemy.Text, nullable=False)

    def __init__(self, name):
        self.name = name
