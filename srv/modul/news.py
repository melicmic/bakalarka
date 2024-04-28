from flask import Blueprint, render_template, redirect, request, url_for
from sqlalchemy.exc import IntegrityError

from database import db_session, Zarizeni, Lokace, Budova, Uzivatel, Kategorie, Vyrobce
from core import (kratke_datum, vyrobce_list, kategorie_list, lokace_list, budovy_list, tr_new_device, my_role, opravneni_list, vztah_list, 
                  db_update_kategory, db_update_manufacturer, db_update_building, db_update_location)

news_bp = Blueprint("news", __name__)#, static_folder="static", template_folder="templates")

@news_bp.route("device", methods=["GET", "POST"])
def device():
    pravo = my_role()
    if pravo is True:
        print("má právo provádět změny")
        print("++ news.py | device() - vytvoření nového zařízení")
        if request.method == "POST":
            print("++ čtu vstupy z formuláře")
            input = Zarizeni(zar_inv = request.form["inv"],
                            zar_seriove = request.form["seriove"].upper(),
                            zar_model = request.form["model"].capitalize(),
                            zar_nakup = request.form["nakup"],
                            zar_poznm = request.form["info"] ,
                            id_kat = request.form["kat"],
                            id_vyr  = request.form["vyr"]                       
                            )
            db_session.add(input) 
            #### opravit, padá to při duplikátní hodnotě, ale nevím proč???????
            try:
                db_session.commit()
            except IntegrityError as e:
                print(f"chyba při vkládání {e}")
                db_session.rollback() ##### nutnéééééééééééééééééééééééééééééééé
                return render_template("main/error.html", e=e)
            else:
                print("Zařízení založeno, trigger do transakce")
                poznamka = request.form["tran_popis"]
                zalozeni = tr_new_device(input,poznamka)
                id_tr = zalozeni.id_tran
                print(id_tr)
                db_session.close()
                return redirect(url_for("main.history", id=id_tr, cp=10))
        else:
            print("první načtení")
            y=vyrobce_list()
            k=kategorie_list()
            return render_template("news/device.html", x=kratke_datum(), y=y, k=k)

    else:
        return render_template("main/error.html", e="Nemáš právo na zapisování")


@news_bp.route("location", methods=["GET", "POST"])
def location():
    pravo = my_role()
    select_vypis=budovy_list()
    vypis = db_session.query(Lokace, Budova).join(Budova, Lokace.id_bud == Budova.id_bud).order_by(Budova.bud_nazev).all()
    print("++ news.py | location() - vytvoření nového zařízení")
    if request.method == "POST":
        print("++ čtu vstupy z formuláře")
        button_name = request.form.get('button_name')
        if button_name == "edit":
            id_lok = request.form["selected_id"]
            lok_kod  = request.form["lok_kod"] 
            lok_nazev  = request.form["lok_nazev"]   
            fk_bud = request.form["id_bud"]
            return render_template("news/location.html", rozbal=select_vypis, dotaz=vypis, pravo=pravo, edit_nazev=lok_nazev, edit_kod=lok_kod, edit_bud=int(fk_bud), chosen_id=int(id_lok))
        elif button_name == "save":
            id = request.form["pass_id"]
            new_kod = request.form["new_kod"]
            new_nazev = request.form["new_nazev"]
            new_fk_bud = request.form["id_bud"]
            try:
                db_update_location(id, new_kod, new_nazev, new_fk_bud)
            except IntegrityError as e:
                print(f"chyba při vkládání {e}")
                return render_template("main/error.html", e=e)
            else:
                print("Zařízení založeno, trigger do transakce")
                return redirect(url_for("news.location"))
        elif button_name == "cancel":
            return redirect(url_for("news.location"))
        else:
            input = Lokace(lok_kod = request.form["kod"].upper(),
                                lok_nazev = request.form["nazev"].capitalize(),
                                id_bud = int(request.form["id_bud"])            
                                )
            db_session.add(input) 

            try:
                db_session.commit()
            except IntegrityError as e:
                print(f"chyba při vkládání {e}")
                db_session.rollback() ##### nutnéééééééééééééééééééééééééééééééé
                return render_template("main/error.html", e=e)
            else:
                print("Zařízení založeno, trigger do transakce")
                return redirect(url_for("news.location"))

    else:
        print("první načtení")       
        return render_template("news/location.html", rozbal=select_vypis, dotaz=vypis, pravo=pravo, edit_nazev=None, edit_kod=None, edit_bud=None, chosen_id=None)

# Nové budovy
@news_bp.route("building", methods=["GET", "POST"])
def building():
    print("++ news.py | building() - vytvoření nového zařízení")
    vypis=budovy_list() 
    pravo = my_role()
    if request.method == "POST":
        print("++ čtu vstupy z formuláře")
        button_name = request.form.get('button_name')
        if button_name=="edit":
            id_bud = request.form["selected_id"]
            bud_kod  = request.form["bud_kod"] 
            bud_nazev  = request.form["bud_nazev"]   
            return render_template("news/building.html", dotaz=vypis, pravo=pravo, edit_nazev=bud_nazev, edit_kod=bud_kod, chosen_id=int(id_bud))
        elif button_name=="save":
            id = request.form["pass_id"]
            new_kod = request.form["new_kod"]
            new_nazev = request.form["new_nazev"]

            try:
                db_update_building(id, new_kod, new_nazev)
            except IntegrityError as e:
                print(f"chyba při vkládání {e}")
                return render_template("main/error.html", e=e)
            else:
                print("Zařízení založeno, trigger do transakce")
                return redirect(url_for("news.building"))
        elif button_name=="cancel":
            return redirect(url_for("news.building"))
        else:
            input = Budova(bud_kod = request.form["kod"].upper(),
                    bud_nazev = request.form["nazev"].capitalize())               

            db_session.add(input) 
            try:
                db_session.commit()
            except IntegrityError as e:
                print(f"chyba při vkládání {e}")
                db_session.rollback() ##### nutnéééééééééééééééééééééééééééééééé
                return render_template("error.html", e=e)
            else:
                print("Zařízení založeno, trigger do transakce")
                return redirect(url_for("news.building"))

    else:
        print("první načtení")
          
        return render_template("news/building.html", dotaz=vypis, pravo=pravo, edit_nazev=None, edit_kod=None, chosen_id=None)


@news_bp.route("manufacturer", methods=["GET", "POST"])
def manufacturer():
    pravo = my_role()
    vypis=vyrobce_list()
    print("++ news.py | manufacturer() - vytvoření nového zařízení")
    if request.method == "POST":
        print("++ čtu vstupy z formuláře")
        button_name = request.form.get('button_name')
        if button_name == "edit":
            id_vyr = request.form["selected_id"]
            vyr_nazev  = request.form["kat_nazev"]   
            return render_template("news/manufacturer.html", dotaz=vypis, pravo=pravo, edit_nazev=vyr_nazev, chosen_id=int(id_vyr))
        elif button_name =="save": # přepsání změn
            id = request.form["pass_id"]
            new_nazev  = request.form["new_nazev"]

            try:
                db_update_manufacturer(id, new_nazev)
            except IntegrityError as e:
                print(f"chyba při vkládání {e}")
                return render_template("main/error.html", e=e)
            else:
                print("Zařízení založeno, trigger do transakce")
                return redirect(url_for("news.manufacturer"))
            
        elif button_name =="cancel":
            return redirect(url_for("news.manufacturer"))
        else:
            input = Vyrobce(vyr_nazev = request.form["nazev"].capitalize())
            db_session.add(input) 
            try:
                db_session.commit()
            except IntegrityError as e:
                print(f"chyba při vkládání {e}")
                db_session.rollback() ##### nutnéééééééééééééééééééééééééééééééé
                return render_template("error.html", e=e)
            else:
                print("Zařízení založeno, trigger do transakce")
                return redirect(url_for("news.manufacturer"))
    else:
        print("první načtení")
        return render_template("news/manufacturer.html", dotaz=vypis, pravo=pravo, edit_nazev=None, chosen_id=None)

@news_bp.route("category", methods=["GET", "POST"])
def category():
    pravo = my_role()
    vypis = kategorie_list()
    print("++ news.py | category() - vytvoření nového zařízení")
    if request.method == "POST":
        print("++ čtu vstupy z formuláře")
        button_name = request.form.get('button_name')
        if button_name == "edit":
            print("button edit")
            id_kat = request.form["selected_id"]
            kat_nazev  = request.form["kat_nazev"]
            kat_zivot = request.form["kat_zivot"]
            print(kat_zivot, kat_nazev, id_kat)
            return render_template("news/category.html", dotaz=vypis, pravo=pravo, edit_nazev=kat_nazev, edit_zivot=kat_zivot, chosen_id=int(id_kat))
        elif button_name =="save": # přepsání změn
            id = request.form["pass_id"]
            new_nazev  = request.form["new_nazev"]
            new_zivot = request.form["new_zivot"]

            try:
                db_update_kategory(id, new_nazev, new_zivot)
            except IntegrityError as e:
                print(f"chyba při vkládání {e}")
                return render_template("main/error.html", e=e)
            else:
                print("Zařízení založeno, trigger do transakce")
                return redirect(url_for("news.category"))  
        elif button_name=="cancel":
            return redirect(url_for("news.category")) 
        else:
            input = Kategorie(kat_nazev = request.form["nazev"].capitalize())
            db_session.add(input) 
            try:
                db_session.commit()
            except IntegrityError as e:
                print(f"chyba při vkládání {e}")
                db_session.rollback() ##### nutnéééééééééééééééééééééééééééééééé
                return render_template("main/error.html", e=e)
            else:
                print("Zařízení založeno, trigger do transakce")
                return redirect(url_for("news.category"))
    else:
        print("první načtení")
        return render_template("news/category.html", dotaz=vypis, pravo=pravo, edit_nazev=None, edit_zivot=None, chosen_id=None)

@news_bp.route("user", methods=["GET", "POST"])
def user():
    pravo = my_role()
    print("++ news.py | user() - vytvoření nového uživatele")
    if request.method == "POST":
        print("++ čtu vstupy z formuláře")

        input = Uzivatel(uziv_kod = request.form["kod"].lower(),
                        uziv_jmeno = request.form["jmeno"].capitalize(),
                        uziv_prijmeni = request.form["prijmeni"].capitalize(),
                        uziv_email = request.form["email"].lower(),
                        uziv_nastup = request.form["nastup"],
                        uziv_heslo = request.form["heslo"],
                        id_vzt = request.form["vzt"],
                        id_opr = request.form["opr"]
                            )
        db_session.add(input) 

        try:
            db_session.commit()
        except IntegrityError as e:
            print(f"chyba při vkládání {e}")
            db_session.rollback() ##### nutnéééééééééééééééééééééééééééééééé
            return render_template("main/error.html", e=e)
        else:
            print("Zařízení založeno, trigger do transakce")
            return redirect(url_for("main.accounts"))

    else:
        print("první načtení")
        k=vztah_list()
        y=opravneni_list()
        return render_template("news/user.html", x=kratke_datum(), y=y, k=k, pravo=pravo)
    

