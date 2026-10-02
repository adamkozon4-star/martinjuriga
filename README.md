# Martin Juriga – web finančného poradcu

Statický web (HTML + CSS + JS), bez buildu. Stačí otvoriť `index.html` alebo nasadiť priečinok.

## Nasadenie (Vercel)
*Add New Project* → import tohto repozitára → **Deploy**. Nič netreba nastavovať, web je v koreni repozitára.
Každý push do vetvy `main` sa nasadí automaticky. Vlastnú doménu pripojíš v *Settings → Domains*.

## Ešte treba doplniť
| Čo | Kde |
|---|---|
| Formulár: po prvom odoslanom dopyte príde na martin.juriga@merucompany.sk e-mail od FormSubmit, Martin klikne na potvrdenie (iba raz) | `main.js` (`FORM_EMAIL`) |
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
