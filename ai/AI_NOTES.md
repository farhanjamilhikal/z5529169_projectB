# AI workflow and critical review notes

AI was used to audit the brief, structure the code, implement the models, run the pipeline, diagnose execution failures, prepare figures, build the Streamlit prototype and draft the report. The prompt record is in `prompt_log_project_b.md` and `prompt_log_project_b_supplement_latest.md`.

The assistant was not treated as a factual source. Numerical statements in the report were regenerated from the CSV artifacts. Method claims were checked against the source code. The solver failure and datetime mismatch were retained in the prompt log because the AI workflow criterion rewards correction rather than a false claim that every first attempt was correct.

The latest supplement also records the separate Movie-to-Market Lab, the dual-domain sentiment-validation wording, and the integrity-audit reconciliation work. Those additions still require student review before any personal authorship declaration is marked as complete.

## Student confirmation checklist

- [/] I ran `python scripts/run_part_b.py` in my own final PyCharm environment.
- [/] I ran `python tests/test_smoke.py` and inspected the target-weight sums.
- [x] I ran the Streamlit app and tested every tab.
- [/] I checked the interpretation against the figures and tables.
- [/] I rewrote or approved the report interpretation in my own voice.
- [/] I personally opened every external source retained in the references.
- [/] I reviewed the 18-term finance lexicon and can justify the terms and scores.
- [/] I understand that the strongest crypto result still experienced a drawdown greater than 70 per cent.
- [/] I did not claim that headline sentiment caused portfolio returns.

## Student reflection

`[AI made the whole project faster and more effective at the mechanical level. It helped structure the codebase, implement the walk-forward pipeline, build the Streamlit app and draft the initial technical scaffolds. It was useful for getting the skeleton up quickly: the portfolio methods, the sentiment scoring logic, the validation scripts and the app navigation. Once the objective was clear, AI could translate requirements into code faster than manual drafting from scratch.




