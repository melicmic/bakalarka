from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from database import db_session, engine
from core import search_bar

main_bp = Blueprint("main", __name__)#, static_folder="static", template_folder="templates")


@main_bp.route("/home", methods=["GET", "POST"])
def home():
        if request.method == "POST":
                print("main.py | home() >>> čtu z vyhledávacího formuláře")
                text_pole = request.form["search"]
                combo_pole = request.form["category"]

                return redirect(url_for("main.dotaz", tp = text_pole, cp = combo_pole))
        else:
                print("++ main.py | home() >> > načtení úvodní stránky")  
                return render_template("main/home.html")
        
@main_bp.route("/dotaz")
def dotaz():
        print("++ main.py | dotaz() >>> vyhledávám v DB podle kritériích")
        text_pole = request.args.get('tp')
        combo_pole = request.args.get('cp')
        result = search_bar(text_pole, combo_pole)
        print(result)
        db_session.close()
        if result == False:
                print("chybný formát v search baru")
                return render_template("main/error.html", e="DataError: Chybný formát. Vyhledávání podle \"Inventární číslo\" musí být datového typu int()")
        elif result == None:
                nabidka=["Inventární číslo", "Sériové číslo", "Doménové jméno", "ID uživatele", "Uživatele"]
                return render_template("main/error.html", e=f"Nenalezl jsem žádný záznam pro {text_pole} v {nabidka[int(combo_pole)]}.")
        else:
                return render_template("result/search.html", uzv=text_pole, hsl=combo_pole)   

  






@main_bp.route("/device")
def device():
        print("++ main.py | new_device() - vytvoření nového zařízení")
        if int(session.get("pravo")) == 1: 
                print(" mám právo zapisovat")
                return redirect(url_for("news.device"))
        else:
                return redirect(url_for("main.home"))

@main_bp.route("/transaction")
def transaction():
        print("++ main.py | new_transaction() - vytvoření nového zařízení")
        if int(session.get("pravo")) == 1: 
                print(" mám právo zapisovat")
                return redirect(url_for("news.transaction"))
        else:
                return redirect(url_for("main.home"))
        
@main_bp.route("/user")
def user():
        print("++ main.py | new_user() - vytvoření nového zařízení")
        if int(session.get("pravo")) == 1: 
                print(" mám právo zapisovat")
                return redirect(url_for("news.transaction"))
        else:
                return redirect(url_for("main.home"))

@main_bp.route("/location")
def location():
        print("++ main.py | new_location() - vytvoření nového zařízení")
        if int(session.get("pravo")) == 1: 
                print(" mám právo zapisovat")
                return redirect(url_for("news.location"))
        else:
                return redirect(url_for("main.home"))        

@main_bp.route("/odhlaseni")
def odhlaseni():
        session.clear()
        engine.dispose()
        print(f"++ main.py | logout() >>> Uživatel odhlášen --|==|-- {engine.pool.status()}")
        return redirect(url_for("login.index"))



