# docs/51 — Model plan: Qwen 3.8 family (constraint-honoring ladder)

Directive: "don't use any other model than Qwen 3.8 and 3.8 Flash for the qwen series —
others aren't that good, focus on these." All other families (incl. Gemma-4-31B despite
LB-0.86 evidence) rejected for our stack.

## 1. The ladder (with wiring status)

| Tier | Model | Source | Status |
|---|---|---|---|
| **Primary** | **Qwen3.8-27B-FP8** | Kaggle dataset `saltb0x/qwen3-8-27b-fp8` (25.3GB, official HF snapshot) | **WIRED in apex-v13** (MODEL_DIR first candidate) |
| Fallback 1 | Qwen3.5-27B-FP8 | dataset `eliork/qwen3-5-27b-fp8` | kept attached; auto-fallback via _resolve_path chain |
| Fallback 2 (incumbent) | Qwen3.8-Flash-Next W4A16 | model `dfranzen/intel-qwen3.8-flash-next-w4a16-autoround` | attached since v11; path 3 in chain |
| Drafter tier | Qwen3.8-Flash-Next (albucino drafter) | model `dfranzen/albucino-qwen3-8-flash-next-drafter` | attached; spec-decode enable = v15 (E-055) |
| Emergency (CPU) | Qwen3.8-27B GGUF q4 | `unsloth/Qwen3.8-27B-GGUF` | insurance only, not wired |

## 2. Why the swap is safe (evidence)

1. **Arch compatibility**: Qwen3.8-27B ships `model_type == "qwen3_5"` (HF tag qwen3_5;
   GitHub: "built on the architectural foundation of Qwen3.5"). Our cell-7 fingerprint
   accepts it; SGLang serving stack (feasibility-proven on 3.5) needs no change.
2. **Same size class**: 25.3GB FP8 ≈ 3.5's footprint → 96GB RTX Pro 6000 fits weights+KV.
3. **Public meta confirmation**: LB-9 kernel + duck-v12 run exactly this model.
4. **Fail-open**: absent mirror → 3.5 → Flash-Next incumbent (v11/v12 receipts green there).
5. **Receipts**: `#OURS_V38 served=... dir=...` proves which generation actually served.

## 3. Constraints & laws

- Qwen-3.8-family only (user directive, E-263) — codified as campaign law.
- No model swap within 24h of fire (E-265 freeze); model changes require fresh G2 receipts.
- Generation-tag every submission description (`model=qwen38-27b-fp8`, E-450) for
  attribution; scoreboard tracks 3.5-era vs 3.8-era scores (E-408).

## 4. Open items (tracked in idea pool)

- v13 verdict = first 3.8-era datapoint; attribute model vs D3 deltas via receipts hits
  (E-441). If 3.8 regresses: revert cell (3.5 first in chain) is one build (E-442).
- Multimodal: 3.8 is image-text-to-text; we serve text-only grids today (E-313). Vision
  branch (grid→PNG + STEP labels à la LB-0.86) = v15 research behind flag (E-314/436).
- 3.8-Max: open-weights watch (E-054); NVFP4/W4A16 quant family watch (E-140).
- Tokenizer checks at G2: ACTION names tokenize cleanly (E-445), context window confirm
  (E-447), multimodal config keys harmless in text mode (E-448).
