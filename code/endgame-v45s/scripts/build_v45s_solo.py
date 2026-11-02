#!/usr/bin/env python3
"""Build v45s SOLO-LEG ENDGAME from the v44 mixture notebook.

v45s = v44 MINUS the 12h NVARC starter launch (cell 16 -> receipt) MINUS the
NVARC-only pip stack (cell 5 -> no-op) MINUS the GLM/swap levers (proven path
only), with the budget boxes shrunk to the 2.2h quota reality:
  - ARC_V44_TOTAL_BUDGET_H 5.5 -> 1.7   (rerun kill at T0+1h47m; 240 tasks x 1 sample)
  - ARC_V32_LEG27B_COMMIT_BOX_MIN 100 -> 40  (commit kill at T0+40m)
  - ARC_V32_LEG27B_COMMIT_TASKS -> 3 tasks (fast path validation only)
Cell 1's safety net already writes a schema-valid base submission.json
(identity attempt_1, flip attempt_2); the proven 27B leg (cells 31-33,
byte-identical) improves attempt_2 over that base, fail-open at the kill.
Everything not patched stays byte-identical vs v44 (merge contract untouched).
"""
import json, ast, sys, hashlib

SRC = "/home/z/my-project/arc/oct29_work/arc26-nvarc-v44-mixture.ipynb"
DST = "/home/z/my-project/arc/oct29_work/arc26-nvarc-v45s-solo.ipynb"

nb = json.load(open(SRC))
src0 = json.dumps(nb)

def cell_text(i):
    return "".join(nb["cells"][i]["source"])

def set_cell(i, text):
    nb["cells"][i]["source"] = text.splitlines(keepends=True)

def patch(i, old, new, label):
    t = cell_text(i)
    if old not in t:
        print(f"FAIL: anchor not found in cell {i} ({label})")
        sys.exit(1)
    if t.count(old) != 1:
        print(f"FAIL: anchor not unique in cell {i} ({label})")
        sys.exit(1)
    set_cell(i, t.replace(old, new))
    print(f"patched cell {i}: {label}")

# --- cell 0: title line ------------------------------------------------------
t = cell_text(0)
lines = t.splitlines(keepends=True)
assert lines[0].startswith("# ARC26 NVARC v44"), f"cell 0 line 0 unexpected: {lines[0][:60]}"
lines[0] = ("# ARC26 NVARC v45s — SOLO 27B-LEG ENDGAME (no NVARC run: cell-1 safety-net base + "
            "proven leg; boxes shrunk to the 2.2h weekly GPU quota; merge contract untouched)\n")
set_cell(0, "".join(lines))
print("patched cell 0: title")

# --- cell 3: budget boxes ----------------------------------------------------
patch(3, '"ARC_V44_GLM": "1",', '"ARC_V44_GLM": "0",', "GLM swap OFF (proven path only)")
patch(3, '"ARC_V44_TOTAL_BUDGET_H": "5.5",', '"ARC_V44_TOTAL_BUDGET_H": "1.6",', "rerun budget 1.6h")
patch(3, '"ARC_V44_MIXTURE": "1",', '"ARC_V44_MIXTURE": "0",', "mixture counters inert")
patch(3, '"ARC_V32_LEG27B_COMMIT_BOX_MIN": "100",', '"ARC_V32_LEG27B_COMMIT_BOX_MIN": "40",', "commit box 40 min")
patch(3,
      '"ARC_V32_LEG27B_COMMIT_TASKS": "0934a4d8 136b0064 16de56c4 20270e3b 31f7f899 3dc255db 409aa875 7b3084d4 8f215267 b99e7126 d35bdbdc e376de54",',
      '"ARC_V32_LEG27B_COMMIT_TASKS": "0934a4d8 136b0064 16de56c4",',
      "commit tasks -> 3")

# --- cell 4: tensorflow uninstall -> no-op -----------------------------------
set_cell(4, "# v45s solo: tensorflow uninstall not needed (NVARC stack skipped).\n"
            "print('[v45s solo] cell 4 no-op', flush=True)\n")
print("patched cell 4: no-op")

# --- cell 5: NVARC pip stack -> no-op ----------------------------------------
set_cell(5, "# v45s solo: NVARC's cp312 wheel install skipped (no starter.py run; the 27B leg\n"
            "# brings its own isolated vLLM stack from the wheelhouse mount, as in every v32+ run).\n"
            "print('[v45s solo] cell 5 no-op (leg self-bootstraps its wheels)', flush=True)\n")
print("patched cell 5: no-op")

# --- cell 16: the 12h starter launch -> solo receipt --------------------------
set_cell(16, (
    "# v45s SOLO: the 12h NVARC starter launch is REMOVED (quota endgame: 2.2h/week left,\n"
    "# a 12h run can never fit). Cell 1's safety net already wrote the base submission.json\n"
    "# (identity attempt_1, flip attempt_2). The proven 27B leg (cells 31-33, byte-identical)\n"
    "# improves attempt_2 over that base, fail-open at its kill-switch.\n"
    "import os as _solo_os, json as _solo_json\n"
    "with open('/kaggle/working/submission.json') as _solo_f:\n"
    "    _solo_base = _solo_json.load(_solo_f)\n"
    "_solo_n = sum(len(v) for v in _solo_base.values())\n"
    "print(f\"[v45s solo] NVARC skipped; base submission.json: {len(_solo_base)} tasks / {_solo_n} outputs \"\n"
    "      f\"(rerun={bool(_solo_os.getenv('KAGGLE_IS_COMPETITION_RERUN'))})\", flush=True)\n"
))
print("patched cell 16: starter launch -> solo receipt")

# --- static checks ------------------------------------------------------------
# Strict AST only for the cells THIS build patched; inherited cells are proven
# by real v44-family runs (several carry IPython magics that pure ast rejects).
PATCHED = (0, 3, 4, 5, 16)
nb44 = json.load(open(SRC))
n_ast = 0
for i, c in enumerate(nb["cells"]):
    if c["cell_type"] != "code":
        continue
    src = "".join(c["source"])
    if src.startswith("!"):
        continue
    body = src.split("\n", 1)[1] if src.startswith("%%writefile") else src
    try:
        ast.parse(body)
        n_ast += 1
    except SyntaxError:
        if i in PATCHED:
            print(f"FAIL: AST on PATCHED cell {i}")
            sys.exit(1)
        same = json.dumps(nb44["cells"][i]) == json.dumps(nb["cells"][i])
        if not same:
            print(f"FAIL: cell {i} fails AST and is NOT byte-identical to v44")
            sys.exit(1)
        print(f"note: cell {i} has IPython magics (skipped AST; byte-identical to proven v44)")
print(f"AST OK: {n_ast} code cells parsed strict")

# byte-identity of untouched cells vs v44
nb44 = json.load(open(SRC))
ident = sum(1 for i in range(len(nb44["cells"]))
            if json.dumps(nb44["cells"][i]) == json.dumps(nb["cells"][i]))
print(f"byte-identical cells vs v44: {ident}/{len(nb44['cells'])} (patched: 0,3,4,5,16)")

# forbidden tokens (no credentials, no cross-account references in kernel text)
import re
blob = json.dumps(nb)
for bad in ("KGAT_", "ghp_", "uradkr", "koushik", "kragglenote", "dasshovon"):
    if bad in blob:
        print(f"FAIL: forbidden token '{bad}' present in notebook text")
        sys.exit(1)
if re.search(r"hf_[A-Za-z0-9]{20,}", blob):
    print("FAIL: HF-token-shaped string present in notebook text")
    sys.exit(1)
print("forbidden-token sweep: clean")

json.dump(nb, open(DST, "w"))
h = hashlib.sha256(open(DST, "rb").read()).hexdigest()
import os
print(f"WROTE {DST} ({os.path.getsize(DST)} chars) sha256={h[:16]}")
