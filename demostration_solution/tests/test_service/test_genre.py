from unittest.mock import MagicMock

import pytest

from dao.model.genre import Genre
from dao.genre import GenreDAO
from service.genre import GenreService
from setup_db import db


#фикстура по genre_dao
@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(db.session)

#фальшивые данные для имитации работы БД
    action = Genre(id=1, name='action')
    comedy = Genre(id=2, name='comedy')
    thriller = Genre(id=3, name='thriller')

#имитация методов DAO на основе фальшивых данных
    genre_dao.get_one = MagicMock(return_value=action)
    genre_dao.get_all = MagicMock(return_value=[action, comedy, thriller])
    genre_dao.create = MagicMock(return_value=Genre(id=3, name='Horror'))
    genre_dao.delete = MagicMock()
    genre_dao.update = MagicMock()

    return genre_dao


#Тесты TestGenreService (подставляем фикстуру genre_dao) тестируем методы dao
#Даже если тесты в другом файле, фикстуру genre_dao не нужно импортировать, потому что pytest ее узнает
#autouse=True - для того, чтобы все тесты в этом классе по умолчанию использовали эту фикстуру
#в методе test_update прописывать assert не нужно (главное, чтобы тест не упал)
class TestGenreService:
   @pytest.fixture(autouse=True)
   def genre_service(self, genre_dao):
       self.genre_service = GenreService(dao=genre_dao)

   def test_get_one(self):
       genre = self.genre_service.get_one(1)
       assert genre is not None
       assert genre.id == 1

   def test_get_all(self):
       genres = self.genre_service.get_all()
       assert len(genres) == 3
       assert len(genres) > 0

   def test_create(self):
       genre_data = {
           'name': 'Horror'
       }
       genre = self.genre_service.create(genre_data)
       assert genre.name == genre_data['name']

   def test_delete(self):
       genre = self.genre_service.delete(1)
       assert genre is None

   def test_update(self):
       genre_data = {'id': 3, 'name': 'Arthouse'}
       self.genre_service.update(genre_data)
