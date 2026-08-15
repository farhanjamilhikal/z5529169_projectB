# Week 10 and market feasibility plan

## Source reviewed

This plan now uses the supplied **Week 10 Agentic Coding and Revision** deck
(FINS3645, 56 PDF pages / 50 numbered teaching slides) together with
`PROJECT_BRIEF.md`. The deck is a worked reference implementation, while the
published brief and rubric remain the assessment authority. This distinction
matters: the lecture shows twelve baseline funds, but the brief requires at least
two combined optimisation methods and rewards broader, carefully evidenced work.

## Feasibility test result

The transparent weighted score is **63/100**. This means the prototype is
feasible, not that commercial launch is approved. Three scorecard dimensions are
critical blockers: commercial evidence, execution/operations and regulatory
readiness. The full evidence is in
`results/tables/product_feasibility_scorecard.csv`.

## Course benchmark position, line by line

| Part B benchmark | Current position | Evidence | Gap to the strongest band |
|---|---|---|---|
| Funds and OOS backtest, 15% | Strong and above the required minimum | Ten funds: three core methods in equity, crypto and combined, plus one sentiment fund; monthly past-only weights; 252/365 calendars; 10 bps costs | The lecture's optional twelve-fund reference also includes tangency in all three universes. This project deliberately omits it; explain estimation-error risk or add it as a labelled robustness benchmark, not as a guaranteed winner. |
| Sentiment and fusion, 10% | Strong prototype | 146,830 usable unique headlines; ten-sector index; one-trading-day lag; no-news sensitivity; reliability-gated before/after comparison | Add a human/expert-labelled finance holdout. The movie test is only a non-degradation check. |
| Innovation and results, 30% | Strong candidate, not an assured grade | Finance lexicon, reliability gate, dual-domain assurance harness, cost model, feasibility registers and Decision Studio | The student must identify which contribution is genuinely theirs and explain its evidence. More features do not substitute for authorship or depth. |
| App and implementation, 15% | Strong local prototype | Six views; compare; fact sheet; holdings; allocation; sentiment; transparency; objective trade-offs; precomputed artifacts | No public repo or logged-out live-link test yet, because the user explicitly prohibited a GitHub push. |
| Interpretation and writing, 10% | Technically strong draft | Ten narrative pages, three recommendations, six captioned figures and report-to-CSV checks | Student must rewrite/approve the economic judgement in their own words. |
| AI workflow and transparency, 20% | Evidence structure present | Agent instructions, prompt logs, AI notes and candid unresolved gates | The student must curate the actual prompts, AI mistakes and their own corrections. Manufactured retrospective authorship would be unacceptable. |

## Exact comparison with the Week 10 worked numbers

These are **diagnostics, not a leaderboard**. The lecture uses an expanding
window and its own constraints/cost treatment. This project uses a rolling
one-native-year window, explicit caps, covariance shrinkage and 10 bps turnover
costs. A higher number under a different specification is not proof of a better
fund.

| Method and universe | Week 10 Sharpe | This project Sharpe | Difference | Honest reading |
|---|---:|---:|---:|---|
| Equity Equal Weight | 0.85 | 0.83 | -0.02 | Approximately reproduces the lecture baseline |
| Crypto Equal Weight | 0.99 | 0.77 | -0.22 | Does not beat the lecture; crypto result is specification-sensitive |
| Combined Equal Weight | 0.76 | 0.77 | +0.01 | Essentially tied, not economically decisive |
| Equity Minimum Variance | 0.62 | 0.49 | -0.13 | Lower risk did not compensate for lower return here |
| Crypto Minimum Variance | 1.17 | 1.01 | -0.16 | Best Sharpe in this project, but a -72.99% drawdown prevents a safety claim |
| Combined Minimum Variance | 0.61 | 0.52 | -0.09 | Lower than lecture, but this project has a shallower -15.77% drawdown |
| Equity Risk Parity | 0.75 | 0.72 | -0.03 | Close to lecture |
| Crypto Risk Parity | 1.02 | 0.81 | -0.21 | Does not beat lecture and remains extremely high drawdown |
| Combined Risk Parity | 0.78 | 0.85 | +0.07 | The only clear positive Sharpe gap; still sample- and design-dependent |
| Tangency, all universes | 0.72 / 0.73 / 0.40 | Not offered | Not comparable | A transparent scope difference, not a hidden failure |

The project beats its own Combined Equal Weight benchmark with Combined Risk
Parity on Sharpe (0.85 versus 0.77) and drawdown (-20.47% versus -28.75%), while
giving up 1.80 percentage points of annualised return. That multi-metric trade-off
is a stronger course answer than claiming to beat every benchmark.

## Week 10 exhibit and implementation audit

| Lecture requirement | Status | Project evidence | Remaining action |
|---|---|---|---|
| Performance table | Pass | `performance_metrics.csv` and report Table 1 | None |
| Growth of one dollar | Pass | Figure 1 | None |
| Drawdown | Pass | Figure 2 and every fact sheet | None |
| Weights over time | Pass | Figure 3 | None |
| Sharpe or risk-return comparison | Pass | Figure 6 | None |
| Sector sentiment over time | Pass | Figure 4 | None |
| Fusion before versus after | Pass | Figure 5 and Table 2 | None |
| Compare funds | Pass locally | App Compare view | Deploy later |
| Read a fact sheet and holdings | Pass locally | App Fact sheet view | Deploy later |
| Build an allocation with a fee | Partial | Historical allocation and scenario CSV exist; 10 bps fund trading costs are modelled | Add a user-facing annual management-fee input only if its basis and double-counting treatment are defined |
| Fear and greed gauge | Alternative implemented | Sector analytics, coverage and reliability are shown | A 0-100 gauge is optional; if added, standardise using past-only data for live use |
| Meaningful crypto sleeve | Tested as an extension | All ten supplied cryptos are used; 0/10/20/30% minimum-sleeve sensitivity is saved and shown in Decision Studio | Keep the variants labelled research-only unless the student chooses a product objective and defends the additional drawdown |
| Precomputed lightweight app | Pass | App loads `results/` and does not run VADER/backtests | None |
| Public repository and live link | Intentionally open | Local project only | User-authorised GitHub push and logged-out link check |
| AI prompt log and own corrections | Partial/student-owned | Files exist under `ai/` | Student must curate truthful entries |

## What “beat the benchmark” can truthfully mean

The project can beat its transparent internal baselines and the course minimum.
It cannot yet claim to beat Wealthfront, Stockspot, Composer, eToro, AQR,
BlackRock or RavenPack on investment performance because their universes,
periods, costs, objectives and live operations are not comparable.

- Combined Risk Parity beats Combined Equal Weight on Sharpe (0.85 versus 0.77)
  and drawdown (-20.47% versus -28.75%), but not return (13.29% versus 15.10%).
- The sentiment extension beats Equity Minimum Variance modestly on return
  (6.09% versus 5.57%) and Sharpe (0.53 versus 0.49), but its drawdown is
  marginally worse and turnover is higher.
- The app exceeds the minimum investor journey by adding objective trade-offs,
  scenario download, dual-domain sentiment assurance, feasibility gates and a
  risk-mitigation register.

It is **not correct** to tune parameters until all lecture Sharpe ratios are
exceeded. Week 10 explicitly warns that a tuned aggressive sentiment tilt can
score 0.84 in discovery and collapse to 0.08 in the 2023 holdout. Beating a
visible benchmark by repeated tuning would create the exact overfitting problem
the course teaches students to avoid.

## Market options

### Option A: portfolio learning and research lab, recommended

- Customer: self-directed learner or early-career investor.
- Promise: understand risk trade-offs before choosing a portfolio method.
- Revenue test: free comparison plus paid decision workbook, scenario history or
  cohort education.
- Why it fits: the current product already provides traceability and explanations.
- First proof: five to ten observed usability sessions and a willingness-to-pay
  experiment.

### Option B: adviser research cockpit

- Customer: licensed adviser, educator or small research team.
- Promise: compare model portfolios and export a complete evidence trail.
- Revenue test: paid pilot or white-label report export.
- Required additions: benchmark import, holdings overlap, attribution, audit log,
  access control and a licensed partner.

### Option C: sentiment assurance module

- Customer: research teams testing general versus finance language models.
- Promise: dual-domain non-degradation and finance-validity gates.
- Required additions: licensed star-labelled movie data, licensed or proprietary
  expert-labelled finance data, confusion matrices and slice monitoring.
- Weakness: there is no proprietary data moat yet.

### Option D: retail managed portfolios, long-term only

- Customer: retail investor.
- Promise: invest in transparent systematic funds.
- Blockers: live record, execution, custody, capacity, fees, advice/dealing or
  scheme authorisation, client suitability and incident governance.
- Decision: do not market this route as available now.

## Product gates before launch

1. Complete the expert-labelled finance benchmark.
2. Obtain legitimate star-labelled movie reviews if the movie slice is retained.
3. Run user comprehension tests on Sharpe, drawdown and “best fund” language.
4. Run rolling subperiod and later-data validation.
5. Stress transaction costs, market impact, tax and fees.
6. Add holdings overlap, factor exposure and marginal risk contribution.
7. Run a live shadow portfolio with predeclared rules and incident logs.
8. Test willingness to pay with a narrow target segment.
9. Obtain qualified Australian legal and licensing advice before advice,
   execution, custody or pooled investment activity.
10. Complete the public course deployment only after the student authorises it.

## Decision

The correct immediate direction is Option A, with Option B as the next commercial
experiment. The dual-domain sentiment work is model assurance, not a movie-driven
investment factor. Option D remains a future regulated route rather than the
current product claim.

For the course, retain the current three-method design and explain why tangency is
not necessary for compliance. If time permits, tangency may be added as a clearly
labelled robustness benchmark, but only with its in-sample versus out-of-sample
instability reported. Do not add it merely to make the fund count equal twelve.
