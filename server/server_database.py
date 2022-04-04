from sqlalchemy import create_engine, Table, Column, Integer, MetaData, DateTime, Float
from sqlalchemy.orm import mapper, sessionmaker
from variables import *
import datetime


# Класс - серверная база данных:
class ServerStorage:
    # Класс - отображение таблицы Points
    class PointsView:
        def __init__(self, device_id, latitude, longitude):
            self.point_id = None
            self.device_id = device_id
            self.point_time = datetime.datetime.now()
            self.latitude = latitude
            self.longitude = longitude

    def __init__(self, path):
        # Создаём движок базы данных
        print(path)
        self.database_engine = create_engine(f'sqlite:///{path}', echo=False, pool_recycle=7200,
                                             connect_args={'check_same_thread': False})

        # Создаём объект MetaData
        self.metadata = MetaData()

        # Создаём таблицу points
        points_table = Table('Points', self.metadata,
                             Column('point_id', Integer, primary_key=True),
                             Column('device_id', Integer, unique=True),
                             Column('point_time', DateTime),
                             Column('latitude', Float),
                             Column('longitude', Float),
                             )

        # Создаём таблицы
        self.metadata.create_all(self.database_engine)

        # Создаём отображения
        mapper(self.PointsView, points_table)

        # Создаём сессию
        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()
        self.session.commit()

    # Функция выполняющаяся при входе пользователя, записывает в базу факт входа
    def add_point(self, device_id, latitude, longitude):
        point = self.PointsView(device_id, latitude, longitude)
        self.session.add(point)
        # Коммит здесь нужен, чтобы присвоился ID
        self.session.commit()