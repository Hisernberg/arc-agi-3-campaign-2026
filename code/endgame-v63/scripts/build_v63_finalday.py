#!/usr/bin/env python3
"""Build v63 FINALDAY from the v44 mixture notebook (built 2026-11-02, post-lock).

User directive Nov-2: "run a new best possible notebook for final day with all
ideas mentioned best for final". Competition scoring is sealed (lock 05:45 UTC
Nov-2; submissions closed Nov-1 23:45 UTC) -> v63 is the validation/R&D vehicle:
it runs TODAY (CPU pool free of quota; dasshovon GPU 1.98h receipted) and is the
Nov-7 staged full run.

All-ideas composition (v63 = v44 base + final-day decode):
  - v44 mixture-of-solvers chassis (proven 37-cell surgery, static-passed):
    L12' gate, dynamic-trace protocol, 6h-cap budget, mixture receipts.
  - NEW: the decoded 34.86 leader's student mechanism wired in as ladder PRIMARY:
    their kernel mounts sorokin/qwen3_4b_grids15_sft139 (4B ARC-grids SFT) - the
    SAME model already in our model_data_sources. v63 bakes its glob into the
    v38 swap ladder primary; the proven Qwen3.8-27B FP8 stays as ladder fallback
    (ladder falls through on any failure = proven behaviour).
    ARC_V44_NO_TOOL_PARSER flipped to "0": the 4B is a Qwen3 family model and
    keeps the qwen3 tool parsers (the GLM-only parser strip no longer applies).
  - The full sandbox-verified code-induction harness (their cells 04-19) is NOT
    lifted: it is a 150KB dependency web; receipted as the post-competition
    upgrade path. The v63 student channel = direct sampling through the proven
    leg stack (unverified direct channel, labelled in receipts).

Variants (one builder, three outputs):
  gpu-full : budget 5.5h, full NVARC starter      -> staged for Nov-7 (kragglenote lane)
  solo     : budget 1.45h, commit 30min/3 tasks,
             starter->solo receipt, pip no-ops     -> RUN today on dasshovon (1.98h)
  cpu      : solo shape, GPU legs fail-open       -> RUN today on kragglenote CPU pool
"""
import json, ast, sys, hashlib, datetime

SRC = "/home/z/my-project/arc/oct29_work/arc26-nvarc-v44-mixture.ipynb"
OUTDIR = "/home/z/my-project/arc/oct29_work"
STUDENT_GLOB = ("/kaggle/input/models/sorokin/qwen3_4b_grids15_sft139/"
                "**/*.safetensors")

def log(m):
    print(f"[{datetime.datetime.now(datetime.timezone.utc).isoformat()}] {m}", flush=True)

def load(p):
    return json.load(open(p))

def cell_text(nb, i):
    return "".join(nb["cells"][i]["source"])

def set_cell(nb, i, t):
    nb["cells"][i]["source"] = t.splitlines(keepends=True)

def patch(nb, i, old, new, label):
    t = cell_text(nb, i)
    if old not in t or t.count(old) != 1:
        print(f"FAIL: anchor in cell {i} ({label}): found={t.count(old)}")
        sys.exit(1)
    set_cell(nb, i, t.replace(old, new, 1))
    log(f"patched cell {i:02d}: {label}")

SOLO_CELL16 = '''# v63 solo: the 12h NVARC starter launch is REMOVED (final-day validation boxes).
# Cell 1's safety net already wrote the base submission.json (identity attempt_1,
# flip attempt_2); the ladder leg (4B student primary, 27B fallback) improves
# attempt_2 over that base, fail-open at its kill-switches.
import os as _solo_os, json as _solo_json
with open('/kaggle/working/submission.json') as _solo_f:
    _solo_base = _solo_json.load(_solo_f)
_solo_n = sum(len(v) for v in _solo_base.values())
print(f"[v63 solo] NVARC skipped; base submission.json: {len(_solo_base)} tasks / {_solo_n} outputs "
      f"(rerun={bool(_solo_os.getenv('KAGGLE_IS_COMPETITION_RERUN'))})", flush=True)
'''

NOOP45 = ("# v63 {tag}: the NVARC-only stack is skipped (no starter.py run; the ladder leg\n"
          "# brings its own isolated serving stack from the wheelhouse mount, as in every v32+ run).\n"
          "print('[v63 {tag}] cell {n} no-op', flush=True)\n")

def apply_variant(nb, tag, budget, commit_min):
    """v45s-proven surgery: title, env boxes, cells 4/5 no-op, cell 16 solo receipt."""
    set_cell(nb, 0, "# ARC26 NVARC v63 %s - FINALDAY MIXTURE (v44 chassis + decoded 34.86 student mount "
                    "sorokin/qwen3_4b_grids15_sft139 as ladder primary, 27B fallback; built Nov-2 "
                    "post-lock; validation vehicle, no submission path)\n" % tag)
    patch(nb, 3, '"ARC_V44_TOTAL_BUDGET_H": "5.5",', '"ARC_V44_TOTAL_BUDGET_H": "%s",' % budget,
          "budget %sh" % budget)
    if commit_min:
        patch(nb, 3, '"ARC_V32_LEG27B_COMMIT_BOX_MIN": "100",',
              '"ARC_V32_LEG27B_COMMIT_BOX_MIN": "%s",' % commit_min, "commit box %s min" % commit_min)
        patch(nb, 3,
              '"ARC_V32_LEG27B_COMMIT_TASKS": "0934a4d8 136b0064 16de56c4 20270e3b 31f7f899 3dc255db '
              '409aa875 7b3084d4 8f215267 b99e7126 d35bdbdc e376de54",',
              '"ARC_V32_LEG27B_COMMIT_TASKS": "0934a4d8 136b0064 16de56c4",', "commit tasks -> 3")
    set_cell(nb, 4, NOOP45.format(tag=tag, n=4))
    set_cell(nb, 5, NOOP45.format(tag=tag, n=5))
    set_cell(nb, 16, SOLO_CELL16)
    log(f"variant {tag}: cells 0/3/4/5/16 applied")

def static_checks(nb, base_nb, patched_idx, allow_changed):
    """AST on changed code cells; byte-identity for everything else; forbidden sweep."""
    ok = 0
    for i, c in enumerate(nb["cells"]):
        src = "".join(c["source"])
        if c["cell_type"] != "code" or src.startswith("!"):
            continue
        body = src.split("\n", 1)[1] if src.startswith("%%writefile") else src
        try:
            ast.parse(body)
            ok += 1
        except SyntaxError:
            same = json.dumps(base_nb["cells"][i]) == json.dumps(nb["cells"][i])
            if i in patched_idx and not same:
                print(f"FAIL: AST on changed cell {i}")
                sys.exit(1)
            if not same:
                print(f"FAIL: cell {i} fails AST and is NOT byte-identical to v44")
                sys.exit(1)
            log(f"note: cell {i} magics (byte-identical to proven v44)")
    log(f"AST OK: {ok} code cells parsed strict")
    ident = sum(1 for i in range(len(base_nb["cells"]))
                if json.dumps(base_nb["cells"][i]) == json.dumps(nb["cells"][i]))
    log(f"byte-identical cells vs v44: {ident}/{len(base_nb['cells'])}")
    import re
    blob = json.dumps(nb)
    for bad in ("KGAT_", "ghp_", "hf_n", "uradkr", "koushik", "kragglenote", "dasshovon",
                "CreateCodeSubmission"):
        if bad in blob:
            print(f"FAIL: forbidden token '{bad}' in notebook text")
            sys.exit(1)
    if re.search(r"hf_[A-Za-z0-9]{20,}", blob):
        print("FAIL: HF-token-shaped string in notebook text")
        sys.exit(1)
    log("forbidden-token sweep: clean")

def write(nb, path):
    json.dump(nb, open(path, "w"))
    h = hashlib.sha256(open(path, "rb").read()).hexdigest()
    import os
    log(f"WROTE {path} ({os.path.getsize(path)} chars) sha256={h[:16]}")

def main():
    base_nb = load(SRC)
    assert len(base_nb["cells"]) == 37, f"v44 expected 37 cells"

    # ---------- gpu-full: the staged Nov-7 vehicle ----------
    nb = load(SRC)
    patch(nb, 0, "# ARC26 NVARC v44", "# ARC26 NVARC v63", "title family")
    patch(nb, 3, '"ARC_V44_NO_TOOL_PARSER": "1",', '"ARC_V44_NO_TOOL_PARSER": "0",',
          "qwen3 parsers kept (4B student is Qwen3 family)")
    patch(nb, 3, '"ARC_V44_GLM_GLOB": "",', '"ARC_V44_GLM_GLOB": %r,' % STUDENT_GLOB,
          "decoded student mount -> ladder primary")
    set_cell(nb, 0, "# ARC26 NVARC v63 - FINALDAY MIXTURE (v44 chassis + decoded 34.86 student mount "
                    "sorokin/qwen3_4b_grids15_sft139 as ladder primary via the proven v38 swap, 27B "
                    "fallback; built Nov-2 post-lock; staged full run for the Nov-7 quota refresh)\n"
                    + "\n".join(cell_text(nb, 0).splitlines()[1:]))
    static_checks(nb, base_nb, {0, 3}, allow_changed=True)
    write(nb, f"{OUTDIR}/arc26-nvarc-v63-finalday.ipynb")

    # ---------- solo: RUN today on dasshovon (1.98h receipted) ----------
    nb = load(SRC)
    patch(nb, 3, '"ARC_V44_NO_TOOL_PARSER": "1",', '"ARC_V44_NO_TOOL_PARSER": "0",', "parsers kept")
    patch(nb, 3, '"ARC_V44_GLM_GLOB": "",', '"ARC_V44_GLM_GLOB": %r,' % STUDENT_GLOB, "student primary")
    apply_variant(nb, "SOLO", "1.45", "30")
    static_checks(nb, base_nb, {0, 3, 4, 5, 16}, allow_changed=True)
    write(nb, f"{OUTDIR}/arc26-nvarc-v63-finalday-solo.ipynb")

    # ---------- cpu: RUN today on the kragglenote lane (free pool) ----------
    nb = load(SRC)
    patch(nb, 3, '"ARC_V44_NO_TOOL_PARSER": "1",', '"ARC_V44_NO_TOOL_PARSER": "0",', "parsers kept")
    patch(nb, 3, '"ARC_V44_GLM_GLOB": "",', '"ARC_V44_GLM_GLOB": %r,' % STUDENT_GLOB, "student primary")
    apply_variant(nb, "CPU", "1.45", None)
    static_checks(nb, base_nb, {0, 3, 4, 5, 16}, allow_changed=True)
    write(nb, f"{OUTDIR}/arc26-nvarc-v63-finalday-cpu.ipynb")

    log("ALL THREE VARIANTS BUILT")
    return 0

if __name__ == "__main__":
    sys.exit(main())
