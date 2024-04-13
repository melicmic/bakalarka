from flask import Blueprint, session
from flask import request, render_template, redirect, url_for
from sqlalchemy.exc import IntegrityError

from database import db_session
from core import (my_role, status_list, uzivatel_list, lokace_list, kategorie_list, vyrobce_list, vztah_list, opravneni_list, kratke_datum, edit_list, 
                  write_change, relocation_listing, load_device, db_update_device, load_user, db_update_user, db_discard_user)

task_bp = Blueprint("task", __name__)#, static_folder="static", template_folder="templates")
                        
# Záložka "Přehled podle lokacích" - první načtení je id_lok = 2 (IT SKLAD)
# Používá tlačítka Přesunout a Vyřadit. 
@task_bp.route("listing", methods=["GET", "POST"], defaults={"id_lok": 2}) 
@task_bp.route("listing/<int:id_lok>", methods=["GET", "POST"])
def listing(id_lok):
    pravo = my_role()
    print("++ news.py | relocation() - vytvoření nového uživatele")
    k=lokace_list()

    if request.method == "POST":
        button_name = request.form.get('button_name')
        if button_name == "search":
            print("++ kam se propadnu? čtu vstupy z formuláře")
            id_lok = request.form["location"]
            return redirect(url_for("task.listing", id_lok=id_lok))
        else:
                id_e_lok = request.form.getlist('zaskrt')
                if id_e_lok == []:
                        return redirect(url_for("task.listing", id=id_lok))
                elif button_name == "discard":
                        session["edit"] = id_e_lok
                        return redirect(url_for("task.writing", akce="rip"))
                elif button_name == "move":
                        id_e_lok = request.form.getlist('zaskrt')
                        session["edit"] = id_e_lok
                        return redirect(url_for("task.writing"))
                else:
                      print("Sem jsem se neměl dostat")
    else:
        print("první načtení")
        selected_id = 2
        if id_lok != 2:
               selected_id = id_lok                
        vypis = relocation_listing(int(id_lok))
        return render_template("task/listing.html", dotaz=vypis, k=k, pravo=pravo,  hledane=selected_id)


@task_bp.route("/move", methods=["GET", "POST"], defaults={"akce": None})
@task_bp.route("/move/<string:akce>", methods=["GET","POST"])
def writing(akce):
        pravo = my_role()
        stat= status_list(None)
        uziv = uzivatel_list(1)
        lok = lokace_list()
        print("++ task.py | change() >> > načtení úvodní stránky")
        nacist = session.get("edit")

        if request.method == "POST":
                new_date = request.form.getlist("datum[]")
                old_id = request.form.getlist("id_tran[]")
                inv = request.form.getlist("inv[]")
                new_lok = request.form.getlist("new_lok[]")
                new_status = request.form.getlist("new_status[]")
                new_popis = request.form.getlist("popis[]")
                actual_date = kratke_datum()
                for i in new_date: # ověříme datum, zda nezadáváme datum v budoucnosti
                        if i > actual_date:
                                return render_template("main/error.html", e=f"Dnes je {actual_date}. Nelze upravovat zápis s budoucím termínem platnosti. --> Chybně zvolené datum {i}")
                if akce == "rip": # tl. Vyřadit
                        print("jsem na vyřazení, nastavuji lokaci, status, uživatele ze sessiony")
                        new_user = [session.get("uzivatel")] * len(old_id) # list z přihlášeného uživatele
                        new_user = [1] * len(old_id) # lokace id_lok = 1 ; RIP
                else: # tl. Přesunout
                        new_user = request.form.getlist("new_user[]")

                for i in range(len(old_id)):
                        write_change(old_id[i], new_lok[i], new_status[i], new_date[i], new_popis[i], new_user[i], inv[i])
                vystup = edit_list(nacist)
                return redirect(url_for("task.listing", id_lok=int(new_lok[0])))
        else: # první načtení
                vystup = edit_list(nacist)
                print(akce)
                if akce == "rip":
                        return render_template("task/device_discard.html", result=vystup, status=stat, uziv=session.get("uzivatel"), lok=lok, datum=kratke_datum(), pravo=pravo)
                else:
                        return render_template("task/device_move.html", result=vystup, status=stat, uziv=uziv, lok=lok, datum=kratke_datum(), pravo=pravo)

                
# Oprave záznamu zařízení v Zarizeni_tab, po uspěšném zapsání je redirect zpět do searching
@task_bp.route("/update_device/<int:id>", methods=["GET", "POST"])
def update_device(id):
        pravo = my_role()
        k = kategorie_list()
        v = vyrobce_list()
        vystup = load_device(id)
        db_session.close()
        if request.method == "POST":
                same_inv = request.form["inv"]
                new_seriove = request.form["seriove"]
                new_model = request.form["model"]
                new_info = request.form["info"]
                new_kat = request.form["kat"]
                new_vyr = request.form["vyr"]
                try:
                        db_update_device(id, new_seriove, new_model, new_info, new_kat, new_vyr)
                except IntegrityError as e:
                        print(f"chyba při vkládání {e}")
                        return render_template("main/error.html", e=e)
                else:
                        print("Zařízení založeno, trigger do transakce")
                        db_session.close()
                        return redirect(url_for("main.searching", tp = same_inv, cp = 0))
        else:
              return render_template("task/device_update.html", result=vystup, k=k, v=v, pravo=pravo)


# Oprava záznamu zařízení v Uzivatel_tab, po uspěšném zapsání je redirect zpět do searching
@task_bp.route("/update_user/<int:id>", methods=["GET", "POST"])
def update_user(id):
        pravo = my_role()
        k = vztah_list()
        v = opravneni_list()
        vystup = load_user(id)
        if request.method == "POST":
                #id_uziv = request.form["id"]
                vystup.Uzivatel.uziv_jmeno = request.form["jmeno"]
                vystup.Uzivatel.uziv_prijemni = request.form["prijmeni"]
                vystup.Uzivatel.uziv_email = request.form["email"]
                vystup.Uzivatel.uziv_heslo = request.form["pswd"]
                vystup.Uzivatel.id_vzt = request.form["vzt"]
                vystup.Uzivatel.id_opr = request.form["opr"]
                try:
                        db_session.commit()
                        #db_update_user(id_uziv, new_jmeno, new_prijmeni, new_vzt, new_opr, new_heslo, new_email)
                except IntegrityError as e:
                        print(f"chyba při vkládání {e}")
                        db_session.rollback()
                        return render_template("main/error.html", e=e)
                else:
                        print("Zařízení založeno, trigger do transakce")
                        db_session.close()
                        return redirect(url_for("main.accounts", pravo=pravo))
        else: # GET, první načtení
                return render_template("task/user_update.html", result=vystup, k=k, v=v, pravo=pravo)
        

@task_bp.route("/discard_user/<int:id>", methods=["GET", "POST"])
def discard_user(id):
        pravo = my_role()
        vystup = load_user(id)
        if request.method == "POST":
                new_vystup = request.form["vystup"]
                if new_vystup > kratke_datum():
                        return render_template("main/error.html", e=f"Dnes je {kratke_datum()}. Nelze upravovat zápis s budoucím termínem platnosti. --> Chybně zvolené datum {new_vystup}")
                vystup.Uzivatel.uziv_vystup = new_vystup
                try:
                        db_session.commit()
                except IntegrityError as e:
                        print(f"chyba při vkládání {e}")
                        db_session.rollback()
                        return render_template("main/error.html", e=e)
                else:
                        print("Zařízení založeno, trigger do transakce")
                        db_session.close()
                        return redirect(url_for("main.accounts", pravo=pravo))
        else: # GET, první načtení
                if vystup.Uzivatel.uziv_vystup is not None: # tady lze vyřešit znovu zavedení uživatele (další endpoint? přidat podmínku do discard?)
                       x = vystup.Uzivatel.uziv_vystup
                       return render_template("main/error.html", e=f"Uživatel {vystup.Uzivatel.uziv_kod} byl vyřazen {x}")
                else:
                       x = kratke_datum()
                db_session.close()
                return render_template("task/user_discard.html", result=vystup,  x=x, pravo=pravo)