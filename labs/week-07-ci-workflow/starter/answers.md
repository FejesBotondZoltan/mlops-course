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

