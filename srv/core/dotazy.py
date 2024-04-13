from flask import session

from database import db_session, Zarizeni, Kategorie, Vyrobce, Uzivatel, Budova, Lokace, Transakce, Vztah, Status, Opravneni

# Pomůcka na vypsání všech položek do rozbalovacího seznamu
# V částech vytváření --- šlo by zjednodušit na jednu funkci (???)
def vyrobce_list():
    list_vyr = db_session.query(Vyrobce).all()
    db_session.close()
    return list_vyr

def kategorie_list():
    list_kat = db_session.query(Kategorie).order_by(Kategorie.id_kat).all()
    db_session.close()
    return list_kat

def budovy_list():
    list_bud = db_session.query(Budova).all()
    db_session.close()
    return list_bud

def lokace_list():
    list_lok = db_session.query(Lokace, Budova).join(Budova, Lokace.id_bud == Budova.id_bud).all()
    db_session.close()
    return list_lok

def vztah_list():
    list_vzt = db_session.query(Vztah).all()
    db_session.close()
    return list_vzt

def opravneni_list():
    list_opr = db_session.query(Opravneni).all()
    db_session.close()
    return list_opr

def status_list(x):
    if x is None:
        ls = db_session.query(Status).all()
    else:
        list_stat = db_session.query(Status.stat_nazev).where(Status.id_stat==x).one_or_none()   
        ls = list_stat[0]
    db_session.close()
    return ls

def uzivatel_list(x):
    if x is None:
            ls=db_session.query(Uzivatel).all()
    elif x == 1:
            ls=db_session.query(Uzivatel).where(Uzivatel.uziv_vystup.is_(None)).all()
    else:    
        list_uziv=db_session.query(Uzivatel.id_uziv).where(Uzivatel.uziv_kod==x).one_or_none()
        ls = list_uziv[0]
    return ls



# Pomůcka pro zjištění oprávnění k zapisování
# Zobrazí editovací pole a tlačítka
def my_role():
    if int(session.get("pravo")) == 1:
        role=True
    else:
        role=False
    return role
