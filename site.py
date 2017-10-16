from flask import Flask, request, render_template, redirect, url_for
import json
import urllib2
import requests

app = Flask(__name__)
api_url="http://127.0.0.1:4000/"

@app.route("/")
def home():
    paises = json.loads(urllib2.urlopen(api_url+"paises").read())
    return render_template("index.html", paises = paises['paises'])

@app.route("/cidades/", methods=["GET"])
def get():
    if request.method == "GET":
        cidades = json.loads(urllib2.urlopen(api_url+"cidades/"+request.args['pais']).read())
        return render_template("cidades.html", cidades = cidades['cidades'])


@app.route("/addcidade")
def addcidade():
    paises = json.loads(urllib2.urlopen(api_url+"paises").read())
    return render_template("addcidade.html", codes = paises['paises'])

@app.route("/newcity/", methods=["POST"])
def post():
    if request.method == "POST":
        dic = {
            "Name"          : request.form['Name'],
            "CountryCode"   : request.form['CountryCode'],
            "District"      : request.form['District'],
            "Population"    : request.form['Population'],
        }
        res = requests.post(api_url+"cidades", params=dic)
        paises = json.loads(urllib2.urlopen(api_url+"paises").read())
        return render_template("index.html", paises = paises['paises'])

@app.route("/rmcidade")
def rmcidade():
    cidades = json.loads(urllib2.urlopen(api_url+"cidades").read())
    return render_template("rmcidade.html", cidades = cidades['cidades'])

@app.route("/delcity/", methods=["POST"])
def delete():
    if request.method == "POST":
        res = requests.delete(api_url+"cidades/"+request.form["ID"])
        paises = json.loads(urllib2.urlopen(api_url+"paises").read())
        return render_template("index.html", paises = paises['paises'])

@app.route("/attcidade")
def attcidade():
    return render_template("attcidade.html")

@app.route("/upcity/", methods=["POST", "GET"])
def path():
    if request.method == "POST":
        dic = {
            "Name"          : request.form['Name'],
            "CountryCode"   : request.form['CountryCode'],
            "District"      : request.form['District'],
            "Population"    : request.form['Population'],
            "ID"            : request.form['ID'],
        }
        res = requests.patch(api_url+"cidades", params=dic)
        paises = json.loads(urllib2.urlopen(api_url+"paises").read())
        return render_template("index.html", paises = paises['paises'])


if __name__ == '__main__':
    app.run("127.0.0.1", port=2000, debug=True)
