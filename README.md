# Tietokannat-ja-web-ohjelmointi-harjoitustyo

## Loppupalautus

### Käyttöönotto:

Repositoirion juurihakemistossa tulee ajaa komennot
 - 'python3 -m venv venv'
 - 'source venv/bin/activate'
 - 'pip install -r requirements.txt'
 - 'psql < schema.sql'

'run flask' pitäisi ohjelman lähteä käyntiin, jonka jälkeen voi localhostissa ajaa ohjelmaa paikallisesti

### Ohjelman tila:

Ohjelma täyttää vaatimusmäärittelyn

### Aihe/vaatimusmäärittely

Valitsisin aiheekseni keskustelusovelluksen. Esimerkkiaiheen mukaisesti toiminnoiksi tuotan seuraavat:
 - Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
 - Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan.
 - Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
 - Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
 - Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.
 - Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
 - Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
 - Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.

