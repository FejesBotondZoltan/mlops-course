4.
logreg-C=0.01              f1=0.5047  roc_auc=0.8208
  logreg-C=0.1               f1=0.5714  roc_auc=0.8301
  logreg-C=1.0               f1=0.5785  roc_auc=0.8320
  logreg-C=10.0              f1=0.5785  roc_auc=0.8318
  rf-n_estimators=100        f1=0.6066  roc_auc=0.8161
  rf-n_estimators=300        f1=0.6240  roc_auc=0.8172
  
Nem, A közel jövőben jobb modell jöhet létre amit esetleg jobbban preferálunk

data_path

6.
Nyomkövetési lánc (Traceability chain): Az alias feloldásához a client.get_model_version_by_alias("diabetes-classifier", "staging"),
a futás lekéréséhez a client.get_run(run_id),
a Git-commit eléréséhez a futási metaadatok/tagek ellenőrzése, a forráskódhoz pedig a git checkout <commit_hash> hívás szükséges.

Alias előnyei a fix szakaszokkal (stages) szemben: Az aliasok lehetővé teszik a teljesen tetszőleges,
testreszabható elnevezések használatát (pl. @champion, @challenger),
valamint egyetlen modellverzióhoz egyszerre több különböző alias is hozzárendelhető.

A lánc vége (data/diabetes.csv): Ez azt jelenti, hogy a metrikák reprodukálhatósága nem garantált,
mivel a helyi fájl módosulhat vagy törlődhet anélkül, hogy a változást követnénk.
A rés áthidalásához verziózott adathalmaz-kezelő eszközre (pl. DVC) vagy az adathalmaz pontos hash-értékének/lenyomatának MLflow-ban történő naplózására van szükség.