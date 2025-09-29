# O projektu
V tem prjektu bom naredila...

How to install requests on my computer
or any other packages
just replace the name requests.
```
py -m pip install requests
```

# TODOS
- [ ] TODO: Analiziraj podatke od animejev. Podatki so shranjeni v datoteki anime_data_premium.csv
- [ ] Anime type
1. ONA najbolj gledan od TV in OVA.
2. Razlika med end date in start datom pomeni da ima več ogledov.
3. Razlika med end date in start datom pomeni da ima višjo oceno.
6. Več epizod višja ocena.
8. Katero leto je najbolj gledan?
9. Katero leto ima najboljšo oceno?
10. Death note je v 1% animejev po oceni.
11. Najboljši studio po oceni.
12. Več animejev za male fantke kot za punčke.
13. Romantični animeji so za punčke.
14. Histogram po oceni. Torta tudi opcija.
15. Krajši animeji imajo manj gledalcev. Krajša epiza.
16. Diagram po žanrih in gledanosti in oceni.
17. Najbolj popularen anime za ženske.
18. Kateri žanri se pojavio med animeji, ki imajo demografiko odrasle ženske.
19. Povprečne oceno odvisne od letnega časa premiere.
20. Gledanost odvisna od letnega časa premiere.
21. **Vir zgodbe vpliva na oceno/gledanost** (Source: Manga, Light Novel, Original, Game, Web manga, …)
    * Test: Kruskal–Wallis (Score/ Members po `Source`), Dunn + FDR.
22. **TV vs Movie vs ONA/OVA – razlike v oceni/gledanosti** (razširi A).
    * Test: Kruskal–Wallis; parne Dunn.
23. **Razmerje Favorites/Members (engagement) po žanrih/studijih.**
    * Metrično: `engagement_ratio = Favorites / Members`.
    * Testi po žanrih/studijih; graf: stolpične.
24. **Starost naslova in gledanost:** starejši (več let od `Start Date`) imajo več/ manj Members?
    * Test: Spearman (years\_since\_start vs Members).
25. **Sequel/continuation učinek (če imaš polje v `Name` ali `Link` za nadaljevanja)**
    * Npr. naslovi z “2nd Season”, “S2” ipd. → ali imajo drugačen `Score`/`Members` kot originale?
26. **Multipli žanri (žanrska širina) vs ocena/gledanost:**
    * `num_genres = len(genres_list)`.
    * Test: Spearman z `Score` in `Members`.
27. **Dolžina epizode (`Duration`) vs `Score` in `Members`.**
    * Pogosto kratke (3–5 min) “shorts” imajo drugačne metrike.
28. **Broadcast (npr. timeslot) vpliv** (če je polje čisto):
    * “Saturdays 17:00 (JST)” ipd. → izlušči dan v tednu in uro; testiraj razlike.
29. **Demografija × Žanr interakcije:**
    * Npr. ali je “Romance” v **Shoujo** bistveno bolj gledan kot “Romance” v **Seinen**?
    * Test: 2-way ANOVA (če norm. predpostavke), sicer stratificirane primerjave + Dunn.
30. **Studio stabilnost:**
    * Ali ima studio nizko varianco `Score` (konsistentna kakovost) v primerjavi z drugimi?
    * Test: Levene/Brown–Forsythe za varianco; graf: “error bars”.

Rank
Score
Name
ID
Link
Type
Episodes
Start Date
End Date
Status
Premiered
Broadcast
Producers
Licensors
Studios
Source
Genres
Demographics
Duration
Rating
Popularity
Members
Favorites

- [x] complete get_data.py. Get all the neded data from the website.


### A) “ONA najbolj gledan od TV in OVA.”

* **H0:** Mediana `Members` (ali povprečje log1p(Members)) je enaka za `Type ∈ {ONA, TV, OVA}`.
* **H1:** vsaj ena se razlikuje; posebej te zanima `ONA > TV` in `ONA > OVA`.
* **Test:** Kruskal–Wallis (neparametrično); nato **Dunn** parne primerjave z FDR.
* **Graf:** box/violin + swarm za `log1p(Members)` po `Type`.

### B) “Razlika med end in start datom pomeni več ogledov.”

* **H0:** Korelacija med `duration_days` in `Members` = 0.
* **H1:** Korelacija ≠ 0 (ali > 0, če želiš enostransko).
* **Test:** Spearman ρ (robusten na nelinearnost).
* **Graf:** scatter `duration_days` vs `log1p(Members)` + LOWESS.

### C) “Razlika med end in start datom pomeni višjo oceno.”

* Kot B), le da odvisna spremenljivka `Score`.
* **Test:** Spearman ρ; po želji robustna linearna regresija `Score ~ duration_days + Type + year + genres (one-hot)`.
* **Graf:** scatter `duration_days` vs `Score`.

### D) “Povprečni čas za izdelavo epizode vs ocena.”

* `airing_length_per_ep = duration_days / Episodes`.
* **H0:** ρ(`airing_length_per_ep`, `Score`) = 0.
* **Test:** Spearman ρ; alternativno regresija `Score ~ airing_length_per_ep + Episodes + Type + year`.
* **Graf:** scatter `airing_length_per_ep` vs `Score`.

### E) “Več ogledov → višja ocena.”

* **H0:** ρ(`Members`, `Score`) = 0.
* **Test:** Spearman ρ; ali regresija `Score ~ log1p(Members) + Type + year + genres`.
* **Graf:** scatter `log1p(Members)` vs `Score`.

### F) “Več epizod → višja ocena.”

* **H0:** ρ(`Episodes`, `Score`) = 0.
* **Test:** Spearman ρ; regresija z nadzori, ker serije z veliko epizod pogosto spadajo v specifične žanre/demografije.
* **Graf:** scatter `Episodes` vs `Score` (morda log x-os, če zelo razpršeno).

### G) “Kateri žanr je najbolj gledan?”

* **Metodologija:** za vsak žanr izračunaj **mediano** ali **trimmed mean** `log1p(Members)`; ker je multi-label, šteje anime v vse svoje žanre.
* **Test:** Kruskal–Wallis čez žanre; parne Dunn + FDR.
* **Graf:** rangirana stolpična za `median log1p(Members)` po žanru.

### H) “Katero leto je najbolj gledano?”

* **Metodologija:** agregiraj po `year` (iz Start Date ali Premiered).
* **Test:** Kruskal–Wallis (če primerjaš več let) ali izračun rangirane mediane/povprečja.
* **Graf:** črta: year vs `median log1p(Members)`.

### I) “Katero leto ima najboljšo oceno?”

* Enako kot H), le metrika `Score`.
* **Test/Graf:** kot H).

### J) “Death Note je v top 1% po oceni.”

* **H0:** `Score(Death Note) < p99(Score)` (ali ≤).
* **Postopek:** izračunaj `p99 = Score.quantile(0.99)` in primerjaj. Enostavno poročilo.

### K) “Najboljši studio po oceni.”

* **Metodologija:** za vsak studio izračunaj `mean/median Score`; filtriraj studije z npr. **min N >= 5** animejev, da se izogneš šumu.
* **Test:** Kruskal–Wallis; parne Dunn + FDR.
* **Graf:** rangirana stolpična (top N studiev).

### L) “Več animejev za ‘male fantke’ kot za ‘punčke’.”

* Predpostavka: **Shounen** (fantje) vs **Shoujo** (dekleta).
* **H0:** Število Shounen = Število Shoujo.
* **Test:** χ² test za frekvence (kontingenčna tabela).
* **Graf:** stolpična primerjava count(Shounen) vs count(Shoujo).

### M) “Romantični animeji so za punčke.”

* Operacionalizacija: Romantika ∈ `Genres` in demografija ∈ {Shoujo, Josei} vs {Shounen, Seinen, ostalo}.
* **H0:** Delež romantičnih v ženskih demografijah = delež v drugih.
* **Test:** χ² test neodvisnosti (Genres×Demographics).
* **Graf:** mozaik/stacked bar.

### N) “Histogram po oceni. Torta tudi opcija.”

* **Graf:** histogram `Score` (n=velik → raje histogram + KDE). “Torta” le za deleže kategorij (npr. Type, Demographics), ne za Score.

### O) “Krajši animeji imajo manj gledalcev. Krajša epizoda.”

* Razdeli na:

  * **Krajši anime**: manj `Episodes` ali manj `duration_days`.
  * **Krajša epizoda**: `Duration` na epizodo (min).
* **H0:** ρ(`Episodes`, `Members`) = 0 in ρ(`Duration per ep`, `Members`) = 0.
* **Test:** Spearman; po želji binariziraj (kratko/dolgo) in Mann–Whitney U.
* **Graf:** scatter + boxploti.

### P) “Diagram po žanrih in gledanosti in oceni.”

* **Graf:** mehurčkast graf (x=`median Score` žanra, y=`median log1p(Members)`, velikost=št. naslovov). Alternativa: facet grid po sezonah ali demografijah.

### Q) “Najbolj popularen anime za ženske.”

* Definiraj “za ženske” kot demografiji **Josei** ali **Shoujo**.
* **Metodologija:** filtriraj `Demographics ∈ {Josei, Shoujo}`, rangiraj po `Members` (ali `Favorites`).
* **Poročaj:** top 10.

### R) “Kateri žanri se pojavljajo med animeji z demografiko odrasle ženske (Josei).”

* Filtriraj `Demographics` vsebuje **Josei**; nato šteješ pogostost `Genres`.
* **Graf:** rangirana stolpična pogostosti.

### S) “Povprečne ocene odvisne od letnega časa premiere.”

* **H0:** Distribucije `Score` so enake čez `season ∈ {Winter, Spring, Summer, Fall}`.
* **Test:** Kruskal–Wallis; parne Dunn + FDR.
* **Graf:** box/violin po sezonah.

### T) “Gledanost odvisna od letnega časa premiere.”

* Enako kot S), a metrika `log1p(Members)`.
