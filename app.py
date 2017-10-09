from flask import Flask, request, render_template, redirect, url_for
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import json

app = Flask(__name__)
api = Api(app)

#dialect+driver://username:password@host:port/database
engine = create_engine("mysql+mysqlconnector://root:@127.0.0.1:3306/world")

class paises(Resource):
    def get(self):
        conn = engine.connect()
        query = conn.execute("SELECT * FROM country")
        return {"paises" : [i[0] for i in query.cursor.fetchall()]}

class cidades(Resource):
    def get(self, code):
        conn = engine.connect()
        query = conn.execute("SELECT * FROM city WHERE CountryCode = '%s'" %code.upper())
        return {"cidades" : [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}

class linguas(Resource):
    def get(self, code):
        conn = engine.connect()
        query = conn.execute("SELECT * FROM countrylanguage WHERE CountryCode = '%s'" %code.upper)
        return {"linguas" : [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}


api.add_resource(paises, "/paises")
api.add_resource(cidades, "/cidades/<string:code>")

if __name__ == '__main__':
    app.run()
