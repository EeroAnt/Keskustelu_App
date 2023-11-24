# Tietokannat-ja-web-ohjelmointi-harjoitustyo

## Välipalautus 2

Repositoirion juurihakemistossa tulee ajaa komennot
 - 'source venv/bin/activate'
 - 'pip install -r requirements.txt'
 - 'psql < schema.sql'

'run flask' pitäisi ohjelman lähteä käyntiin, jonka jälkeen voi localhostissa ajaa ohjelmaa paikallisesti

Tällä hetkellä sovellus on ruma, mutta perustoiminnaillisuuden rankaa on. 
 - Käyttäjän luominen ja kirjautuminen onnistuu. Sovelluksen kautta luodessa käyttäjän admin-status on aina false. Admin käyttäjän luominen tapahtuu tällä hetkellä erillisellä INSERT-komenolla, jossa asetetaan admin = TRUE. En tiedä onko tämä hyvä tapa, mutta se on tapa tällä hetkellä.
 - admin voi luoda keskustelualueita
 - käyttäjä voi avata keskustelun keskustelualueelle
 - käyttäjä voi muokata avaamansa keskustelun otsikon tai poistaa keskustelun kokonaan
 - käyttäjä voi lisätä viestin keskusteluun
 - käyttäjä voi muokata tai poistaa omia viestejään

## Aihe/vaatimusmäärittely

Valitsisin aiheekseni keskustelusovelluksen. Esimerkkiaiheen mukaisesti toiminnoiksi tuotan seuraavat:
 - Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
 - Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan.
 - Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
 - Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
 - Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.
 - Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
 - Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
 - Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.

