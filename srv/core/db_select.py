from sqlalchemy.exc import DataError
from sqlalchemy import select, and_, not_, desc
from database import db_session, Zarizeni, Kategorie, Vyrobce, Uzivatel, Budova, Lokace, Transakce, Vztah, Status, Opravneni
from core import status_list


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
        #return dotaz, dotaz2  
    return dotaz, dotaz2

# Výpis všech zařízení z hlavního menu, výchozí zobrazení - všechno
def device_listing(text_pole=None, combo_pole=0):
    combo_pole = int(combo_pole)
    
    list = [ Zarizeni.zar_inv!=text_pole, Zarizeni.zar_inv==text_pole, Zarizeni.zar_seriove==text_pole, Vyrobce.vyr_nazev==text_pole, 
                Zarizeni.zar_model==text_pole, Kategorie.kat_nazev==text_pole, Zarizeni.zar_nakup==text_pole ]
    x = list[combo_pole]
    dotaz3 = (db_session.query(Zarizeni, Kategorie, Vyrobce)
            .join(Kategorie, Zarizeni.fk_kat == Kategorie.id_kat)
            .join(Vyrobce, Zarizeni.fk_vyr == Vyrobce.id_vyr)
            .order_by(desc(Zarizeni.id_zar))
            .where(x)
            .limit(50)
            .all())
    db_session.close()
    return dotaz3

# Výpis Transakcí z hlavního menu
# Funguje jako potvrzení trigerru     
def transaction_listing(text_pole, combo_pole_t,y=50):
    if text_pole == None: # první načtení přehledu bez zadaných parametrů
        dotaz4 = (db_session.query(Transakce, Uzivatel, Zarizeni, Lokace, Status, Kategorie, Vyrobce, Budova)
        .join(Zarizeni, Transakce.fk_zar == Zarizeni.id_zar)
        .join(Lokace, Transakce.fk_lok == Lokace.id_lok)
        .join(Status, Transakce.fk_stat == Status.id_stat)
        .join(Kategorie, Zarizeni.fk_kat == Kategorie.id_kat)
        .join(Vyrobce, Zarizeni.fk_vyr == Vyrobce.id_vyr)
        .join(Budova, Lokace.fk_bud == Budova.id_bud)
        .join(Uzivatel, Transakce.fk_uziv == Uzivatel.id_uziv)
        .where(Transakce.tran_platnost_do.is_(None))
        .order_by(desc(Transakce.tran_editace), Transakce.id_tran)
        .limit(y).all())
    else: # pro filtrování výsledků
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
        
        # Výpis historie pro konkrétní INV číslo, řazeno podle id_tran
        dotaz4 = (db_session.query(Transakce, Uzivatel, Zarizeni, Lokace, Status, Kategorie, Vyrobce, Budova)
                .join(Zarizeni, Transakce.fk_zar == Zarizeni.id_zar)
                .join(Lokace, Transakce.fk_lok == Lokace.id_lok)
                .join(Status, Transakce.fk_stat == Status.id_stat)
                .join(Kategorie, Zarizeni.fk_kat == Kategorie.id_kat)
                .join(Vyrobce, Zarizeni.fk_vyr == Vyrobce.id_vyr)
                .join(Budova, Lokace.fk_bud == Budova.id_bud)
                .join(Uzivatel, Transakce.fk_uziv == Uzivatel.id_uziv)
                .order_by(desc(Transakce.id_tran), desc(Transakce.tran_editace))
                .where(x)
                .all())
    db_session.close()   
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
    db_session.close()    
    return dotaz5

# Vypsání při přesunu/vyřazení
def relocation_listing(selected_lok):
    dotaz6 = (db_session.query(Transakce, Uzivatel, Zarizeni, Lokace, Status, Kategorie, Vyrobce, Budova)
    .join(Zarizeni, Transakce.fk_zar == Zarizeni.id_zar)
    .join(Lokace, Transakce.fk_lok == Lokace.id_lok)
    .join(Status, Transakce.fk_stat == Status.id_stat)
    .join(Kategorie, Zarizeni.fk_kat == Kategorie.id_kat)
    .join(Vyrobce, Zarizeni.fk_vyr == Vyrobce.id_vyr)
    .join(Budova, Lokace.fk_bud == Budova.id_bud)
    .join(Uzivatel, Transakce.fk_uziv == Uzivatel.id_uziv)
    .where((and_(Transakce.tran_platnost_do.is_(None), Lokace.id_lok == selected_lok)))
    .order_by(Zarizeni.zar_inv)
    .all())
    db_session.close()   
    return dotaz6
