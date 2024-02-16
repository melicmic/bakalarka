from sqlalchemy.orm import sessionmaker
from core.vytvoreni_schema import Budova, Lokace, Vztah, Opravneni, Status, Kategorie, Vyrobce

def sm_bind(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def sm_commit(session):
    session.commit()

def naplneni_dat(engine):
    vlozeni_budova(engine)
    vlozeni_kategorie(engine)
    vlozeni_lokace(engine)
    vlozeni_opravneni(engine)
    vlozeni_status(engine)
    vlozeni_vztah(engine)
    vlozeni_vyrobce(engine)

def vlozeni_budova(engine):
    session = sm_bind(engine)
    b1 = Budova(bud_nazev="hala A")
    b2 = Budova(bud_nazev="hala B")
    b3 = Budova(bud_nazev="hala C")
    session.add_all([b1,b2,b3])
    sm_commit(session)
    print("Budova - hotovo")

def vlozeni_lokace(engine):
    session = sm_bind(engine)
    l1 = Lokace(lok_kod="A01", lok_nazev="Stul O1", fk_bud=1)
    l2 = Lokace(lok_kod="A02", lok_nazev="Stul O2", fk_bud=1)
    l3 = Lokace(lok_kod="A03", lok_nazev="Kontrola O1", fk_bud=1)
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
    
    session.add_all([l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11,l12,l13,l14,l15])
    sm_commit(session)
    print("Lokace - hotovo")

# Vztahy - Interní, Externí, Vyrobní, Dodavatel
def vlozeni_vztah(engine):
    session = sm_bind(engine)
    v1 = Vztah(vzt_nazev="Interní")
    v2 = Vztah(vzt_nazev="Výrobní")
    v3 = Vztah(vzt_nazev="Externí")
    v4 = Vztah(vzt_nazev="Dodavatel")

    session.add_all([v1,v2,v3,v4])
    sm_commit(session)
    print("Vztah - hotovo")

def vlozeni_opravneni(engine):
    session = sm_bind(engine)
    o1 = Opravneni(opr_nazev="Editor")
    o2 = Opravneni(opr_nazev="Čtenář")
    o3 = Opravneni(opr_nazev="Vyloučený")
        
    session.add_all([o1,o2,o3])
    sm_commit(session)
    print("Oprávnění - hotovo")

def vlozeni_kategorie(engine):
    session = sm_bind(engine)
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
        
    session.add_all([k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11,k12,k13,k14])
    sm_commit(session)
    print("Kategorie - hotovo")

def vlozeni_status(engine):
    session = sm_bind(engine)
    s1 = Status(stat_nazev="Aktivní")
    s2 = Status(stat_nazev="Rezervní")
    s3 = Status(stat_nazev="V opravě")
    s4 = Status(stat_nazev="Zapůjčeno")
    s5 = Status(stat_nazev="Likvidace")
    s6 = Status(stat_nazev="Výměna")
    s7 = Status(stat_nazev="Vráceno")
    s8 = Status(stat_nazev="Odkoupeno")
    s9 = Status(stat_nazev="Vyřezeno")
    s10 = Status(stat_nazev="Ztraceno")    
    s11 = Status(stat_nazev="Nalezeno")
    s12 = Status(stat_nazev="Naskladněno")
        
    session.add_all([s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12])
    sm_commit(session)
    print("Status - hotovo")

def vlozeni_vyrobce(engine):
    session = sm_bind(engine)
    vy1 = Vyrobce(vyr_nazev="Dell")
    vy2 = Vyrobce(vyr_nazev="HP")
    vy3 = Vyrobce(vyr_nazev="Apple")
    vy4 = Vyrobce(vyr_nazev="Samsung")
    vy5 = Vyrobce(vyr_nazev="Lenovo")
    vy6 = Vyrobce(vyr_nazev="Zebra")
        
    session.add_all([vy1,vy2,vy3,vy4,vy5,vy6])
    sm_commit(session)
    print("Výrobce - hotovo")    