from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
from sqlalchemy import create_engine

import core.vytvoreni_schema 

app = Flask(__name__)

app.secret_key = 'TAJNY_KLIC'

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/evihaw", future=True)

core.vytvoreni_schema.vytvoreni_ddl(engine)


@app.route('/')
def uvodni_stranka():
    print("ahoj")
    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def prihlaseni():
    if request.method == "POST":
        print("čtu z formuláře")
        uzivatel = request.form["username"]
        heslo = request.form["password"]

        session["uzivatel"] = uzivatel
        session["heslo"] = heslo

        dotaz = session.query(Uzivatel).f

        return redirect(url_for("overen"))
    else:
        print("Přihlašovací stránka")
        return render_template("prihlaseni.html")

@app.route("/overen")
def overen():
    print("sessions:")
    print(session.get("uzivatel",None))
    return render_template("overen.html", uzv=session.get("uzivatel",None), hsl=session.get("heslo",None))

if __name__ == "__main__":
    app.run(debug=True)
