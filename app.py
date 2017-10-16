from flask import Flask, request, render_template, redirect, url_for
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from json import dumps
import json

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('ID')
parser.add_argument('Name')
parser.add_argument('CountryCode')
parser.add_argument('District')
parser.add_argument('Population')

#dialect+driver://username:password@host:port/database
engine = create_engine("mysql+mysqlconnector://root:@127.0.0.1:3306/world")

class paises(Resource):
    def get(self):
        conn = engine.connect()
        query = conn.execute("SELECT * FROM country")
        return {"paises" : [dict(zip(tuple(query.keys()), i))for i in query.cursor]}

class cidades(Resource):
    def get(self):
        conn = engine.connect()
        query = conn.execute("SELECT * FROM city")
        return {"cidades" : [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
    def post(self):
        args = parser.parse_args()
        conn = engine.connect()
        query = conn.execute("INSERT INTO city(ID, Name, CountryCode, District, Population)\
        VALUES(null, '%s', '%s', '%s', %d)" %(args['Name'],args['CountryCode'],args['District'],int(args['Population'])))
        return args
    def patch(self):
        args = parser.parse_args()
        conn = engine.connect()
        query = conn.execute("UPDATE city SET Name='%s', CountryCode='%s', District='%s', Population='%d' WHERE ID = %d"
        %( args['Name'], args['CountryCode'], args['District'], int(args['Population']), int(args['ID'])))
        return "UPDATED"

class cidades_pais(Resource):
    def get(self, code):
        conn = engine.connect()
        query = conn.execute("SELECT * FROM city WHERE CountryCode = '%s'" %code.upper())
        return {"cidades" : [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
    def delete(self, code):
        conn = engine.connect()
        query = conn.execute("DELETE FROM city WHERE ID = %d" %(int(code)))
        return "DELETED"

class linguas(Resource):
    def get(self):
        conn = engine.connect()
        query = conn.execute("SELECT * FROM countrylanguage")
        return {"linguas" : [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}

api.add_resource(paises, "/paises")
api.add_resource(cidades, "/cidades")
api.add_resource(cidades_pais, "/cidades/<code>")
api.add_resource(linguas, "/linguas")

if __name__ == '__main__':
    app.run("127.0.0.1", port=4000, debug=True)
