# O projektu
Projekt analizira podatke o najbolje ocenjenih animejih, pridobljenih iz [MyAnimeList](https://myanimelist.net/).

# Kako zagnati
Za pridobivanje podatkov je potrebno zagnati datoteko `get_data.py`.  
Na dnu datoteke je definirano, koliko animejev se prenese, npr.:

```python
dump_data(total_number_of_anime=100)
```

Analizo podatkov izvede datoteka `analize_data.ipynb`. Možno je zagnati vsako celico posebej.

V repozitoriju je tudi CSV datoteka anime_data_premium_6000.csv, ki vsebuje podatke za 6000 animejev.