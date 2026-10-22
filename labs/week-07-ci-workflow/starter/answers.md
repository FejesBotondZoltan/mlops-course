https://github.com/FejesBotondZoltan/mlops-course/actions/runs/39761462652

https://github.com/FejesBotondZoltan/mlops-course/actions/runs/39763868002

1.
a) \
Minden push, pull request, workflow dispatch esetén ellenőrzi a függőségeket és futtatja az adott laborhoz tartozó teszteket\
b) \
Minden 'labs/*/starter' és 'labs/*' mappában, ami tartalmaz 'pyproject.toml' fájlt.
-'uv lock --check'
-'uv sync --locked --all-groups'
-'uv run --frozen pytest -q'
\

5.
a) \
közös: Mindkettő ugyanazt az adat-előkészítési, tanítási és kiértékelési kaput futtatja \
különbség: A CI kódváltozásra indul, és futtat lintelést és tesztrétegeket. A CT időzítve vagy kézzel fut, kódmódosítás és tesztek nélkül.

b) \
A futtató környezet izolált, és a kapu `GO` döntése szükséges, de nem elégséges feltétel: nem pótolja az üzleti validációt és az emberi döntéshozatalt a kiadás előtt.

c) \
A GitHub Actions az ingyenes vagy túlterhelt kapacitás függvényében elhalaszthatja vagy eldobhatja az ütemezett futásokat.