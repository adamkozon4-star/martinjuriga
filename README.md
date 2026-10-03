# Martin Juriga – web finančného sprostredkovateľa

Statický web (HTML + CSS + JS), bez buildu. Stačí otvoriť `index.html` alebo nasadiť priečinok.

## Nasadenie (Vercel)
*Add New Project* → import tohto repozitára → **Deploy**. Nič netreba nastavovať, web je v koreni repozitára.
Každý push do vetvy `main` sa nasadí automaticky. Vlastnú doménu pripojíš v *Settings → Domains*.

## Ešte treba doplniť
| Čo | Kde |
|---|---|
| Formulár cez Resend: `RESEND_API_KEY` a `CONTACT_FROM` (formular@send.peakstudio.sk) sú nastavené vo Verceli, `CONTACT_TO` je voliteľné | `api/contact.js` |
| Samostatný finančný agent, v mene ktorého Martin koná (`[doplniť]`) | pätička v `index.html` |
| Adresa kancelárie | kontakt a pätička v `index.html` |
| Skutočné recenzie | `main.js` (`REVIEWS`) |

## Kde sa čo mení
- Farby a písmo: `style.css`, sekcia `:root`
- Fotky: `img/` (`martin-1200.webp`, `martin-720.webp` = hero, `martin-portrait.webp` = O mne, `og.jpg` = náhľad pri zdieľaní)

## Referencie
Sekcia „Čo hovoria klienti“ je skrytá, kým nie sú doplnené skutočné recenzie. Doplň ich do poľa `REVIEWS` v `main.js`
(`{ text: '…', name: 'Jana K.', place: 'Žilina' }`) a sekcia sa zobrazí sama.

## Kalkulačka
Stratégie Opatrná / Vyvážená / Dynamická (3 / 5 / 7 % ročne, 30 / 60 / 90 % akcií) sú ilustračné. Hodnoty sú v `index.html` v atribútoch `data-rate` a `data-stocks`, pred spustením ich treba prebrať s Martinom.

## MeruCompany
Martin pracuje pre MeruCompany, s. r. o. (IČO 52893511), podriadeného finančného agenta. Pred spustením pošli web na schválenie
compliance oddeleniu MeruCompany. Agenti mávajú pravidlá pre osobné weby (povinné údaje, používanie loga, označenie „finančný poradca“).

## Podstránky služieb
Každá služba má podstránku v priečinku `/<slug>/index.html` (napr. `hypoteky-a-uvery/`). Tieto súbory sa negenerujú ručne:
- obsah stránky je v `tools/pages/<slug>.html`, title a popis v `PAGES` v `tools/build_pages.py`,
- hlavička, kontakt a pätička sa preberajú z `index.html`,
- po akejkoľvek zmene spusti `python3 tools/build_pages.py`. Pregeneruje podstránky, menu Služby, pätičku aj `sitemap.xml`.

Nová podstránka = nový súbor v `tools/pages/` + záznam v `PAGES`. Kým súbor neexistuje, odkaz v menu vedie na sekciu Služby.

Texty väčšiny podstránok (refinancovanie, sporenie pre deti, dôchodok, poistenia, finančný plán) sú v `tools/service_pages.py`. Po úprave spusti `python3 tools/service_pages.py && python3 tools/build_pages.py`. Hypotéky a investovanie sú písané priamo v `tools/pages/`. Sklenené ilustrácie sú v `tools/glass/`, 3D mapa v `tools/make_map.py`, 3D cesta krokov v `tools/make_road.py`, ostrovčeky v sekcii životných etáp v `tools/make_life.py`.
Priečinok `tools/` sa na Vercel nenasadzuje (`.vercelignore`).
