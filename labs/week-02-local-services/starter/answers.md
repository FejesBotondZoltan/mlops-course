4.
MinIO-ban mert struktúrálatlan adat amit nem akarunk/lehet querries-ni csak letölteni esetekben.
Ezért itt tároljuk mert ez "olcsóbb" és gyorsabb.

5.
comparability: MLflow-val könnyen összehasonlíthatjuk a különböző modellek teljesítményeit.
shareability: Postgres és MinIO-ban tárolt adatokat könnyen megtudjuk osztani akár egy csapattal is.
reproducibility: Minden futáshoz fix run_uuid tartozik ami alapján mindig visszalehet fejteni a model
bemenetetét, kimenetét illetve környezeti függőségeit.
