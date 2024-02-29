from flask import session
from sqlalchemy.exc import DataError
from sqlalchemy import select
from database import db_session, Zarizeni, Kategorie, Vyrobce, Uzivatel, Budova, Lokace, Transakce, Vztah, Status

def search_in_combo(text_pole, combo_pole):
    if combo_pole == 0:
        return Zarizeni.zar_inv == text_pole
    elif combo_pole == 1:
        return Zarizeni.zar_seriove == text_pole
    elif combo_pole == 2:
        return Zarizeni.zar_nazev == text_pole
    
def search_bar(text_pole, combo_pole):
    combo_pole = int(combo_pole)
    dotaz=None
    if combo_pole != 3:
        x = search_in_combo(text_pole, combo_pole)
        try:
            dotaz = (db_session.query(Zarizeni, Vyrobce, Kategorie)
                     .join(Vyrobce, Zarizeni.fk_vyr == Vyrobce.id_vyr )
                     .join(Kategorie, Zarizeni.fk_kat == Kategorie.id_kat)
                     .where(x)
                     .one_or_none())
            
        except DataError:
            print("v dotazech chybný datový formát")
            dotaz=False
            return dotaz

    elif combo_pole == 4:
        print("redireeect do uživatleů")
        x = Uzivatel.uziv_jmeno == text_pole
        dotaz = db_session.query(Uzivatel).join(Vyrobce).join(Kategorie).where(x).one_or_none()
    else:
        print("redireeect do uživatleů")
        x = Uzivatel.uziv_kod == text_pole
        dotaz = db_session.query(Uzivatel).join(Vyrobce).join(Kategorie).where(x).one_or_none()

    """dotaz2 = (db_session.query(Transakce, Zarizeni, Uzivatel, Lokace, Status, Kategorie, Vztah)
                     .join(Vyrobce, Zarizeni.fk_vyr == Vyrobce.id_vyr )
                     .join(Kategorie, Zarizeni.fk_kat == Kategorie.id_kat)
                     .where(x)
                     .all())
    """
    return dotaz


def search_add_info(text_pole, combo_box):
    pass
     




def vyrobce_list():
    list_vyr = db_session.query(Vyrobce)
    return list_vyr

def kategorie_list():
    list_kat = db_session.query(Kategorie)
    return list_kat

def budovy_list():
    list_bud = db_session.query(Budova)
    return list_bud

def lokace_list():
    list_kat = db_session.query(Kategorie)
    return list_kat

def my_role():
    if int(session.get("pravo")) == 1:
        role=True
    else:
        role=False
    return role