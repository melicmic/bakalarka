from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from database import db_session
from core import search_bar, my_role, device_listing, transaction_listing, user_listing

main_bp = Blueprint("main", __name__)#, static_folder="static", template_folder="templates")

@main_bp.route("/", methods=["GET", "POST"])
@main_bp.route("/home", methods=["GET", "POST"])
def home():
        pravo = my_role()
        if request.method == "POST":
                print("main.py | home() >>> čtu z vyhledávacího formuláře")
                text_pole = request.form["search"].upper()
                combo_pole = request.form["category"]

                return redirect(url_for("main.searching", tp = text_pole, cp = combo_pole))
        else:
                print("++ main.py | home() >> > načtení úvodní stránky")
                return render_template("main/home.html", pravo=pravo)
        
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
                result, result2 = search_bar(text_pole, combo_pole)
                db_session.close() # nutný, jinak to padne při dalším validním dotazu
                if (result is not None):
                        if result is not False:
                                session["edit"] = [result2.Zarizeni.zar_inv]
                                print(session.get("edit"))                    
                                return render_template("result/search.html", dotaz=result, dotaz2=result2)   
                        else:
                                print("chybný formát v search baru")
                                return render_template("main/error.html", e="DataError: Chybný formát. Vyhledávání podle \"Inventární číslo\" musí být datového typu int()")
                else:
                        nabidka=["Inventární číslo", "Sériové číslo", "Doménové jméno", "ID uživatele", "Uživatele"]
                        return render_template("main/error.html", e=f"Nenalezl jsem žádný záznam pro {text_pole} v {nabidka[int(combo_pole)]}.")

@main_bp.route("records", methods=["GET","POST"], defaults={"id": None, "cp": None})
@main_bp.route("records/<int:id>/<int:cp>", methods=["GET","POST"])
def records(id, cp):
    pravo = my_role()
    if request.method == "POST":
        text_pole_t = request.form["tr_search"]
        combo_pole_t = request.form["tr_category"]      
        print(combo_pole_t)       
        vypis= transaction_listing(text_pole_t,combo_pole_t,y=None)
        return render_template("result/records.html", dotaz=vypis, hledane=text_pole_t, pravo=pravo)                               
    else: # GET
        if id == None:
            print("++ main.py | records() - vypsání transakcí (id=none)")
            vypis= transaction_listing(text_pole=id, combo_pole_t=11)
            db_session.close()
            return render_template("result/records.html", dotaz=vypis, hledane=None, pravo=pravo)
        else:
            print(f"předané id je {id} a {cp}")
            if cp is None:
                   cp=10
            vypis= transaction_listing(text_pole=id, combo_pole_t=cp)
            print("++ main.py | records() - zapsání transakce")
            db_session.close()
            return render_template("result/records.html", dotaz=vypis, hledane=id, pravo=False)   


@main_bp.route("inventory", methods=["GET", "POST"])
def inventory():
        pravo=my_role()
        if request.method == "POST":
                button_name = request.form.get('button_name')
                if button_name == "search":  
                        print("searchuji??")
                        text_pole_l = request.form["inv_search"]
                        combo_pole_l = request.form["category"]             
                        result=device_listing(text_pole_l,combo_pole_l)
                        return render_template("result/inventory.html", dotaz=result, hledane=text_pole_l, pravo=pravo)
                else: # kliknuto na Nový
                        return redirect(url_for("news.device"))             
        else:
                result=device_listing(None, 1)
                return render_template("result/inventory.html", dotaz=result, hledane=None, pravo=pravo)                       

@main_bp.route("participants", methods=["GET","POST"])#, defaults={"id": None})
def participants():
    pravo = my_role()
    print("++ main.py | user() - vypsání uživatelů")
    if request.method == "POST":
        button_name = request.form.get('button_name')
        if button_name == "search":       
                text_pole_u = request.form["us_search"]
                combo_pole_u = request.form["us_category"]      
                vypis= user_listing(text_pole_u,combo_pole_u)
                return render_template("result/participants.html", dotaz=vypis, pravo=pravo, hledane=text_pole_u, vybrane=int(combo_pole_u))
        elif button_name == "edit": 
               id = request.form["selected_id"]
               return redirect(url_for("edit.update_user", id=int(id)))
        elif button_name == "discard":
               id = request.form["selected_id"]
               return redirect(url_for("edit.discard_user", id=int(id)))
        else: # kliknuto na Nový
               return redirect(url_for("news.user"))
               
    else:
        vypis= user_listing(text_pole=None,combo_pole=0)
        db_session.close()
        text_pole_u=None
        return render_template("result/participants.html", dotaz=vypis, pravo=pravo, hledane=text_pole_u)