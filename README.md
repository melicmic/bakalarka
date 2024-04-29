
# Bakalářkská práce - Hardwarová evidence majetku

Hlavní stránka:
![Snímek obrazovky z 2024-04-29 15-35-56](https://github.com/melicmic/bakalarka/assets/108867825/38b0d981-78b5-4c45-8fbd-6b708f8ec5d3)


Databázový model:

![Snímek obrazovky z 2024-04-29 15-38-42](https://github.com/melicmic/bakalarka/assets/108867825/2417d4ba-fbf9-4913-897f-807b6f32d03a)

Funguje:
- založení zařízení (kontorla duplicit)
- vyhledání podle parametrů
- sledování historie od založení po vyřazení
- administrace základních tabulek (založení, editace, smazání)
- automatické naskladnění po založení zařízení
- přesun mezi lokacemi (i hromadný)
- automatické sestavování plánu výměn
- správa uživatelských účtu
- filtrování podle lokací s přiřazeným majetkem
- rozlišení UI podle oprávnění (editor/návtěvník)

Náměty na zlepšení:
- vylepšit UI (sjednotit styly tabulek, přizpůsobit na menší monitory, ...)
- napovídání hodnot, chytré vyhledávání
- omezit dotazování do DB, ukládát si některá data do paměti
- navrhnout hromadný import při zakádání nových záznamů
- navrhout skript pro naplnění dat při prvním spuštění
- doplnit sloupcové vyhledávání
- export do jiných formátů (xls, csv)
- doplnit prohlížení podle účtů (účet -> jaká zařízení?)
- detailnější členění u záznamu o Výrobci (obchodní značka modelu, ...)
- vylepšit UI chybových hlášek
