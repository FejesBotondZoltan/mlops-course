2\. Feladat

a)

Git: A data/raw/batch\_01.csv adat fájlt, data/.gitignore és data/measurements.csv.dvc. Kb: 100-150 bájt

MinIO: A teljes adathalmazt (19 034 bájt) az MD5 hash útvonalán

DVC: A nagy adathalmazokkal nem a gitet terheljük hanem az erre tervezett MinIO-val tároljuk



b)

build-measurement: Azonos .dvc fájl és az indexek elhagyása(index=False) esetén igaz, de a windows alapértelmezett sorvégjelölése használata elrontja.



c)

"uv run dvc pull"

Minio kulcsokkal rendelkezzen és



4\. Feladat

a)

Git chekcout: Visszaállította a data/measurements.csv.dvc-t az 1. verzió állapotára

Dvc Checkout: A local cache-ből betölti az 1.verziót

A Git csak a mutatót kezeli verzió szerint az adatot nem látja, viszont a DVC nem tudná a gittel tárolt mutató nélkül hogy melyik verziót töltse be.



b)

git checkout lefut, de a dvc checkout hibaüzenetet kap mert nem találja a local cache-ben.



5\. Feladat

a)
deps:

&#x20;     - data/processed/test.csv

&#x20;     - models/model.pkl

&#x20;     - models/mlflow\_run\_id.json

&#x20;     - src/week\_04\_dvc\_introduction/pipeline.py

&#x20;     - src/week\_04\_dvc\_introduction/model.py

model.pkl törlés estén a pipeline nem dob hibát, sikeresen lefut de elavult eredményt ad.



b)

A batch\_01, batch\_02, batch\_03 összefűzése miatt a sorok más sorrendben vannak és így lényegében olyan mint ha más seed-el történt volna.



6\. Feladat

a)

MLflow digest: Az adattábla oszlopnevei, sor száma és az első 10 000 sor értékeit

DVC md5: A teljes fájl nyers bájtjait hasheli

A DVC md5-öt kell adni, mert ez bizonyítja a betanított bájtok egyezését

MLflow digest haszna: Gyors ellenőrzés arra, hogy a táblázat tartalma megegyezik-e, de nem biztosítja a pontos egyezést ezért a Windows (CRLF) és Linux (LF) különbségem nem akad fent.



b)

tags.dvc\_md5 = 'a8fd7b4f0d6d1bc4e378a8f76c5fff0c'

Melyik esetekben használtuk pontosan ezt az adatverziót.



