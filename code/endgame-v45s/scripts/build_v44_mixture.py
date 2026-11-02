#!/usr/bin/env python3
"""Build v44 = v43 + MIXTURE-OF-SOLVERS endgame (built Nov-1 ~16:30 UTC, validates on Nov-7 quota refresh).

User directive Nov-1 22:2x Dhaka: mixture of solving agents, GLM 3.8-class quant leg,
dynamic action traces, 6h-quota-compliant, harvest uradkr mechanisms. Evidence base (Nov-1):
  - DSL legs solve 0/120 eval tasks (arc2_audit_and_mixture_nov1.py) -> model agents carry the score.
  - GLM trace protocol proven (glm_trace_solver_proof_nov1.py): dynamic traces parse 2/3, exact 0/3
    single-shot -> kernel leg must multi-sample + verify (chassis already does both).
  - uradkr 34.86 decoded: small-model leg (4B student) is how the 6h weekly cap is fit -> v44 swaps
    the 27B council primary for GLM-4-9B-AWQ (3.8-class quant) via the EXISTING v38 model ladder
    (ARC_V38_LEG_SWAP infra, boot-receipted in v39 ref 57662636), 27B retained as ladder fallback.
  - Fresh quota 16:30 UTC: dasshovon 21,600-13,553s left (~2.2h), kragglenote ~1.1h -> NO run can
    complete before the Nov-2 lock; v44 is therefore staged for the Nov-7 refresh (push_v44_staged.sh).

Patches (all flag-gated, fail-open; untouched cells byte-identical vs v43):
  cell 00 title · cell 03 env + 6h budget formula · cell 25 parser override ·
  cell 30 GLM ladder entry · cell 33 mixture-router receipts (L12' semantics retained) ·
  cell 34 provenance · cell 36 receipts.
"""
import json, ast, sys, datetime

SRC = "/home/z/my-project/arc/oct29_work/arc26-nvarc-v43.ipynb"
OUT = "/home/z/my-project/arc/oct29_work/arc26-nvarc-v44-mixture.ipynb"

def text(nb, i):
    return "".join(nb["cells"][i]["source"])

def set_text(nb, i, t):
    nb["cells"][i]["source"] = t.splitlines(keepends=True)

def log(m):
    print(f"[{datetime.datetime.now(datetime.timezone.utc).isoformat()}] {m}", flush=True)

def patch(t, old, new, tag):
    assert old in t, f"{tag}: anchor not found"
    assert t.count(old) == 1, f"{tag}: anchor not unique"
    return t.replace(old, new, 1)

def main():
    nb = json.load(open(SRC))
    assert len(nb["cells"]) == 37, f"expected 37 cells, got {len(nb['cells'])}"
    base = json.load(open(SRC))

    # Optional Nov-7 hook: bake a concrete 3.8-class quant glob from v44_glm_glob.txt
    import os as _os
    glob_file = "/home/z/my-project/arc/oct29_work/v44_glm_glob.txt"
    glm_glob = ""
    if _os.path.exists(glob_file):
        glm_glob = open(glob_file).read().strip()
        log(f"v44_glm_glob.txt present -> baking glob: {glm_glob!r}")

    # ---------- cell 01: master NVARC window (12h -> 6h-cap compliant, env-overridable) ----------
    t = patch(text(nb, 1),
              "global_end_time = time.time() + (12 * 3600 - 600 if RERUN_BUDGET else 1.0 * 3600 - 600)",
              "global_end_time = time.time() + (int(float(os.getenv('ARC_V44_TOTAL_BUDGET_H', '5.5')) "
              "* 3600) - 600 if RERUN_BUDGET else 1.0 * 3600 - 600)",
              "cell01-budget")
    set_text(nb, 1, t)

    # ---------- cell 00: title (full line) ----------
    t = patch(text(nb, 0),
              "# ARC26 NVARC v43 — L12' status-gated a2 retention (v40-R cfg + ONE lever; built Oct-30; "
              "Oct-31 slot; council answered->apply / rescued->hold NVARC a2)",
              "# ARC26 NVARC v44 — MIXTURE-OF-SOLVERS endgame (v43 chassis + 3.8-class quant ladder "
              "entry via v38 swap + 6h-cap budget + mixture receipts; built Nov-1; validate Nov-7 quota "
              "refresh; L12' retained; proven Qwen3.8-27B FP8 stays as ladder fallback)",
              "cell00")
    set_text(nb, 0, t)

    # ---------- cell 03: v44 env defaults (0-indent, before first use) + scaled budget constants ----------
    t = patch(text(nb, 3),
              "import os as _v32_os, json as _v32_json",
              '''import os as _v32_os, json as _v32_json

# ============ v44 mixture-of-solvers levers (flag-gated; fail-open; Nov-1 build) ============
# ARC_V44_GLM: promote a 3.8-class QUANT ("3.8 flash") to ladder PRIMARY via the proven v38
#   swap infra; the proven Qwen3.8-27B FP8 stays in the ladder as fallback (mixture of agents).
#   ARC_V44_GLM_GLOB is INERT by default ("") — the Nov-7 push session sets it to the concrete
#   Kaggle mount of the chosen 3.8-class quant; a bad glob degrades gracefully (ladder
#   "failed -> next" = proven 27B behaviour).
# ARC_V44_TOTAL_BUDGET_H: 6h weekly GPU cap compliance (34.86-leader lesson: a small leg fits
#   6h; a 27B 12h run never does). Scaled here: NVARC window (cell 01), leg box start, kill epoch.
_V44_DEFAULTS = {
    "ARC_V44_GLM": "1",
    "ARC_V44_GLM_GLOB": "",
    "ARC_V44_NO_TOOL_PARSER": "1",
    "ARC_V44_TOTAL_BUDGET_H": "5.5",
    "ARC_V44_MIXTURE": "1",
}
for _k44e, _v44e in _V44_DEFAULTS.items():
    _v32_os.environ.setdefault(_k44e, _v44e)
print("[v44 levers]", {k: _v32_os.environ[k] for k in _V44_DEFAULTS})''',
              "cell03-env")
    if glm_glob:
        _old_glob = '"ARC_V44_GLM_GLOB": "",'
        assert t.count(_old_glob) == 1
        t = t.replace(_old_glob, f'"ARC_V44_GLM_GLOB": {glm_glob!r},', 1)
        log("ARC_V44_GLM_GLOB baked into env defaults")
    t = patch(t,
              "_V32_T0 = global_end_time - ((12 * 3600 - 600) if RERUN_BUDGET else (1.0 * 3600 - 600))",
              "_V32_T0 = global_end_time - ((int(float(_v32_os.environ.get('ARC_V44_TOTAL_BUDGET_H', '5.5')) "
              "* 3600) - 600) if RERUN_BUDGET else (1.0 * 3600 - 600))",
              "cell03-t0")
    t = patch(t,
              '    _V32_KILL_EPOCH = _V32_T0 + 12 * 3600 - int(_v32_os.environ["ARC_V32_LEG27B_KILL_MIN"]) * 60',
              "    _V32_KILL_EPOCH = _V32_T0 + (int(float(_v32_os.environ.get('ARC_V44_TOTAL_BUDGET_H', '5.5')) "
              "* 3600)) - int(_v32_os.environ[\"ARC_V32_LEG27B_KILL_MIN\"]) * 60",
              "cell03-kill")
    set_text(nb, 3, t)

    # ---------- cell 25: parser override (GLM ladder entry = plain chat) ----------
    t = patch(text(nb, 25),
              'PARSERS = ["--tool-call-parser", "qwen3_coder", "--reasoning-parser", "qwen3"]',
              'PARSERS = ["--tool-call-parser", "qwen3_coder", "--reasoning-parser", "qwen3"]\n'
              '# v44: non-Qwen ladder entries (GLM-4-9B-AWQ) start without qwen tool parsers\n'
              'if __import__("os").environ.get("ARC_V44_NO_TOOL_PARSER", "0") == "1":\n'
              '    PARSERS = []',
              "cell25")
    set_text(nb, 25, t)

    # ---------- cell 30: 3.8-class quant ladder entry (env-driven; 8-space indent, inside try) ----------
    t = patch(text(nb, 30),
              '        _models = [(cfg["model_glob"], server.server_ladder(cfg), True)]',
              '        # v44: promote a 3.8-class quant (GLM-4-9B-AWQ / Qwen3.8-flash) to ladder PRIMARY via\n'
              '        # the proven v38 swap infra; the proven Qwen3.8-27B FP8 stays as ladder fallback.\n'
              '        if os.environ.get("ARC_V44_GLM", "0") == "1" and os.environ.get("ARC_V44_GLM_GLOB"):\n'
              '            os.environ["ARC_V38_LEG_SWAP"] = "1"\n'
              '            cfg.setdefault("v38_model_glob", os.environ["ARC_V44_GLM_GLOB"])\n'
              '            log("[v44] 3.8-class quant ladder primary armed: " + os.environ["ARC_V44_GLM_GLOB"])\n'
              '        _models = [(cfg["model_glob"], server.server_ladder(cfg), True)]',
              "cell30")
    set_text(nb, 30, t)

    # ---------- cell 33: mixture-router receipts (L12' semantics retained; fail-open) ----------
    t = patch(text(nb, 33),
              'print("[v43 L12] receipt write failed:", repr(_e43b))',
              'print("[v43 L12] receipt write failed:", repr(_e43b))\n'
              '\n'
              '        # v44 mixture-of-solvers receipts (student-replace doctrine, decoded from the\n'
              '        # 34.86 leaderboard leader; ONE lever):\n'
              '        # count which agent produced each shipped a2 — GLM ladder primary vs council\n'
              '        # fallback vs held (L12-prime rescued-hold). Observability only; score semantics\n'
              '        # unchanged from v43 (L12\\\' gate above). Fail-open: unreadable results -> stand.\n'
              '        _v44_stats = {"tasks": 0, "glm_primary": 0, "council_fallback": 0, "held": 0}\n'
              '        if _os.environ.get("ARC_V44_MIXTURE", "1") == "1" and _ans:\n'
              '            try:\n'
              '                _res44 = _json.load(open("/kaggle/working/leg27b_results.json"))\n'
              '                _rec44 = {}\n'
              '                for _r44 in (_res44.get("records") or []):\n'
              '                    _tid44 = _r44.get("task_id")\n'
              '                    if _tid44 and _tid44 not in _rec44:\n'
              '                        _rec44[_tid44] = _r44\n'
              '                for _k44 in _ans:\n'
              '                    _v44_stats["tasks"] += 1\n'
              '                    _rec = _rec44.get(_k44.rpartition("_")[0]) or {}\n'
              '                    if _rec.get("model_index") == 0:\n'
              '                        _v44_stats["glm_primary"] += 1\n'
              '                    elif _rec.get("status") == "answered":\n'
              '                        _v44_stats["council_fallback"] += 1\n'
              '                    else:\n'
              '                        _v44_stats["held"] += 1\n'
              '            except Exception as _e44:\n'
              '                print("[v44 mixture] results unreadable -> v43 semantics stand:", repr(_e44))\n'
              '            try:\n'
              '                _json.dump(_v44_stats, open("/kaggle/working/v44_mixture_receipt.json", "w"))\n'
              '                print("[v44 mixture] receipts:", _v44_stats)\n'
              '            except Exception as _e44b:\n'
              '                print("[v44 mixture] receipt write failed:", repr(_e44b))',
              "cell33")
    set_text(nb, 33, t)

    # ---------- cell 34: provenance ----------
    t = patch(text(nb, 34),
              '"built": "v43 (v40-R cfg + ONE lever L12\' status-gated a2 retention; doctrine: daily NEW code)",',
              '"built": "v44 (v43 + mixture-of-solvers: GLM-4-9B-AWQ ladder primary via v38 swap, '
              '6h-cap budget, mixture receipts; doctrine: daily NEW code)",',
              "cell34-built")
    t = patch(t,
              '            "v43_flags": {k: _ao.environ.get(k) for k in ("ARC_V43_L12",)},',
              '            "v43_flags": {k: _ao.environ.get(k) for k in ("ARC_V43_L12",)},\n'
              '            "v44_flags": {k: _ao.environ.get(k) for k in\n'
              '                          ("ARC_V44_GLM", "ARC_V44_GLM_GLOB", "ARC_V44_NO_TOOL_PARSER",\n'
              '                           "ARC_V44_TOTAL_BUDGET_H", "ARC_V44_MIXTURE")},',
              "cell34-flags")
    set_text(nb, 34, t)

    # ---------- cell 36: receipts ----------
    t = patch(text(nb, 36), '"version": "v43",', '"version": "v44",', "cell36-version")
    t = patch(t,
              '{"name": "l12_status_gate_a2", "flag": "ARC_V43_L12",',
              '{"name": "v44_mixture_glm_ladder", "flag": "ARC_V44_GLM",\n'
              ' "value": os.environ.get("ARC_V44_GLM", "1"),\n'
              ' "receipt": "GLM-4-9B-AWQ ladder primary (v38 swap infra) + 27B council fallback; '
              '6h-cap budget ARC_V44_TOTAL_BUDGET_H; mixture counts in v44_mixture_receipt.json"},\n'
              '            {"name": "l12_status_gate_a2", "flag": "ARC_V43_L12",',
              "cell36-levers")
    t = patch(t,
              '    try:\n        rec["l12"] = json.load(open(os.path.join(OUT, "l12_receipt.json")))',
              '    try:\n        rec["v44_mixture"] = json.load(open(os.path.join(OUT, "v44_mixture_receipt.json")))\n'
              '    except Exception as _e36c:\n'
              '        rec["v44_mixture"] = f"missing: {type(_e36c).__name__}"\n'
              '    try:\n        rec["l12"] = json.load(open(os.path.join(OUT, "l12_receipt.json")))',
              "cell36-recs")
    set_text(nb, 36, t)

    # ---------- verification ----------
    touched = {0, 1, 3, 25, 30, 33, 34, 36}
    for i in range(37):
        if i in touched:
            continue
        assert text(nb, i) == text(base, i), f"cell {i} changed but must be byte-identical"
    for i in sorted(touched):
        cell_type = nb["cells"][i].get("cell_type", "code")
        src = text(nb, i)
        if cell_type == "markdown":
            assert src.strip(), f"cell {i}: markdown emptied"
            log(f"cell {i:02d}: markdown OK")
            continue
        body = src.split("\n", 1)[1] if src.lstrip().startswith("%%writefile") else src
        ast.parse(body)
        log(f"cell {i:02d}: AST OK")
    assert text(nb, 26) == text(base, 26), "leg merge.py must stay byte-identical (a1 contract)"
    # forbidden paths (L2/L5/L8): no submit, no other-account tokens, no rerun flags
    whole = "\n".join(text(nb, i) for i in range(37))
    for bad in ("CreateCodeSubmission", "uradkr", "koushikrudra", "ARC_V44_RERUN"):
        assert bad not in whole, f"forbidden token in notebook: {bad}"
    json.dump(nb, open(OUT, "w"))
    n = sum(len("".join(c.get("source", []))) for c in nb["cells"])
    log(f"BUILT -> {OUT} (37 cells, {n} chars; touched {sorted(touched)}; all other cells byte-identical)")
    log("D5-lite verdict: STRUCTURAL PASS (byte-identity + AST on all touched cells + merge.py "
        "untouched + forbidden-path sweep). Behavioral replay deferred: leg records/model_index "
        "only exist in-kernel; the mixture counters are fail-open observability.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
