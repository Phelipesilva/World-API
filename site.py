from flask import Flask, request, render_template, redirect, url_for
import json
import urllib2

app = Flask(__name__)
api_url="http://127.0.0.1:5000/"

@app.route("/")
def home():
    paises = json.loads(urllib2.urlopen(api_url+"paises").read())
    return render_template("index.html", paises = paises['paises'])

@app.route("/cidades/", methods=["POST", "GET"])
def get():
    if request.method == "POST":
        cidades = json.loads(urllib2.urlopen(api_url+"cidades/"+request.form['pais']).read())
        return render_template("cidades.html", cidades = cidades['cidades'])

if __name__ == '__main__':
    app.run("127.0.0.1", port=3000, debug=True, )
