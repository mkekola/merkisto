<img src="./static/images/merkisto_logo.png" alt="Merkistö Logo" width="400"/>
<br/>

# Merkistö - Haalarimerkkikirjasto
*HY Tietokannat ja web-ohjelmointi-kurssin projektityö: Haalarimerkkikirjasto*

## Sovelluksen toiminnallisuudet
- [x] Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- [x] Käyttäjä pystyy lisämään, muokkaamaan ja poistamaan haalarimerkkejä sovelluksessa.
- [x] Käyttäjä pystyy näkemään sovellukseen lisätyt merkit sekä niiden tiedot.
- [x] Käyttäjä pystyy hakemaan merkkejä niiden nimen tai kuvauksen perusteella.
- [x] Haalarimerkeille pystyy lisäämään tietoja, esimerkiksi mistä saatu/ostettu tieto.
- [X] Käyttäjä pystyy lisäämään kuvia lisätyille merkeille.
- [X] Käyttäjä voi lisätä kategorioita merkeille.
- [X] Käyttäjäprofiilissa näkyy käyttäjän lisäämät merkit.
- [ ] Käyttäjä pystyy kommentoimaan ja tykkäämään omista sekä muiden lisäämistä merkeistä.

## Sovelluksen asennusohjeet
1. Kloonaa repositorio paikalliselle koneellesi suorittamalla komento:
   ```git clone https://github.com/mkekola/merkisto.git```
2. Siirry projektin juurihakemistoon suorittamalla komento:
   ```cd merkisto```
3. Luo ja aktivoi virtuaaliympäristö suorittamalla komennot:
   ```python -m venv venv```
   ```source venv/bin/activate```
4. Asenna riippuvuudet:
   ```pip install flask```
5. Alusta tietokannat suorittamalla komennot:
   ```sqlite3 database.db < schema.sql```
   ```sqlite3 database.db < init.sql```
6. Käynnistä sovellus suorittamalla komento:
   ```flask run```

## Sovelluksen käyttöohjeet
1. Avaa selain ja siirry osoitteeseen `http://127.0.0.1:5000/` nähdäksesi sovelluksen käyttöliittymän.
2. Luo käyttäjätili ja kirjaudu sisään.
3. Lisää, muokkaa tai poista haalarimerkkejä.
4. Hae merkkejä nimen tai kuvauksen perusteella.
5. Lisää kuvia ja kategorioita merkeille.
6. Kommentoi merkkejä ja tarkastele muiden käyttäjien profiileja.