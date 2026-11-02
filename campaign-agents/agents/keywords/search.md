# keyword: search — targeted lookup

Given a term (technique, flag, paper, notebook, game id):
1. Local first: `grep -ri` across `docs/`, `research/`, `references/`, `notebook-intel/`, `analysis/`, `references/sweeps/*/delta_cells.txt`.
2. Then the forum dump (`research/discussions/raw/*.json`) and the kernel listing (`references/sweeps/listing_*.json`).
3. Then the web (WebSearch/WebFetch) only for what the corpus does not have.
4. Answer in ≤ 15 lines with file paths / URLs; cache anything new under `research/search/<slug>.md`.
