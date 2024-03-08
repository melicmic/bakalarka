from flask import Blueprint, session
from flask import request, render_template, redirect, url_for
from sqlalchemy import and_, select, update, insert

from core import my_role, status_list, uzivatel_list, lokace_list, kratke_datum, dlouhe_datum, edit_list, relocation_listing
from database import db_session, Transakce

edit_bp = Blueprint("edit", __name__)#, static_folder="static", template_folder="templates")



def write_change(id, lok, status, date, popis, user, zar):
        print("jsem uvnitr")
        print(id, lok, status, date, popis, user)
        #zapsani = Transakce(tran_platnost_od=dlouhe_datum(), tran_editace=dlouhe_datum(), tran_poznamka = popisek, fk_uziv=x, fk_zar=input.id_zar, fk_lok=2, fk_stat=1)
        print(type(lok))
        with db_session as ssn:
              with ssn.begin():
                        update_stmt = (update(Transakce).where((Transakce.id_tran == id) & (Transakce.tran_platnost_do == None))
                                .values(
                                tran_platnost_do=date,
                                tran_editace=dlouhe_datum()
                        ))
                        ssn.execute(update_stmt)
                        insert_stmt = (insert(Transakce).values(tran_platnost_od=kratke_datum(), tran_editace=dlouhe_datum(), 
                                                                tran_poznamka = popis, fk_uziv=user, fk_zar=zar, fk_lok=lok, fk_stat=status))
                        
                        ssn.execute(insert_stmt)

                        

@edit_bp.route("listing", methods=["GET", "POST"])
def listing():
    pravo = my_role()
    print("++ news.py | relocation() - vytvoření nového uživatele")
    k=lokace_list()

    if request.method == "POST":
        button_name = request.form.get('button_name')
        if button_name == "search":
            print("++ kam se propadnu? čtu vstupy z formuláře")
            id_lok = request.form["location"]
            vypis = relocation_listing(int(id_lok))
            if vypis == []:
                print("je noneneoneoe")
            #print(selected_id)
            return render_template("edit/listing.html", dotaz=vypis, k=k, pravo=pravo, hledane=id)

        elif button_name == "discard":
            id_e_lok = request.form.getlist('zaskrt')
            session["edit"] = id_e_lok
            return redirect(url_for("edit.writing", akce="rip"))
        elif button_name == "move":
            id_e_lok = request.form.getlist('zaskrt')
            session["edit"] = id_e_lok
            return redirect(url_for("edit.writing"))

    else:
        print("první načtení")
        id_lok = 2
        selected_id = 2
        vypis = relocation_listing(int(id_lok))
        return render_template("edit/listing.html", dotaz=vypis, k=k, pravo=pravo,  hledane=selected_id)




@edit_bp.route("/", methods=["GET", "POST"])
@edit_bp.route("/<string:akce>", methods=["GET","POST"])
def writing(akce=False):
        pravo = my_role()
        stat= status_list(None)
        uziv = uzivatel_list(None)
        lok = lokace_list()
        print("++ edit.py | change() >> > načtení úvodní stránky")
        nacist = session.get("edit")

        if request.method == "POST":
                new_date = request.form.getlist("datum[]")
                old_id = request.form.getlist("id_tran[]")
                inv = request.form.getlist("inv[]")
                new_lok = request.form.getlist("new_lok[]")
                new_status = request.form.getlist("new_status[]")
                new_popis = request.form.getlist("popis[]")
                actual_date = kratke_datum()
                for i in new_date: # ověříme datum
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
                return render_template("main/error.html", e="Vyřazujeme či co")
        else:
                vystup = edit_list(nacist)
                if akce == "rip":
                        return render_template("edit/edit_discard.html", result=vystup, status=stat, uziv=session.get("uzivatel"), lok=lok, datum=kratke_datum(), pravo=pravo)
                else:
                        return render_template("edit/edit.html", result=vystup, status=stat, uziv=uziv, lok=lok, datum=kratke_datum(), pravo=pravo)