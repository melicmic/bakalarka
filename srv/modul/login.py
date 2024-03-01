# hlavní stránka po načtení, nějaké plky o čem to je
# povede na tří další části podle oprávnění 
# 1 > full controll
# 2 > omezený přístup, jen prohlížení a vyhledávání
# 3 > error page, přístup odmítnut; spolu s neplatnými pokusy

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from database import db_session, engine, Uzivatel


login_bp = Blueprint("login", __name__)#, static_folder="static", template_folder="templates")


@login_bp.route("/", methods=["GET", "POST"])
#@login_bp.route('/login', methods=["GET", "POST"])
def index():
        if "uzivatel" in session:
            print(session.get("uzivatel"))
            return redirect(url_for("main.home"))
        else:
            if request.method == "POST":
                print("++ login.py | index() >>> čtení z formuláře")
                uzivatel = request.form["username"]
                heslo = request.form["password"]
                dotaz = db_session.query(Uzivatel).filter_by(uziv_kod=uzivatel).one_or_none()
                db_session.close()
                if dotaz==None:
                    print("vráceno NONE ... nenašel se v db")
                    return render_template("main/error.html")
                elif (dotaz.uziv_kod==uzivatel and dotaz.uziv_heslo==heslo):
                    print("++ login.py | index() >>> uživatel je ověřen")
                    session["uzivatel"] = uzivatel
                    session["pravo"]  = dotaz.fk_opr
                    return redirect(url_for("main.home"))
                else:
                    print("++ login.py | index() >>> neplatný vstup")
                    return render_template("main/error.html")
            
            else:
                print("++ login.py | index() >>> Přihlašovací stránka (default)")
                return render_template("index.html")



@login_bp.route("/edit")
def edit():
    print("transakce")
    return render_template("main/error.html", e="<h1>upravit uživatelům profil</h1>")

@login_bp.route("/logout")
def logout():
        session.clear()
        engine.dispose()
        print(f"++ main.py | logout() >>> Uživatel odhlášen --|==|-- {engine.pool.status()}")
        return redirect(url_for("login.index"))
     