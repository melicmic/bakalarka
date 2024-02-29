from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from database import db_session, engine
from core import search_bar

"""class ObDevice():
    def __init__(self, id_zar, zar_nazev, zar_seriove, zar_model, zar_nakup, zar_poznm, fk_kat, fk_vyr):
            self.id = id_zar
            self.nazev = zar_nazev
            self.sc = zar_seriove
            self.model = zar_model
            self.nakup = zar_nakup
            self.poznm = zar_poznm
            self.kat = fk_kat
            self.vyr = fk_vyr"""


main_bp = Blueprint("main", __name__)#, static_folder="static", template_folder="templates")

@main_bp.route("/", methods=["GET", "POST"])
@main_bp.route("/home", methods=["GET", "POST"])
def home():
        if int(session.get("pravo")) == 1:
                pravo=True
        else:
                pravo=False
        if request.method == "POST":
                print("main.py | home() >>> čtu z vyhledávacího formuláře")
                text_pole = request.form["search"]
                combo_pole = request.form["category"]

                return redirect(url_for("main.searching", tp = text_pole, cp = combo_pole))
        else:
                print("++ main.py | home() >> > načtení úvodní stránky")
                y=0
                x=0  
                return render_template("main/home.html", x=x, y=y, pravo=pravo)
        
@main_bp.route("/searching", methods=["GET", "POST"])
def searching():
        if request.method == "POST":
                print("tlačítko pro edit")
                akce = int(request.form["selected_id"])
                print(type(akce))
                return redirect(url_for("news.device", akce=akce))

        else: # "GET"
                print("++ main.py | searching() >>> vyhledávám v DB podle kritériích")
                text_pole = request.args.get('tp')
                combo_pole = request.args.get('cp')
                result = search_bar(text_pole, combo_pole)
                db_session.close() # nutný, jinak to padne při dalším validním dotazu
                if (result is not None):
                        if result is not False:
                                zarizeni, vyrobce, kategorie = result  # Rozbalení výsledku (při dotazu .all()) do jednotlivých proměnných, pak lze volat vyrobce.vyr_nazev atp
                                return render_template("result/search.html", zar=zarizeni, kat=kategorie, vyr=vyrobce)   
                        else:
                                print("chybný formát v search baru")
                                return render_template("main/error.html", e="DataError: Chybný formát. Vyhledávání podle \"Inventární číslo\" musí být datového typu int()")
                else:
                        nabidka=["Inventární číslo", "Sériové číslo", "Doménové jméno", "ID uživatele", "Uživatele"]
                        return render_template("main/error.html", e=f"Nenalezl jsem žádný záznam pro {text_pole} v {nabidka[int(combo_pole)]}.")

  
