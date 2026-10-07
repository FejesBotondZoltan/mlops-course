2\. feladat

a)

Hozzá kell adni a szerződéshez.

Kinek kell megegyezniük:
-Az adatküldő fél (klinika)

\-Mérnök csapat



b)

1. \- extra oszlop

&#x09;sor: -

&#x09;Oszlop: notes

&#x09;Hibás érték: -

2\. - nem numerikus

&#x09;sor: 4

&#x09;Oszlop: glucose

&#x09;Hibás érték: unknown

3\. - tartomány kívüli

&#x09;sor: 24

&#x09;Oszlop: bmi

&#x09;Hibás érték: 280

4\. - tartomány kívüli

&#x09;sor: 8

&#x09;Oszlop: age

&#x09;Hibás érték: 250



A glucose=unknown: nem tudta az "unknown"-t float-ra alakítani ezért nem is lett az expected type (2,3) és a két tartomány ellenőrzés ugyan ezért elszállt.



4\. feladat

a)

\-A data/processed/train.csv (az md5 hash meg is változott d9eba76c-ról 267b4f5e-re), aztán a betanított modellfájlba, a kiértékelés eredményébe.

\-éles környezetben a hibás adatokra tanult modell rosszul teljesít, a kiértékeléssel szemben is.

b)

\_require\_validated

c)

validate: lefut -> dvc.yaml deps: schemas.py

prepare: skipped -> a validáció kimenete nem változott ettől mert nem volt 120 és 125 éves közötti sor.

train:  skipped -> dvc.yaml deps: schemas.py

evaluate: lefut -> dvc.yaml deps: schemas.py és új model.pkl miatt

