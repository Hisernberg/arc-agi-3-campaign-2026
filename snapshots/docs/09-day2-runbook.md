# 09 · Day-2 Runbook (Sunday 2026-09-20) — turnkey loop

Preconditions (end of Day 1):
- v3 = duck-governor-v1 ran + auto-submitted; score recorded in analysis/results.md
- Day-1 PDF finalized with real score + verdict (new best / family band / rollback)

## Morning checklist

1. **Read Day-1 verdict**
   - `tail /tmp/finalizer-2026-09-19.log` (or finalizer log of the day)
   - `analysis/results.md` campaign log table
   - Decision rules: delta < ±0.5 = noise; rollback only if score < 2.45 (best − 1.0)

2. **Pick today's variant**
   - If governor ≥ 3.0 (family band): ship **worldmodel-v1.1** (Version 4 of kernel 35c14d)
   - If governor < 2.45: ship **production-12 re-push** (rollback sanity) OR worldmodel-v1.1
     anyway (fail-open, ledger independent of governor) — prefer v1.1, note the risk
   - If GPU hours exhausted: resubmit best-scoring existing version (variance harvest)

3. **Push v1.1 (if shipping)**
   ```bash
   cd /home/z/my-project/arc-agi-3
   export PATH="/home/z/.local/bin:$PATH"
   export KAGGLE_API_TOKEN=$(grep '^KAGGLE_TOKEN=' .env | cut -d= -f2)
   cd notebooks/duck-worldmodel-v1 && kaggle kernels push && cd ../..
   kaggle kernels status kragglenote2forwork/duck-qwen3-8-anim-base-35c14d   # expect QUEUED/RUNNING
   ```

4. **Poll in foreground (sandbox kills background procs!)**
   ```bash
   bash scripts/poll_cycle.sh    # repeat; exit code 10 = COMPLETE, 11 = FAILED
   ```

5. **On COMPLETE → submit the new version**
   ```bash
   # version = 4 for worldmodel-v1.1 (check kaggle kernels list -v or push output)
   kaggle competitions submit arc-prize-2026-arc-agi-3 \
     -k duck-qwen3-8-anim-base-35c14d -v 4 -m "worldmodel-v1.1 auto-submit"
   ```

6. **Wait for score (~30–60 min)**
   ```bash
   python3 scripts/kaggle_full_subs.py
   ```

7. **Mine traces from the completed run output**
   ```bash
   kaggle kernels output kragglenote2forwork/duck-qwen3-8-anim-base-35c14d --path /tmp/dayNout
   python3 scripts/mine_traces.py --kernel-output /tmp/dayNout
   python3 scripts/build_replay_dataset.py --kernel-output /tmp/dayNout
   ```

8. **Evening close-out**
   - Update analysis/results.md + notes-<date>.md
   - Regenerate PDF: `python3 scripts/make_daily_pdf.py reports/data-<date>.json reports/<date>-daily-report.pdf`
   - Update docs/07 ship queue; commit + push everything

## Escalation
- Run FAILED → do NOT submit broken version; check kernel log; ship rollback variant
- Submission rejected → check 1/day cap via `kaggle competitions submission-limits -c arc-prize-2026-arc-agi-3`
- GPU slot contention → v3 pattern: run starts when slot frees; poll patiently (up to 20h)
