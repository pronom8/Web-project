# Web-project
Web project
Keskustelusovellus
Sovelluksessa näkyy keskustelualueita, joista jokaisella on tietty aihe. Alueilla on keskusteluketjuja, jotka muodostuvat viesteistä. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

Sovelluksen ominaisuuksia:

Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan.
Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.
Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.
Käyttäjä voi päivittää oman profiilikuvansa haluamaansa profiili kuvaan.


# HUOM. Lisäsin sovellukseen joitakin muitakin toimintoja, joita ei lue aikaisemmassa suunitelmassani. 


# TESTI OHJEET: 

Lataa kaikki tarvittavat dependecies jotka lukee jokaisessa import statementissa ( esim VSCode ainakin näyttää että ei tunnista import from flask_bcrypt import Bcrypt jos ei ole ladannut flask_bcrypt:iä ) 

Kun olet ladannut kaikki tarvittavat niin käynnistä sovellus run run.py tiedostolla.
Yleensä tässä kohtaa terminaalissa saattaisi lukea mitä latauksia sinulta puuttuu jos on niitä. Toinen mistä huomaa on jos painelet eri juttuja sivulla niin voi heittää error pagelle jossa lukee mitä puuttuu (tai ei tunnisteta )
- Sovellusta voi testata oman tietokoneen luomalla serverillä. Paina ctrl + klickaa serverin osoitetta niin pääset sivulle.
- Voit pysäyttää serverin klikkaamalla terminaalia ja painamalla ctrl+c 


# NYKYINEN TILANNE:
Keskeiset toiminnot kuten rekistöröityminen ja kirjautuminen toimii
myöskin se että käyttäjä voi luoda postauksia, muokata omia postauksia ja poistaa oman postauksensa.
Sovellus päivittää automaattisesti uusimmat päivitukset ensimmäiseksi. Klikkaamalla toisen päivitystä pääsee toisen profiiliin josta voi nähdä hänen päivityksensä uusimmasta vanhimpaan järjestyksessä sekä päivityksien määrän. 
Käyttäjä näkee postauksien päivämäärät. 
Käyttäjä voi päivittää oman profiilikuvansa haluamaansa profiili kuvaan.
Sovelluksen ulkoasu on näiltä osin valmis. 
Sovellus tällä hetkellä tukeutuu sql alchemyyn eikä olla integroitu vielä SQL komentoja kunnolla. 


 HUOM. Salasanan uusimis toiminto on vaiheessa ja saattaa tai ei saata toimia jos laitat oman __init__.py tiedostossa
 app.config['MAIL_USERNAME'] = oma sähköposti
app.config['MAIL_PASSWORD'] = oman sähköpostin salasana.
ja olet antanut sähköpostillesi luvat vähemmän turvallisille sovelluksille. 





