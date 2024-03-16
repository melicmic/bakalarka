from sqlalchemy.exc import DataError
from sqlalchemy import select, and_, not_, desc, extract, func, Integer
from database import db_session, Zarizeni, Kategorie, Vyrobce, Uzivatel, Budova, Lokace, Transakce, Vztah, Status, Opravneni
from core import rok

# Výpis ročního plánu výměn podle roku z tabulky Kategorie

def load_year(x): # vstupuje int(x)
    #x=2028
    subquery = (select(Zarizeni, Kategorie.kat_nazev, Kategorie.kat_zivot, Vyrobce.vyr_nazev,
                        (func.cast((func.extract('year', Zarizeni.zar_nakup) + Kategorie.kat_zivot), Integer)).label("zdechni"))
                      .join(Kategorie, Zarizeni.fk_kat == Kategorie.id_kat)
                      .join(Vyrobce, Zarizeni.fk_vyr == Vyrobce.id_vyr)
                      .filter(Kategorie.kat_zivot != None)
                      .subquery())
    
    stmt = (select(Transakce.tran_poznamka,
                   Lokace.lok_kod, Lokace.lok_nazev, 
                   Budova.bud_nazev, Status.stat_nazev, 
                   Uzivatel.uziv_kod, Uzivatel.uziv_email,
                   Vztah.vzt_nazev, subquery)
            .join(Zarizeni, Transakce.fk_zar == Zarizeni.id_zar)
            .join(Lokace, Transakce.fk_lok == Lokace.id_lok)
            .join(Status, Transakce.fk_stat == Status.id_stat)
            .join(Uzivatel, Transakce.fk_uziv == Uzivatel.id_uziv)
            .join(Budova, Lokace.fk_bud == Budova.id_bud)
            .join(Vztah, Uzivatel.fk_vzt == Vztah.id_vzt)
            .join(subquery, Transakce.fk_zar == subquery.c.id_zar)
            .filter(and_(Transakce.tran_platnost_do.is_(None), Transakce.fk_lok !=1))
            .order_by(Zarizeni.zar_nakup))
    
    result = db_session.execute(stmt).all()
    return result 


