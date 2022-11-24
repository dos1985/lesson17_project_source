# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app. config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 2}
db = SQLAlchemy(app)

api = Api(app)
moves_ns = api.namespace('movies')
director_id = api.namespace('director')
genre_id = api.namespace('genre')


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")

class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

"""возвращает список всех фильмов, разделенный по страницам;"""
@moves_ns.route('/')
class MovesView(Resource):
    def get(self):
        movies = Movie.query.all()
        return movies_schema.dump(movies), 200


    def post(self):
        movie = movie_schema.load(request.json)
        db.session.add(Movie(**movie))
        db.session.commit()
        return "", 201


"""возвращает подробную информацию о фильме."""
@moves_ns.route('/<int:nid>')
class MoveView(Resource):
    def get(self, nid):
        movie = Movie.query.get(nid)
        return movie_schema.dump(movie), 200

    def put(self, nid):
        db.session.query(Movie).filter(Movie).update(request.json)
        db.session.commit()

        return "", 204


"""возвращает только фильмы с определенным режиссером по запросу типа"""
@director_id.route('/<int:nid>')
class DirectorsView(Resource):
    def get(self, nid):
        director = Movie.query.get(nid)
        return movie_schema.dump(director), 200


"""возвращает только фильмы определенного жанра  по запросу типа"""
@genre_id.route('/<int:nid>')
class GenresView(Resource):
    def get(self, nid):
        genre = Movie.query.get(nid)
        return movie_schema.dump(genre), 200





if __name__ == '__main__':
    app.run(debug=True)

