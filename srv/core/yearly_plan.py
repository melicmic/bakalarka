from sqlalchemy.exc import DataError
from sqlalchemy import select, and_, not_, desc, extract, func, Integer
from database import db_session, Zarizeni, Kategorie, Vyrobce, Uzivatel, Budova, Lokace, Transakce, Vztah, Status, Opravneni
from core import rok

# Výpis ročního plánu výměn podle roku z tabulky Kategorie

def report_yearly(x): # vstupuje int(x)
    #x=2028
    subquery = (select(Zarizeni, Kategorie.kat_nazev, Kategorie.kat_zivot, Vyrobce.vyr_nazev,
                        (func.cast((func.extract('year', Zarizeni.zar_nakup) + Kategorie.kat_zivot), Integer)).label("zdechni"))
                      .join(Kategorie, Zarizeni.id_kat == Kategorie.id_kat)
                      .join(Vyrobce, Zarizeni.id_vyr == Vyrobce.id_vyr)
                      .filter(Kategorie.kat_zivot != None)
                      .subquery())
    
    stmt = (select(Transakce.tran_poznm,
                   Lokace.lok_kod, Lokace.lok_nazev, 
                   Budova.bud_nazev, Status.stat_nazev, 
                   Uzivatel.uziv_kod, Uzivatel.uziv_email,
                   Vztah.vzt_nazev, subquery)
            .join(Zarizeni, Transakce.id_zar == Zarizeni.id_zar)
            .join(Lokace, Transakce.id_lok == Lokace.id_lok)
            .join(Status, Transakce.id_stat == Status.id_stat)
            .join(Uzivatel, Transakce.id_uziv == Uzivatel.id_uziv)
            .join(Budova, Lokace.id_bud == Budova.id_bud)
            .join(Vztah, Uzivatel.id_vzt == Vztah.id_vzt)
            .join(subquery, Transakce.id_zar == subquery.c.id_zar)
            .filter(and_(Transakce.tran_platnost_do.is_(None), Transakce.id_lok !=1))
            .order_by(Zarizeni.zar_nakup))
    
    result = db_session.execute(stmt).all()
    return result 

# Výpis položek na skladě (lok=2) na úvodní stránce
def report_stock():
    stmt = (select(Kategorie.id_kat, Kategorie.kat_nazev, (func.count((Zarizeni.id_zar)).label("pocet")))
            .join(Transakce, Transakce.id_zar == Zarizeni.id_zar)
            .join(Kategorie, Zarizeni.id_kat == Kategorie.id_kat)
            .filter(and_(Transakce.tran_platnost_do.is_(None), Transakce.id_lok == 2))
            .group_by(Kategorie.kat_nazev, Kategorie.id_kat)
            .order_by(Kategorie.id_kat))
    result = db_session.execute(stmt).all()
    return result
    
# Výpis celkových položek, lok>3 (nezahrnuje rip, it sklad a junk)
def report_usecount():
    stmt = (select(Kategorie.id_kat, Kategorie.kat_nazev, (func.count((Zarizeni.id_zar)).label("pocet")))
            .join(Transakce, Transakce.id_zar == Zarizeni.id_zar)
            .join(Kategorie, Zarizeni.id_kat == Kategorie.id_kat)
            .filter(and_(Transakce.tran_platnost_do.is_(None), Transakce.id_lok > 3))
            .group_by(Kategorie.kat_nazev, Kategorie.id_kat)
            .order_by(Kategorie.id_kat))
    result2 = db_session.execute(stmt).all()
    return result2

"""select count(zt.zar_inv), kt.kat_nazev, kt.id_kat  from "Transakce_tab" tt 
left join "Zarizeni_tab" zt 
on tt.id_zar = zt.id_zar
left join  "Kategorie_tab" kt
on zt.id_kat = kt.id_kat
where (tt.tran_platnost_do is null ) and (tt.id_lok = 2)
group by kt.kat_nazev, kt.id_kat 
"""