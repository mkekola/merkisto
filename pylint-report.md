# Pylint-raportti
```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:13:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:24:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:31:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:36:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:44:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:54:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:65:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:71:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:86:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:122:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:142:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:157:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:184:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:203:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:214:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:258:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:277:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:281:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:296:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:296:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:313:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:14:4: E0237: Assigning to attribute 'last_insert_id' not defined in class slots (assigning-non-slot)
db.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module patches
patches.py:1:0: C0114: Missing module docstring (missing-module-docstring)
patches.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
patches.py:14:0: C0116: Missing function or method docstring (missing-function-docstring)
patches.py:25:0: C0116: Missing function or method docstring (missing-function-docstring)
patches.py:29:0: C0116: Missing function or method docstring (missing-function-docstring)
patches.py:33:0: C0116: Missing function or method docstring (missing-function-docstring)
patches.py:38:0: C0116: Missing function or method docstring (missing-function-docstring)
patches.py:42:0: C0116: Missing function or method docstring (missing-function-docstring)
patches.py:46:0: C0116: Missing function or method docstring (missing-function-docstring)
patches.py:57:0: C0116: Missing function or method docstring (missing-function-docstring)
patches.py:61:0: C0116: Missing function or method docstring (missing-function-docstring)
patches.py:69:0: C0116: Missing function or method docstring (missing-function-docstring)
patches.py:82:0: C0116: Missing function or method docstring (missing-function-docstring)
patches.py:93:0: C0116: Missing function or method docstring (missing-function-docstring)
patches.py:103:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:9:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:13:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:18:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 8.39/10 (previous run: 8.39/10, +0.00)
```

## Yhteenveto

### Docstringit puuttuvat

Suurin osa Pylintin raportoimista ongelmista liittyy puuttuviin docstringeihin moduuleissa ja funktioissa.

```
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:13:0: C0116: Missing function or method docstring (missing-function-docstring)
```

Sovelluksen kehityksessä on tehty tietoisesti päätös, ettei käytetä docstring-kommentteja.

### Puuttuva palautusarvo

```
app.py:296:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
```

Funktion dekoraattorissa on vaatimus, että metodin tulee olla `GET` tai `POST`, joten tässä tapauksessa ei ole riskiä, että funktio ei palauta arvoa.

### Vakion nimi

```
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
```

Sovelluksen kehittäjän näkemyksen mukaan tässä tilanteessa näyttää paremmalta, että muuttujan nimi on pienillä kirjaimilla.

### Vaarallinen oletusarvo

```
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
```
Tässä tapauksessa oletusarvoina käytetään tyhjiä listoja. Tämä ei haittaa, koska koodi ei muokkaa kyseisiä listoja.

### Määrittelemätön attribuutti

```
db.py:14:4: E0237: Assigning to attribute 'last_insert_id' not defined in class slots (assigning-non-slot)
```
Tässä tapauksessa attribuutti määritellään dynaamisesti, joten Pylint ei pysty havaitsemaan sitä etukäteen.