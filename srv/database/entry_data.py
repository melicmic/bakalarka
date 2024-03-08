from .schema import Budova, Lokace, Vztah, Opravneni, Status, Kategorie, Vyrobce, Uzivatel
from .connect import db_session
import datetime

def naplneni_dat():
    vlozeni_budova()
    vlozeni_kategorie()
    vlozeni_lokace()
    vlozeni_opravneni()
    vlozeni_status()
    vlozeni_vztah()
    vlozeni_vyrobce()
    vlozeni_uzivatele()

def vlozeni_budova():
    b1 = Budova(bud_kod="AAA", bud_nazev="hala A")
    b2 = Budova(bud_kod="BBB", bud_nazev="hala B")
    b3 = Budova(bud_kod="CCC", bud_nazev="hala C")
    
    db_session.add_all([b1,b2,b3])
    db_session.commit()
    print("Budova - hotovo")

def vlozeni_lokace():
    l1 = Lokace(lok_kod="RIP", lok_nazev="Křemíkové nebe", fk_bud=1)
    l2 = Lokace(lok_kod="IT", lok_nazev="Sklad IT", fk_bud=1)
    l3 = Lokace(lok_kod="JUNK", lok_nazev="Smetiště", fk_bud=1)
    l4 = Lokace(lok_kod="A04", lok_nazev="Kontorla O2", fk_bud=1)
    l5 = Lokace(lok_kod="A05", lok_nazev="Expedice O1", fk_bud=1)
    l6 = Lokace(lok_kod="B01", lok_nazev="Stul O1", fk_bud=2)
    l7 = Lokace(lok_kod="B02", lok_nazev="Stul O2", fk_bud=2)
    l8 = Lokace(lok_kod="B03", lok_nazev="Kontrola 01", fk_bud=2)
    l9 = Lokace(lok_kod="B04", lok_nazev="Kontrola 02", fk_bud=2)
    l10 = Lokace(lok_kod="B05", lok_nazev="Expedice 01", fk_bud=2)    
    l11 = Lokace(lok_kod="C01", lok_nazev="Stul O1", fk_bud=3)
    l12 = Lokace(lok_kod="C02", lok_nazev="Stul O2", fk_bud=3)
    l13 = Lokace(lok_kod="C03", lok_nazev="Kontrola O1", fk_bud=3)
    l14 = Lokace(lok_kod="C04", lok_nazev="Kontrola 02", fk_bud=3)
    l15 = Lokace(lok_kod="C05", lok_nazev="Expedice 01", fk_bud=3)    
    
    db_session.add_all([l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11,l12,l13,l14,l15])
    db_session.commit()
    print("Lokace - hotovo")

# Vztahy - Interní, Externí, Vyrobní, Dodavatel
def vlozeni_vztah():
    v1 = Vztah(vzt_nazev="Systémový")
    v2 = Vztah(vzt_nazev="Výrobní")
    v3 = Vztah(vzt_nazev="Interní")
    v4 = Vztah(vzt_nazev="Externí")
    v5 = Vztah(vzt_nazev="Dodavatel")

    db_session.add_all([v1,v2,v3,v4, v5])
    db_session.commit()
    print("Vztah - hotovo")

def vlozeni_opravneni():
   
    o1 = Opravneni(opr_nazev="Editor")
    o2 = Opravneni(opr_nazev="Čtenář")
    o3 = Opravneni(opr_nazev="Vyloučený")
        
    db_session.add_all([o1,o2,o3])
    db_session.commit()
    print("Oprávnění - hotovo")

def vlozeni_kategorie():
    k1 = Kategorie(kat_nazev="Notebook")
    k2 = Kategorie(kat_nazev="PC Desktop")
    k3 = Kategorie(kat_nazev="PC Tower")
    k4 = Kategorie(kat_nazev="PC Workstation")
    k5 = Kategorie(kat_nazev="Monitor")
    k6 = Kategorie(kat_nazev="Monitor HUB")
    k7 = Kategorie(kat_nazev="Dokovací stanice")
    k8 = Kategorie(kat_nazev="Mobil")
    k9 = Kategorie(kat_nazev="Tablet")
    k10 = Kategorie(kat_nazev="Telefon")    
    k11 = Kategorie(kat_nazev="Tiskárna")
    k12 = Kategorie(kat_nazev="USB příslušenství")
    k13 = Kategorie(kat_nazev="Taška")
    k14 = Kategorie(kat_nazev="Ostatní")
        
    db_session.add_all([k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11,k12,k13,k14])
    db_session.commit()
    print("Kategorie - hotovo")

def vlozeni_status():
    s1 = Status(stat_nazev="Naskladněno")
    s2 = Status(stat_nazev="Aktivní")
    s3 = Status(stat_nazev="Rezervní")
    s4 = Status(stat_nazev="V opravě")
    s5 = Status(stat_nazev="Zapůjčeno")
    s6 = Status(stat_nazev="Likvidace")
    s7 = Status(stat_nazev="Výměna")
    s8 = Status(stat_nazev="Vráceno")
    s9 = Status(stat_nazev="Odkoupeno")
    s10 = Status(stat_nazev="Vyřazeno")
    s11 = Status(stat_nazev="Ztraceno")    
    s12 = Status(stat_nazev="Nalezeno")
    
        
    db_session.add_all([s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12])
    db_session.commit()
    print("Status - hotovo")

def vlozeni_vyrobce():
    vy1 = Vyrobce(vyr_nazev="Dell")
    vy2 = Vyrobce(vyr_nazev="HP")
    vy3 = Vyrobce(vyr_nazev="Apple")
    vy4 = Vyrobce(vyr_nazev="Samsung")
    vy5 = Vyrobce(vyr_nazev="Lenovo")
    vy6 = Vyrobce(vyr_nazev="Zebra")
        
    db_session.add_all([vy1,vy2,vy3,vy4,vy5,vy6])
    db_session.commit()
    print("Výrobce - hotovo")    


def vlozeni_uzivatele():
    u1 = Uzivatel(uziv_kod="admin", uziv_jmeno="Flask-Admin", uziv_prijmeni="1-Editor", uziv_nastup=datetime.datetime.now(), 
        uziv_heslo="admin", fk_vzt=1, fk_opr=1)
    u2 = Uzivatel(uziv_kod="visitor", uziv_jmeno="Návštěvník", uziv_prijmeni="2-Čtenář", uziv_nastup=datetime.datetime.now(),
                  uziv_heslo="visitor", fk_vzt=1, fk_opr=2)
    u3 = Uzivatel(uziv_kod="expelled", uziv_jmeno="Vyloučený", uziv_prijmeni="3-Vyloučený", uziv_nastup=datetime.datetime.now(),
                  uziv_heslo="expelled", fk_vzt=1, fk_opr=2)      
    db_session.add_all([u1, u2, u3])
    db_session.commit()
    print("Uzivatel - hotovo")



