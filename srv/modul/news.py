from flask import Blueprint, render_template, redirect, request, url_for, session
from sqlalchemy.exc import IntegrityError

from database import db_session, Zarizeni, Kategorie
from core import kratke_datum, vyrobce_list, kategorie_list

news_bp = Blueprint("news", __name__)#, static_folder="static", template_folder="templates")

@news_bp.route("device", methods=["GET", "POST"])
def device():
    print("++ news.py | device() - vytvoření nového zařízení")
    if request.method == "POST":
        print("++ čtu vstupy z formuláře")
        input = Zarizeni(zar_inv = request.form["inv"],
                         zar_nazev = request.form["nazev"],
                         zar_seriove = request.form["seriove"],
                         zar_model = request.form["model"] ,
                         zar_nakup = request.form["nakup"],
                         zar_poznm = request.form["poznm"] ,
                         fk_kat = request.form["kat"],
                         fk_vyr  = request.form["vyr"]                       
                         )
        db_session.add(input) 
        try:
            db_session.commit()
        except IntegrityError as e:
            print(f"chyba při vkládání {e}")
            db_session.rollback() ##### nutnéééééééééééééééééééééééééééééééé
            return render_template("error.html", e=e)
        else:
            print("Zařízení založeno, trigger do transakce")
            db_session.close()
            return redirect(url_for("news.transaction"))

    else:
        print("první načtení")
        y=vyrobce_list()
        k=kategorie_list()

        return render_template("news/device.html", x=kratke_datum(), y=y, k=k)

@news_bp.route("transaction", methods=["GET","POST"])
def transaction():
    print("transakce")
    return "<h1>založena transakce?</h1>"
