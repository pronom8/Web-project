# Web-project Keskustelusovellus
Web project
Keskustelusovellus
Sovelluksessa näkyy keskustelualueita, joista jokaisella on tietty aihe. Alueilla on keskusteluketjuja, jotka muodostuvat viesteistä. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

- Sovelluksen ominaisuuksia:

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän.
- Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
- Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
- Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.
- Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
- Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
- Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.
- Käyttäjä voi päivittää oman profiilikuvansa haluamaansa profiili kuvaan.
- Käyttäjä voi vaihtaa käyttäjänimeänsä ja omaa sähköpostiansa mikäli uusi nimi tai sähköposti ei ole varattu 


# HUOM. Lisäsin sovellukseen joitakin muitakin toimintoja, joita ei lue aikaisemmassa suunitelmassani. 

# 2. HUOM. Jos huomaat että sinun täytyi ladata jotain riippuvuuksia mitä ei ollut dependencies.txt tiedostossa ilmoitathan siitä palautteessasi ja jaa ihmeessä oma tapasi miten sait sovelluksen toimimaan koneellasi (mikä käyttöjärjestelmä tietoon myös)

 # 3. huom. Muista rekistöröidä admin sisään jos haluat luoda topic pageen aiheita. Muuten sivu näkyy tyhjänä:
 - nimi: admin
 - sähköposti: admin@gmail.com
 - salasana: kunhan muistat sen
# JOS admin on jo luotu tässä tunnukset:
- nimi: admin
- sähköposti: admin@gmail.com
- salasana: 123





# Käynnistäminen
Clone this repository to your computer and go to its root folder

Create .env file with the following content:

- DATABASE_URL=<local-database-address>  
- SECRET_KEY=<secret-key>
- for example:
SECRET_KEY=9b1af21b123213d3b83288e3b4a3213b8c9af9
DATABASE_URL=postgresql://postgres:kukka321@localhost/postgres

Activate virtual environment and install requirements as follows:
- $ python3 -m venv venv     
- $ source venv/bin/activate 

Download all the dependecies -> more info below and check the Help for dependencies file.
pip install -r ./requirements.txt

Define the database schema:
- $ psql < schema.sql

flask run

___________________________________
if flask run does not work:
___________________________________
go to app.py file
run the file

if you are not able to run the file try typing into terminal: 
python app.py or try typing: flask run 

_____________________________________
if psycocg2 missing, try installing it again and restart VScode
if dotenv not working, try installing pip install python-dotenv
and after that try to run app.py
if that does not work restart code-editor
_____________________________________


# Downloading the dependencies: 

Lataa kaikki tarvittavat dependecies jotka lukee jokaisessa import statementissa ( esim VSCode ainakin näyttää että ei tunnista import from flask_bcrypt import Bcrypt jos ei ole ladannut flask_bcrypt:iä ) 

Kun olet ladannut kaikki tarvittavat niin käynnistä sovellus run run.py tiedostolla.

Yleensä tässä kohtaa terminaalissa saattaisi lukea mitä latauksia sinulta puuttuu jos on niitä. Toinen mistä huomaa on jos painelet eri juttuja sivulla niin voi heittää error pagelle jossa lukee mitä puuttuu (tai ei tunnisteta )
- Sovellusta voi testata oman tietokoneen luomalla serverillä. Paina ctrl + klickaa serverin osoitetta niin pääset sivulle.
- Voit pysäyttää serverin klikkaamalla terminaalia ja painamalla ctrl+c

# NYKYINEN TILANNE:

- Sovelluksen pitäisi toimia odotetusti niinkuin sovelluksen ominaisuuksia osiossa sanotaan. 



 HUOM. Salasanan uusimis toiminto on vaiheessa ja saattaa tai ei saata toimia jos laitat oman __init__.py tiedostossa
 app.config['MAIL_USERNAME'] = oma sähköposti
app.config['MAIL_PASSWORD'] = oman sähköpostin salasana.
ja olet antanut sähköpostillesi luvat vähemmän turvallisille sovelluksille. 





