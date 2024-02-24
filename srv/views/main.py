# zobrazí základní akce podle oprávnění
# zobrazí přehled zařízeních
# zobrazí vyheldávání
# barva bude červená
from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from sqlalchemy import select

from database import db_session, Lokace, Budova

main_bp = Blueprint("main", __name__)#, static_folder="static", template_folder="templates")


@main_bp.route("/home", methods=["GET", "POST"])
def home():
        if request.method == "POST":
                print("main.py ---- čtu z formuláře")
                text_pole = request.form["search"]
                combo_pole = request.form["category"]
                print(f"textové {text_pole} a combo {combo_pole}")
                return redirect(url_for("main.dotaz", tp = text_pole, cp = combo_pole))
        else:
                print("to druhé")
                #combo_pole = request.form["category"]
                #print(f"textové {text_pole} a combo {combo_pole}")   
                return render_template("main.html")
        
@main_bp.route("/dotaz")
def dotaz():
        print("tisknu v dotazu")
        text_pole = request.args.get('tp')
        print(text_pole)
        
        combo_pole = request.args.get('cp')
        print(combo_pole)

        #search_bar(uzv)

        return render_template("search.html", uzv=combo_pole, hsl=text_pole)

@main_bp.route("/odhlaseni")
def odhlaseni():
        session.clear()
        return redirect(url_for("login.logout"))



