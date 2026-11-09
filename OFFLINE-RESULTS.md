# Offline numerical test results

These are code-only checks on saved fallback reports. No semantic model check or human verification is claimed. The complete Checkpoint 2 proof remains pending.

| Trial | Code correct | Wrong | Unsupported | Report |
|---|---:|---:|---:|---|
| clean | 11 | 0 | 0 | [Offline report](runs/COST_20261106T064855680681Z_offline/offline-report.md) |
| seeded-eps | 10 | 1 | 0 | [Offline report](runs/COST_20261106T064855963715Z_offline/offline-report.md) |
| invented-growth | 11 | 1 | 0 | [Offline report](runs/COST_20261106T064856179608Z_offline/offline-report.md) |

Known answers: annual diluted EPS $20.76; seeded EPS $21.76. Annual revenue growth (303,154 / 275,235 − 1) × 100 = 10.1436953876%; invented growth 14.14%.

The table covers the eleven original core claims plus the invented-growth sentence in its trial. Additional narrative and peer claims are outside the offline parser’s scope. The model-backed Verifier has not been run.
