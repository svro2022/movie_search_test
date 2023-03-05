from unittest.mock import MagicMock

import pytest

from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService
from setup_db import db


#фикстура по movie_dao
@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(db.session)

#фальшивые данные для имитации работы БД
    scary_movie1 = Movie(
        id=1,
        title='scary_movie1',
        description='description1',
        trailer='trailer1',
        year=1991,
        rating=2,
        genre_id=1,
        director_id=1,
    )
    scary_movie2 = Movie(
        id=2,
        title='scary_movie2',
        description='description2',
        trailer='trailer2',
        year=1992,
        rating=2,
        genre_id=2,
        director_id=2,
    )
    scary_movie3 = Movie(
        id=3,
        title='scary_movie3',
        description='description3',
        trailer='trailer3',
        year=1993,
        rating=2,
        genre_id=3,
        director_id=3,
    )

#имитация методов DAO на основе фальшивых данных
    movie_dao.get_one = MagicMock(return_value=scary_movie1)
    movie_dao.get_all = MagicMock(return_value=[scary_movie1, scary_movie2, scary_movie3])
    movie_dao.create = MagicMock(return_value=Movie(id=3, title='Mummy'))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()

    return movie_dao


#Тесты TestDirectorService (подставляем фикстуру director_dao) тестируем методы dao
#Даже если тесты в другом файле, фикстуру director_dao не нужно импортировать, потому что pytest ее узнает
#autouse=True - для того, чтобы все тесты в этом классе по умолчанию использовали эту фикстуру
#в методе test_update прописывать assert не нужно (главное, чтобы тест не упал)
class TestMovieService:
   @pytest.fixture(autouse=True)
   def movie_service(self, movie_dao):
       self.movie_service = MovieService(dao=movie_dao)

   def test_get_one(self):
       movie = self.movie_service.get_one(1)
       assert movie is not None
       assert movie.id == 1
       assert movie.title == 'scary_movie1'

   def test_get_all(self):
       movies = self.movie_service.get_all()
       assert len(movies) == 3
       assert len(movies) > 0

   def test_create(self):
       movie_data = {
           'title': 'Mummy'
       }
       movie = self.movie_service.create(movie_data)
       assert movie.title == movie_data['title']

   def test_delete(self):
       movie = self.movie_service.delete(1)
       assert movie is None

   def test_update(self):
       movie_data = {'id': 3, 'title': 'LOTR'}
       self.movie_service.update(movie_data)
