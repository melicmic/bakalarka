from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Date, DateTime, ForeignKey, SmallInteger, UniqueConstraint

from typing import List, Optional
import datetime

# Párování SQL na ORM-Python
class Base(DeclarativeBase):
    pass

# Definice tabulek v DB
class Vyrobce(Base):
    __tablename__ = "Vyrobci_tab"
    id_vyr: Mapped[int] = mapped_column(primary_key=True)
    vyr_nazev: Mapped[str] = mapped_column(String(30), unique=True) # název výrobce
    
    fk_vyr_zar: Mapped[List["Zarizeni"]] = relationship(back_populates="fk_zar_vyr")

    def __repr__(self) -> str:
        return f"Vyrobce(id={self.id_vyr!r}, name={self.vyr_nazev!r})"

class Kategorie(Base):
    __tablename__ = "Kategorie_tab"
    id_kat: Mapped[int] = mapped_column(primary_key=True)
    kat_nazev: Mapped[str] = mapped_column(String(30), unique=True) # název kategorie - pc, ntbk, workst,...
    kat_zivot: Mapped[Optional[int]] = mapped_column(Integer)

    fk_kat_zar: Mapped[List["Zarizeni"]] = relationship(back_populates="fk_zar_kat")

    def __repr__(self) -> str:
        return f"Kategorie(id={self.id_kat!r}, name={self.kat_nazev!r}, zivot={self.kat_zivot!r})"

class Status(Base):
    __tablename__ = "Statusy_tab"
    id_stat: Mapped[int] = mapped_column(primary_key=True)
    stat_nazev: Mapped[str] = mapped_column(String(30), unique=True) # název statusu

    fk_stat_tran: Mapped[List["Transakce"]] = relationship(back_populates="fk_tran_stat")

class Zarizeni(Base):
    __tablename__ = "Zarizeni_tab"
    __table_args__ = (
        UniqueConstraint("zar_inv"),
    )
    id_zar: Mapped[int] = mapped_column(primary_key=True)
    zar_inv: Mapped[int] = mapped_column(Integer) # inventární číslo
    zar_seriove: Mapped[str] = mapped_column(String(30), unique=True) # sériové číslo
    zar_model: Mapped[str] = mapped_column(String(30)) # model zařízení
    zar_nakup: Mapped[datetime.date] = mapped_column(Date) # datum nakupu
    zar_smrt: Mapped[Optional[int]] = mapped_column(SmallInteger) # datum vyřazení
    zar_poznm: Mapped[Optional[str]] = mapped_column(String(64)) # poznámka
    # FK - kategorie, model->výrobce?, status?
    fk_kat: Mapped[int] = mapped_column(ForeignKey("Kategorie_tab.id_kat"))
    fk_vyr: Mapped[int] = mapped_column(ForeignKey("Vyrobci_tab.id_vyr"))
    
    fk_zar_tran: Mapped[List["Transakce"]] = relationship(back_populates="fk_tran_zar")
    fk_zar_vyr: Mapped[List["Vyrobce"]] = relationship(back_populates="fk_vyr_zar")
    fk_zar_kat: Mapped[List["Kategorie"]] = relationship(back_populates="fk_kat_zar")

    def __repr__(self):
        return f"<Zarizeni(id_zar={self.id_zar}, zar_inv={self.zar_inv}, zar_seriove='{self.zar_seriove}', zar_model='{self.zar_model}', zar_nakup={self.zar_nakup}, zar_smrt={self.zar_smrt}, zar_poznm='{self.zar_poznm}', fk_kat={self.fk_kat}, fk_vyr={self.fk_vyr})>"



class Uzivatel(Base):
    __tablename__ = "Uzivatele_tab"
    __table_args__ = (
        UniqueConstraint("uziv_kod"),
    )
    id_uziv: Mapped[int] = mapped_column(primary_key=True)
    uziv_kod: Mapped[str] = mapped_column(String(30)) # id-čko
    uziv_jmeno: Mapped[str] = mapped_column(String(30)) # jméno
    uziv_prijmeni: Mapped[Optional[str]] = mapped_column(String(30)) # příjmené
    uziv_email: Mapped[Optional[str]] = mapped_column(String(30), unique=True) # email
    uziv_nastup: Mapped[Optional[datetime.date]] = mapped_column(Date) # den nástupu
    uziv_vystup: Mapped[Optional[datetime.date]] = mapped_column(Date) # den ukončení
    uziv_heslo: Mapped[Optional[str]] = mapped_column(String(30)) # heslo
    # FK - vztah, opravneni
    fk_vzt: Mapped[int] = mapped_column(ForeignKey("Vztahy_tab.id_vzt"))
    fk_opr: Mapped[int] = mapped_column(ForeignKey("Opravneni_tab.id_opr"))
    
    fk_uziv_tran: Mapped[List["Transakce"]] = relationship(back_populates="fk_tran_uziv")
    fk_uziv_opr: Mapped[List["Opravneni"]] = relationship(back_populates="fk_opr_uziv")
    fk_uziv_vzt: Mapped[List["Vztah"]] = relationship(back_populates="fk_vzt_uziv")

class Vztah(Base):
    __tablename__ = "Vztahy_tab"
    id_vzt: Mapped[int] = mapped_column(primary_key=True)
    vzt_nazev: Mapped[str] = mapped_column(String(30)) # název vztahu - externi, interni, vyrobni, ot

    fk_vzt_uziv: Mapped[List["Uzivatel"]] = relationship(back_populates="fk_uziv_vzt")

class Opravneni(Base):
    __tablename__ = "Opravneni_tab"
    id_opr: Mapped[int] = mapped_column(primary_key=True)
    opr_nazev: Mapped[str] = mapped_column(String(30)) # název oprávnění
    
    fk_opr_uziv: Mapped[List["Uzivatel"]] = relationship(back_populates="fk_uziv_opr")
    # admin, čtení, zadny

class Lokace(Base):
    __tablename__ = "Lokace_tab"
    __table_args__ = (
        UniqueConstraint("lok_kod"),
    )
    id_lok: Mapped[int] = mapped_column(primary_key=True)
    lok_kod: Mapped[str] = mapped_column(String(30), unique=True) # kód lokace
    lok_nazev: Mapped[str] = mapped_column(String(30)) # název lokace

    fk_bud: Mapped[int] = mapped_column(ForeignKey("Budovy_tab.id_bud"))

    fk_lok_tran: Mapped[List["Transakce"]] = relationship(back_populates="fk_tran_lok")
    fk_lok_bud: Mapped[List["Budova"]] = relationship(back_populates="fk_bud_lok")

    def __repr__(self):
        return f"<Lokace(id_lok={self.id_lok}, lok_kod='{self.lok_kod}', lok_nazev='{self.lok_nazev}', fk_bud={self.fk_bud})>"

class Budova(Base):
    __tablename__ = "Budovy_tab"
    __table_args__ = (
        UniqueConstraint("bud_kod"),
    )
    id_bud: Mapped[int] = mapped_column(primary_key=True)
    bud_kod: Mapped[str] = mapped_column(String(8))
    bud_nazev: Mapped[str] = mapped_column(String(30)) # název budovy A-B-C

    fk_bud_lok: Mapped[List["Lokace"]] = relationship(back_populates="fk_lok_bud")

    def __repr__(self):
        return f"<Budova(id_bud={self.id_bud}, bud_kod='{self.bud_kod}', bud_nazev='{self.bud_nazev}')>"

class Transakce(Base):
    __tablename__ = "Transakce_tab"
    id_tran: Mapped[int] = mapped_column(primary_key=True)
    tran_platnost_od: Mapped[datetime.datetime] = mapped_column(Date) # název oprávnění
    tran_platnost_do: Mapped[Optional[datetime.datetime]] = mapped_column(Date) # popis oprávnění  
    tran_poznamka: Mapped[str] = mapped_column(String(30)) # poznámka oprávnění
    #tran_nazev: Mapped[str] = mapped_column(String(30), unique=True) # domenové jméno
    tran_editace: Mapped[datetime.datetime] = mapped_column(DateTime)

    fk_uziv: Mapped[int] = mapped_column(ForeignKey("Uzivatele_tab.id_uziv"))
    fk_zar: Mapped[int] = mapped_column(ForeignKey("Zarizeni_tab.id_zar"))
    fk_lok: Mapped[int] = mapped_column(ForeignKey("Lokace_tab.id_lok"))
    fk_stat: Mapped[int] = mapped_column(ForeignKey("Statusy_tab.id_stat"))

    fk_tran_uziv: Mapped[List["Uzivatel"]] = relationship(back_populates="fk_uziv_tran")
    fk_tran_zar: Mapped[List["Zarizeni"]] = relationship(back_populates="fk_zar_tran")
    fk_tran_lok: Mapped[List["Lokace"]] = relationship(back_populates="fk_lok_tran")
    fk_tran_stat: Mapped[List["Status"]] = relationship(back_populates="fk_stat_tran")
    # FK - zamestanenc, zarizeni, lokace, status, 
    
    def __repr__(self):
        return f"<Transakce(id_tran={self.id_tran}, tran_platnost_od='{self.tran_platnost_od}', tran_platnost_do='{self.tran_platnost_do}', tran_poznamka={self.tran_poznamka}, tran_editace='{self.tran_editace}', fk_uziv='{self.fk_uziv}', fk_zar={self.fk_zar}, fk_lok='{self.fk_lok}', fk_stat={self.fk_stat})>"
    