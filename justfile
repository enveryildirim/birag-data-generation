# BıRAG — komut kısayolları. Bkz. plan.md §10, §11.
# just kurulumu: uv tool install rust-just (brew değil — bkz. PROJECT_MEMORY oturum notu)
# duckdb kurulumu: bin/duckdb (docker wrapper — brew değil)

default:
    @just --list

# Bağımlılıkları senkronize et
install:
    uv sync

# configs/taxonomy.yaml kapsama raporu (Faz 1)
normalize FILE:
    uv run python src/normalize.py {{FILE}}

# Deterministik kapılar — tek dosya üzerinde (Faz 2+)
check FILE:
    uv run python src/checks.py {{FILE}}

# DuckDB CLI (docker wrapper)
duckdb *ARGS:
    ./bin/duckdb {{ARGS}}
