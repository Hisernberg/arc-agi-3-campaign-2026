# 03 — Architecture: the apex-v12 v2 pipeline

Notebook: `dasshovon/arc26-b-apex-v12` **version 2** (33 cells, 635 KB source, pinned docker,
RTX Pro 6000 GPU, 5 datasets, 2 drafter models, competition-attached).
This is the weapon armed for Oct-27. Everything below is verified by the receipt system.

```
┌────────────────────────────────────────────────────────────────────────┐
│ 0. GUARD-V2 LAYER (first cell that runs, last cell that decides)       │
│    rerun-vs-interactive detection · GPU check (target: RTX Pro 6000)   │
│    gateway DNS probe → 120-min patience / 3600s DNS-escape             │
│    smoke fast-path · guard_decision.json artifact                      │
│    fail-path: writes valid placeholder instead of a broken notebook    │
├────────────────────────────────────────────────────────────────────────┤
│ 1. HARNESS (M2S lineage, patched)                                      │
│    pennyroyal-v253 wheels + taaf source bundle (pinned digests)        │
│    concurrency 120 · priority scheduling · parquet net                 │
│    dual-layout mount resolver (E-135) · deadline watchdog (E01)        │
├────────────────────────────────────────────────────────────────────────┤
│ 2. D′ SLOT-PRIORITY ALLOCATOR (the engine — FORM receipt live)         │
│    priority_value replaced · fresh-first removed                       │
│    tail fade 0.4 · level_pow 0.5 · eff_const 300 · eff_pow 2.5         │
│    pace_pow 0.4 · pace_ref 30000 · c_action 0.1 · action_scale 115     │
│    c_token 0.9 · token_scale 225000 · lin_floor 0.1 · rel_pow 0.5      │
│    budget bands b1=10 b2=14 b3=16                                      │
│    + STALL-KNEE FOLD (D2): priority *= max(0.1, 1/(1+(a−80)/40))       │
│      flat knee 80, halflife 40, floor 0.1 — post-FORM wrap, additive   │
│      constants only, fail-open to exact v11 priority on exception      │
├────────────────────────────────────────────────────────────────────────┤
│ 3. WASTEPACK (context-efficiency pack)                                 │
│    chat_completion + dispatch_tool wrapped                             │
│    death_ledger=1 · repeat_guard=1 · lookahead=1                       │
│    dedup of repeated messages/lines · refusals tracked                 │
├────────────────────────────────────────────────────────────────────────┤
│ 4. KNOWLEDGE LAYER                                                     │
│    dossier v1 (arc26-game-dossier-v1): 25 games, own probe sessions,   │
│      recorded traces, playbooks, protocol_steps=6, prompt_tail         │
│    dossier v2 / XPACK (arc26-game-dossier-v2): categories for 25       │
│      games, transform-tool library, SFT CoT seeds, RL seeds            │
│      (tools currently fail-open → prompt-tail only; v13 fix)           │
├────────────────────────────────────────────────────────────────────────┤
│ 5. AGENT LOOP UPGRADE (D2)                                             │
│    act_checked(): model batches run ONE action at a time; each is      │
│    verified against the model-written simulate(); divergence raises    │
│    PredictionMismatchError → remaining batch cancelled, model          │
│    re-hypothesizes instead of burning budget. Fail-open: no            │
│    simulate() → plain batch; literal not found → no injection.         │
├────────────────────────────────────────────────────────────────────────┤
│ 6. MODEL STACK                                                         │
│    primary: Qwen3.5-27B-FP8 (dataset eliork/qwen3-5-27b-fp8,           │
│             local serve, license-audited Y21)                          │
│    drafters: albucino-qwen3-8-flash-next · intel qwen3.8-flash W4A16   │
├────────────────────────────────────────────────────────────────────────┤
│ 7. PROVENANCE & RECEIPTS                                               │
│    [Y21:AUDIT] license/lineage lines for every dataset+model           │
│    #OURS_* receipt lines (WASTEPACK/DOSSIER/XPACK/FORM/V12/            │
│    ACTCHECKED) — machine-greppable, gate-checked before every fire     │
└────────────────────────────────────────────────────────────────────────┘
```

## The receipts from the live GPU run (Oct-26, ~10:50Z) — all green

```
#OURS_V12 stall_knee=True knee=80 halflife=40 floor=0.1 flat
#OURS_V12_TAIL installed
#OURS_ACTCHECKED {'stall': True, 'act_checked': True, 'tail': False, 'errors': 0}
#OURS_WASTEPACK ok chat_completion + dispatch_tool wrapped death_ledger=1 repeat_guard=1 lookahead=1
#OURS_DOSSIER ok {'mounted': True, 'prompt_tail': 'installed', 'games': 25, 'protocol_steps': 6}
#OURS_XPACK ok {'mounted': True, 'games_categorized': 25, 'tools': False}   ← known fail-open, v13 item
#OURS_FORM ok version=d_prime (full formula live)
[Y21:AUDIT] qwen3.5-27b-fp8 weights (primary): dataset eliork/qwen3-5-27b-fp8
guard_decision.json: guard_version 2 · run_full false (interactive) ·
                     "gateway DNS dead 3612s (87 tries) -> commit-style env"
```

The last line is the quiet hero: **guard-v2 watched the gateway DNS stay dead for 61 minutes
during the interactive run and committed a clean, valid placeholder instead of crashing** —
the exact scenario that produced the two 0.00s in previous configs. Interactive runs are not
scored, so the placeholder there is correct behavior; what matters is that the same patience
now protects the scoring rerun.

## Design principles embodied

1. **Fail-open everywhere.** Every patch wraps the harness seam and falls back to proven
   behavior on any exception. A degraded run scores low; a crashed run scores 0.00.
2. **Additive constants only, no prompt rewording** (#36 grave) — scheduling deltas are
   arithmetic at proven seams, never prose.
3. **Byte-pinned dependencies.** Wheels, bundles, and docker are digest-pinned; a rerun
   environment cannot silently change the base under the agent.
4. **Everything is measured.** No cell ships without a receipt line; no fire without the
   gate script grepping those lines in the kernel output.

---

## v13 layer (Oct-26/27 build — the current weapon)

apex-v13 = apex-v12 + **D3 deltas**, all fail-open, all CPU-proved before GPU:

```
cell 7  MODEL SWAP   MODEL_DIR prefers saltb0x/qwen3-8-27b-fp8 (25.3GB official FP8
                     snapshot); falls back to eliork/qwen3-5-27b-fp8; fingerprint scan
                     breaks early on qwen3-8/qwen38 paths. Qwen3.8-27B ships
                     model_type "qwen3_5" (3.8 is built on the 3.5 architectural
                     foundation) -> SGLang FP8 stack accepts it unmodified.
                     Receipt: #OURS_V38 served=<name> dir=<tail>
cell 28 V13 CELL     (a) XPACK tools heal: dossier v3 ships ours_transforms.py AND
                         transforms.py; heal exec-registers the module (v12's
                         tools=False was an import-name mismatch).
                     (b) #48 transition-graph priors: priority *= (1+0.7*(prior-0.5));
                         dead actions (cheatsheet-parsed, 8 games) -> x0.65.
                     (c) #66 pace: actions_used > 1.25*par*level -> x0.88
                         (25/25 human pars parsed from cheatsheet budget guides).
                     (d) #67 endgame: actions_used >= family threshold ->
                         prior>=0.6 x1.20 else x0.93.
                     (e) additive tail (4th wrap, marker _ours_v13).
                     Receipt: #OURS_V13 graph=True pace=True endgame=True
                              tools_heal=exec-ok tail=installed errors=0
                              hits={'graph','pace','endgame','calls'}
```

Proof chain: 13/13 dataset gates (dossier v3) -> live on BOTH accounts (dasshovon +
kragglenote2forwork, 278KB, sha256 manifest) -> 19/19 kernel gates (v12 byte-identity
maintained, G16/G18) -> 13/13 CPU tests executing the REAL cell against the REAL dataset
with exact factor math (T6 dead-action x0.65 -> 65; T7 stacked x1.105*x0.88*x1.20 -> 117;
T8 -> 113; T9 -> 79; T11 exception -> raw priority) -> pushed v1 RUNNING on RTX Pro 6000
(kernelId 140991512).

Full plan of record: docs/49 (keyword protocol GOLDRUSH); model ladder: docs/51.
