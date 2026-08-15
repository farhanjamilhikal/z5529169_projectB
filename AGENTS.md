# Project B agent instructions for z5529169

Read `PROJECT_BRIEF.md`, `SUBMISSION_CHECKLIST.md`, and
`context/verify_ai_output.md` before changing this folder.

## Scope and product

This folder is FINS3645 Project B for **Signal & Story**. It implements DFF
Stations 3 and 4 using the student's verified Part A foundation. Work only on
the student's own project and preserve the official starter structure.

The product must offer equity-only, crypto-only and combined systematic funds,
out-of-sample fact sheets, a sector headline-sentiment index, a tested
structured/unstructured fusion, and a lightweight Streamlit investor journey.

## Model rules

- Load raw data only through `src/data_access.py`; never edit that provided file.
- Compute crypto returns on the native seven-day calendar before aligning them
  to equity dates for a combined fund.
- Every weight applied on date t must use returns strictly before t.
- Map weekend or holiday headlines to the next equity trading day, then lag the
  resulting signal at least one further equity trading day before investment use.
- Preserve headline casing, punctuation and negation for VADER.
- Equal-weight ticker-day sentiment within sectors. Report and test the chosen
  no-news rule rather than hiding it.
- Use long-only, capped weights; verify that every weight vector sums to one and
  that optimisation methods produce genuinely different weights.
- State annualisation, risk-free rate, turnover and transaction-cost assumptions.
- Treat outliers as audit items. Do not delete plausible market events.
- Never describe a backtest as a forecast or promise.

## Supplied data rule

Account for every supplied field. A field may be a model input, grouping key,
diagnostic, disclosure or provenance field. Do not force OHLCV, URL or publisher
metadata into the return optimiser merely to claim that every column was used.
Document the role and reason in `results/tables/asset_data_use_register.csv`.

## Implementation rules

- Keep reusable model logic in `src/` (including pure dashboard calculations in
  `src/app_logic.py`) and the reproducible entrypoints at `scripts/run_part_b.py`
  and `scripts/run_all.py`.
- The deployed app reads precomputed CSVs under `results/`; it must not import
  NLTK, download raw data or run an optimiser.
- Use the Signal & Story ivory, oxblood, blue, green, brick, ochre and grey
  visual system consistently. No gradients, stock imagery or unsupported claims.
- Do not commit, push, publish or deploy unless the student gives a later,
  explicit instruction. The current scope is local PyCharm use only.

## Verification rules

Run `python scripts/run_all.py`, which rebuilds the analysis and report and then
runs pytest, Ruff and the hand-in checker. Inspect output dimensions, weight sums,
caps, first live dates, sentiment lags and required filenames. Every reported
number must trace to a committed artifact and a reproducible run.

## Writing and AI transparency

- Never invent citations, statistics, sources or market explanations.
- Keep authentic prompts, AI outputs, execution failures, corrections and
  reasons in `ai/`. Do not fabricate student review or claim the student made a
  correction that the record does not show.
