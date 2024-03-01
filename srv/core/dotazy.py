from flask import session
from sqlalchemy.exc import DataError
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, not_, desc
from database import db_session, Zarizeni, Kategorie, Vyrobce, Uzivatel, Budova, Lokace, Transakce, Vztah, Status, Opravneni

# Domovská stránka pro vyhledávání
# nic
def search_bar(text_pole, combo_pole):
    combo_pole = int(combo_pole)
    dotaz = None
    dotaz2 = None
    list = [Zarizeni.zar_inv==text_pole, Zarizeni.zar_seriove==text_pole, "", Uzivatel.uziv_kod==text_pole, Uzivatel.uziv_email==text_pole]
    x = list[combo_pole]
    list2 = [Zarizeni.zar_inv==text_pole, Zarizeni.zar_seriove==text_pole, Transakce.tran_poznamka==text_pole, Uzivatel.uziv_kod==text_pole, Uzivatel.uziv_email==text_pole]
    xx = list2[combo_pole]
    try:
        dotaz = (db_session.query(Zarizeni, Vyrobce, Kategorie)
            .join(Vyrobce, Zarizeni.fk_vyr == Vyrobce.id_vyr )
            .join(Kategorie, Zarizeni.fk_kat == Kategorie.id_kat)
            .where(x)
            .one_or_none())
        
        dotaz2 = (
            db_session.query(Transakce, Zarizeni, Uzivatel, Lokace, Status, Kategorie, Vztah, Budova)
            .join(Zarizeni, Transakce.fk_zar == Zarizeni.id_zar)
            .join(Uzivatel, Transakce.fk_uziv == Uzivatel.id_uziv)
            .join(Lokace, Transakce.fk_lok == Lokace.id_lok)
            .join(Budova, Lokace.fk_bud == Budova.id_bud)
            .join(Status, Transakce.fk_stat == Status.id_stat)
            .join(Kategorie, Zarizeni.fk_kat == Kategorie.id_kat)
            .join(Vyrobce, Zarizeni.fk_vyr == Vyrobce.id_vyr) 
            .join(Vztah, Uzivatel.fk_vzt == Vztah.id_vzt)
            .where(and_(xx, Transakce.tran_platnost_do.is_(None)))
            .one_or_none()
        )

    except DataError:
        print("v dotazech chybný datový formát")
        dotaz=False
        return dotaz, dotaz2
    return dotaz, dotaz2

# Výpis všech zařízení z hlavního menu, 
# Defaultně zobrazí podle Statusu
def device_listing(text_pole=1, combo_pole=7):
    if text_pole == 1:
        text_pole = status_list(text_pole)
    combo_pole=int(combo_pole)
    print(combo_pole)
    list = [Zarizeni.zar_inv==text_pole, Zarizeni.zar_seriove==text_pole, Vyrobce.vyr_nazev==text_pole, 
            Zarizeni.zar_model==text_pole, Transakce.tran_poznamka==text_pole, Kategorie.kat_nazev==text_pole, 
            Zarizeni.zar_nakup==text_pole, Status.stat_nazev==text_pole, Lokace.id_lok==text_pole, Budova.bud_kod==text_pole]
    x = list[combo_pole]

    dotaz3 = (db_session.query(Transakce, Zarizeni, Lokace, Status, Kategorie, Vyrobce)
            .join(Zarizeni, Transakce.fk_zar == Zarizeni.id_zar)
            .join(Lokace, Transakce.fk_lok == Lokace.id_lok)
            .join(Status, Transakce.fk_stat == Status.id_stat)
            .join(Kategorie, Zarizeni.fk_kat == Kategorie.id_kat)
            .join(Vyrobce, Zarizeni.fk_vyr == Vyrobce.id_vyr) 
            .where(and_(x, Transakce.tran_platnost_do.is_(None)))
            .order_by(desc(Transakce.id_tran))
            .limit(20)
            .all())
    
    return dotaz3

# Výpis Transakcí z hlavního menu
# Funguje jako potvrzení trigerru     
def transaction_listing(text_pole, combo_pole_t,y=20):
    if text_pole == None:
        dotaz4 = (db_session.query(Transakce, Uzivatel, Zarizeni, Lokace, Status, Kategorie, Vyrobce, Budova)
        .join(Zarizeni, Transakce.fk_zar == Zarizeni.id_zar)
        .join(Lokace, Transakce.fk_lok == Lokace.id_lok)
        .join(Status, Transakce.fk_stat == Status.id_stat)
        .join(Kategorie, Zarizeni.fk_kat == Kategorie.id_kat)
        .join(Vyrobce, Zarizeni.fk_vyr == Vyrobce.id_vyr)
        .join(Budova, Lokace.fk_bud == Budova.id_bud)
        .join(Uzivatel, Transakce.fk_uziv == Uzivatel.id_uziv)
        .order_by(desc(Transakce.tran_editace))
        .limit(y).all())
    else:
        combo_pole=int(combo_pole_t)
        list = [Zarizeni.zar_inv==text_pole, 
                Zarizeni.zar_seriove==text_pole,
                Vyrobce.vyr_nazev==text_pole, 
                Zarizeni.zar_model==text_pole,
                Transakce.tran_poznamka==text_pole,
                Kategorie.kat_nazev==text_pole,
                Uzivatel.uziv_kod==text_pole, 
                Status.stat_nazev==text_pole,
                Lokace.lok_kod==text_pole,
                Budova.bud_kod==text_pole,
                Transakce.id_tran==text_pole]
        x = list[combo_pole]
            
        dotaz4 = (db_session.query(Transakce, Uzivatel, Zarizeni, Lokace, Status, Kategorie, Vyrobce, Budova)
                .join(Zarizeni, Transakce.fk_zar == Zarizeni.id_zar)
                .join(Lokace, Transakce.fk_lok == Lokace.id_lok)
                .join(Status, Transakce.fk_stat == Status.id_stat)
                .join(Kategorie, Zarizeni.fk_kat == Kategorie.id_kat)
                .join(Vyrobce, Zarizeni.fk_vyr == Vyrobce.id_vyr)
                .join(Budova, Lokace.fk_bud == Budova.id_bud)
                .join(Uzivatel, Transakce.fk_uziv == Uzivatel.id_uziv)
                .order_by(desc(Transakce.tran_editace))
                .where(x)
                .limit(y).all())
    return dotaz4

# Výpis všech uživatelů
# Defaultně řazeno podle abecedy
def user_listing(text_pole, combo_pole):
    combo_pole=int(combo_pole)
    if text_pole == None:
        dotaz5 = (db_session.query(Uzivatel, Vztah, Opravneni)
            .join(Vztah, Uzivatel.fk_vzt == Vztah.id_vzt)
            .join(Opravneni, Uzivatel.fk_opr == Opravneni.id_opr)
            .order_by((Uzivatel.uziv_prijmeni))
            .where(not_(Vztah.id_vzt==1))
            .all())
    else:
        list = [Uzivatel.uziv_kod==text_pole, Uzivatel.uziv_jmeno==text_pole, Uzivatel.uziv_prijmeni==text_pole, Uzivatel.uziv_email==text_pole, Vztah.vzt_nazev==text_pole, Opravneni.opr_nazev==text_pole]
        x = list[combo_pole]
        print(x)
        dotaz5 = (db_session.query(Uzivatel, Vztah, Opravneni)
            .join(Vztah, Uzivatel.fk_vzt == Vztah.id_vzt)
            .join(Opravneni, Uzivatel.fk_opr == Opravneni.id_opr)
            .order_by((Uzivatel.uziv_prijmeni))
            .where(x)
            .all())
    print(dotaz5)         
    return dotaz5



# Pomůcka na vypsání všech položek do rozbalovacího seznamu
# V částech vytváření --- šlo by zjednodušit na jednu funkci (???)
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
    list_lok = db_session.query(Kategorie)
    return list_lok

def vztah_list():
    list_vzt = db_session.query(Vztah)
    return list_vzt

def opravneni_list():
    list_opr = db_session.query(Opravneni)
    return list_opr

def status_list(x):
    list_stat = db_session.query(Status.stat_nazev).where(Status.id_stat==x)
        
    print(list_stat)
    return list_stat


# Pomůcka pro zjištění oprávnění k zapisování
# Zobrazí editovací pole a tlačítka
def my_role():
    if int(session.get("pravo")) == 1:
        role=True
    else:
        role=False
    return role
