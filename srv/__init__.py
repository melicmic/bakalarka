from flask import Flask
from flask import request, render_template, redirect, url_for, session

import psycopg2

from database import Uzivatel, Vyrobce, Zarizeni, Status, Kategorie, Budova, Lokace, Opravneni, Vztah, Transakce
from database import vytvoreni_ddl#, odkomentovat Base, engine
from database import naplneni_dat

def create_app():
    app = Flask(__name__)
    app.secret_key = 'TAJNY_KLIC'

    vytvoreni_ddl()
    #Base.metadata.create_all(engine) # odkomentovat

    @app.route('/')
    def uvodni_stranka():
        print("ahoj")
        return render_template("index.html")


    @app.route("/demo_data")
    def demo_data():
        print("vložení statických dat")
        naplneni_dat()
        return "<h1>Naplnění demo dat</h1>"


    @app.route('/login', methods=["GET", "POST"])
    def prihlaseni():
        if request.method == "POST":
            print("čtu z formuláře")
            uzivatel = request.form["username"]
            heslo = request.form["password"]

            session["uzivatel"] = uzivatel
            session["heslo"] = heslo

            #dotaz = ss.query(Uzivatel).f

            return redirect(url_for("overen"))
        else:
            print("Přihlašovací stránka")
            return render_template("prihlaseni.html")

    @app.route("/overen")
    def overen():
        print("sessions:")
        print(session.get("uzivatel",None))
        return render_template("overen.html", uzv=session.get("uzivatel",None), hsl=session.get("heslo",None))

    return app

