---
title: "Signal & Story: authorship and investment decision guide"
author: "Student ID z5529169"
date: "Evidence base: regenerated Project B artifacts, live period 31 December 2020 to 31 December 2023"
subject: "Understanding and decision support before the student approves the report"
---

> This is a study and decision workbook, not text to submit unchanged as your own writing. Read the
> evidence, record your own answers, then rewrite the final interpretation in your own voice. A
> backtest is historical evidence, not a forecast or personal financial recommendation.

## 1. The authorship issue in plain language

The computer can establish whether formulas ran, files agree and constraints were obeyed. It cannot
decide your investment objective, your tolerance for loss or whether the economic explanation is
genuinely yours. Your authorship is demonstrated when you can:

1. define each metric without reading a script;
2. identify which direction is desirable and why metrics can conflict;
3. compare the ten funds using actual evidence;
4. separate a functioning model from a commercially investable product;
5. state a hypothesis before interpreting a result;
6. reject or qualify claims that the evidence does not support; and
7. explain your design choices, weaknesses and next test.

Use this response scale throughout: **[ ] Yes  [ ] No  [ ] Unsure**. “Unsure” is an acceptable
answer. It identifies what you must investigate before approval.

## 2. From first principles: what every output means

### 2.1 Daily net return

The fund return for day *t* is the weighted sum of asset returns, less the assumed trading cost:

`net return_t = sum(weight_i,t × asset return_i,t) - 0.001 × one-way turnover_t`

The 0.001 is 10 basis points. Weights applied on day *t* are estimated only from observations before
day *t*. A positive daily return means the modeled fund gained value that day. It does not mean the
fund met a long-term objective.

### 2.2 Growth of one dollar and ending value

Growth compounds the daily net returns. An ending value of 1.45 means a modeled dollar became about
$1.45 during the live sample. It is intuitive, but it depends strongly on the sample start and end
dates. It is not an annual rate and does not show the path or pain experienced in between.

### 2.3 Annualised geometric return

Annualised return converts the compounded live result to an equivalent yearly growth rate. Higher is
desirable only if the extra risk, concentration and costs are acceptable. It is not an expected future
return. The project uses 252 periods per year for equity and combined funds, and 365 for crypto funds.

### 2.4 Annualised volatility

Volatility is the standard deviation of daily returns multiplied by the square root of 252 or 365.
Lower means a smoother historical return path, not protection from every loss. It treats upward and
downward surprises symmetrically and does not measure liquidity, custody, model or regulatory risk.

### 2.5 Sharpe ratio

The project assumes a zero risk-free rate:

`Sharpe = average daily return ÷ daily volatility × square root(periods per year)`

It measures historical return per unit of total volatility. Higher is better when comparing funds over
the same sample and with consistent assumptions. A Sharpe of 1.01 does **not** mean a 101% return, a
1% risk or a guarantee. It means the annualised average excess-return estimate was roughly one unit
for each unit of annualised volatility. It can look attractive while maximum drawdown is severe.

### 2.6 Maximum drawdown

Drawdown is the percentage fall from the previous growth peak. Maximum drawdown is the worst such
fall in the live sample. A value of -72.99% means a modeled investor at the prior peak temporarily lost
almost three quarters of value. Less negative is desirable. It is often more intuitive than volatility,
but it records only one historical path and may understate a future loss.

### 2.7 Turnover and transaction costs

One-way turnover measures how much the target portfolio changes when it rebalances. Higher turnover
usually means more trading, operational burden, tax consequences and implementation cost. The model
charges 10 bps per unit of turnover, but this is a common sensitivity assumption, not a calibrated
brokerage, spread or market-impact model.

### 2.8 Current target holdings and concentration

Holdings are the most recent model weights, not proof that orders could be filled at those prices.
Maximum weight, top-five weight and the Herfindahl index reveal concentration. Caps limit single-name
exposure but do not remove sector, factor or asset-class concentration.

### 2.9 Out-of-sample and walk-forward

Out-of-sample means each live weight uses only earlier observations. It reduces look-ahead bias. It
does not make the 2020-2023 sample independent of every design choice. Choosing methods after seeing
the final results can still create selection bias.

### 2.10 Sentiment, coverage and fusion

VADER maps headline language to a score. The finance extension changes scores for 18 disclosed terms.
Ticker-day scores are equal-weighted within sectors. No-news ticker-days are assigned zero, and an
observed-only sensitivity is reported. The investment signal is lagged one equity trading day. The
reliability gate reduces the tilt when coverage or publisher evidence is weak. Headline tone remains a
noisy proxy, not a direct measure of fundamentals or future return.

## 3. Your ten funds: exact regenerated evidence

| Fund | Return | Volatility | Sharpe |
|---|---:|---:|---:|
| Combined Equal Weight | 15.10% | 21.24% | 0.77 |
| Combined Minimum Variance | 5.99% | 12.62% | 0.52 |
| Combined Risk Parity | 13.29% | 16.17% | 0.85 |
| Crypto Equal Weight | 33.63% | 80.39% | 0.77 |
| Crypto Minimum Variance | 60.04% | 72.94% | 1.01 |
| Crypto Risk Parity | 37.94% | 78.63% | 0.81 |
| Equity Equal Weight | 12.87% | 16.16% | 0.83 |
| Equity Minimum Variance | 5.57% | 12.64% | 0.49 |
| Equity Risk Parity | 10.15% | 14.92% | 0.72 |
| Equity Reliability-Gated Sentiment | 6.09% | 12.64% | 0.53 |

| Fund | Max drawdown | Ending $1 | Turnover |
|---|---:|---:|---:|
| Combined Equal Weight | -28.75% | $1.52 | 1.00x |
| Combined Minimum Variance | -15.77% | $1.19 | 9.86x |
| Combined Risk Parity | -20.47% | $1.45 | 1.96x |
| Crypto Equal Weight | -81.60% | $2.39 | 1.00x |
| Crypto Minimum Variance | -72.99% | $4.10 | 6.64x |
| Crypto Risk Parity | -80.22% | $2.63 | 2.03x |
| Equity Equal Weight | -20.32% | $1.44 | 1.00x |
| Equity Minimum Variance | -15.59% | $1.18 | 10.19x |
| Equity Risk Parity | -18.93% | $1.34 | 1.88x |
| Equity Reliability-Gated Sentiment | -15.62% | $1.19 | 11.19x |

### 3.1 There is no universal “best” fund

| Desired outcome | Strongest sample candidate | Why | Principal drawback |
|---|---|---|---|
| Highest return | Crypto Minimum Variance | 60.04% annualised | -72.99% drawdown, 72.94% volatility and high concentration |
| Highest Sharpe | Crypto Minimum Variance | 1.01, the highest return per unit of volatility | Sharpe does not neutralise catastrophic loss severity |
| Lowest volatility | Combined Minimum Variance | 12.62% | Only 5.99% return, 0.52 Sharpe and 9.86x turnover |
| Shallowest drawdown | Equity Minimum Variance | -15.59% | Lowest return and Sharpe among the ten base funds |
| Best diversified balance in this sample | Combined Risk Parity | 13.29% return, 16.17% volatility, 0.85 Sharpe | Still lost 20.47% from peak and latest crypto weight is only 8.15% |
| Simplicity and low turnover | Equity Equal Weight | 1.00x turnover, 12.87% return and 0.83 Sharpe | Ignores risk differences and had a -20.32% drawdown |
| Demonstrated news extension | Reliability-Gated Sentiment | Return and Sharpe improved modestly over Equity Minimum Variance | Nearly identical path, slightly worse drawdown and higher turnover |

The appropriate “desired output” must therefore be stated as an objective. A capital-stability client,
a growth-seeking client and an innovation-focused marker should not receive the same answer.

## 4. Hypotheses, tests and evidence-based inferences

### H1. Adding crypto improves a fund's risk-adjusted performance

**Test:** compare each combined method with its equity counterpart over the common live dates.

- Equal weight: return rises from 12.87% to 15.10%, but Sharpe falls from 0.83 to 0.77 and drawdown
  worsens from -20.32% to -28.75%.
- Minimum variance: Sharpe rises from 0.49 to 0.52, but the latest combined fund holds only 2.65% in
  crypto and its drawdown is slightly worse.
- Risk parity: return rises from 10.15% to 13.29%, Sharpe rises from 0.72 to 0.85, volatility rises
  from 14.92% to 16.17%, and drawdown worsens from -18.93% to -20.47%.

**Inference:** partially supported. The strongest evidence is for Combined Risk Parity, but adding
crypto does not improve every method or every risk measure.

### H2. Optimisation beats the transparent equal-weight baseline

**Test:** compare minimum variance and risk parity with equal weight inside each family.

- Equity: optimisation reduces volatility and drawdown, but both optimised funds have lower Sharpe
  and return than equal weight.
- Crypto: minimum variance dominates the other crypto variants on return, volatility, Sharpe and
  drawdown inside this sample, but it concentrates 90% in BTC, ETH and TRX at the latest rebalance.
- Combined: risk parity improves Sharpe and downside control relative to equal weight, while minimum
  variance sacrifices substantial return for a smoother path.

**Inference:** supported only conditionally. Optimisation changes the trade-off; it does not
automatically improve every outcome.

### H3. The sentiment extension adds investment value

**Test:** compare the same Equity Minimum Variance base before and after the reliability-gated tilt.

- Annualised return increases by 0.52 percentage points, from 5.57% to 6.09%.
- Sharpe increases by 0.039, from 0.492 to 0.531.
- Maximum drawdown is 0.028 percentage points worse, from -15.593% to -15.621%.
- Total turnover increases by about 1.00x, from 10.19x to 11.19x.
- The two daily return paths correlate at 0.998.

**Inference:** weak, positive in-sample-of-the-live-backtest evidence, not a new return engine. The
extension is more defensible as a transparent, look-ahead-safe product experiment than as proof that
headline sentiment predicts returns.

### H4. Minimum variance provides capital protection

**Test:** compare volatility and drawdown, not the method name.

**Inference:** relatively supported within the sample. Equity and Combined Minimum Variance have the
lowest volatility and shallowest drawdowns. It is not absolute protection: losses still reached about
15.6%, and covariance estimates can change outside the sample.

### H5. The combined funds are meaningfully multi-asset

**Test:** inspect latest asset-class weights.

- Combined Equal Weight: 16.67% crypto.
- Combined Risk Parity: 8.15% crypto.
- Combined Minimum Variance: 2.65% crypto.

**Inference:** true by construction, but economically weak for Combined Minimum Variance. “Combined”
should not be presented as an equal asset-class balance.

### H6. The funds are investable now

**Test:** separate model implementability from production readiness.

**Inference:** the rules are implementable as a prototype because they are long-only, capped,
monthly, cost-adjusted and produce current target weights. They are not yet production-investable.
There is no live execution evidence, calibrated slippage, capacity analysis, custody design, fee model,
tax treatment, regulatory approval, client suitability process or post-2023 validation.

## 5. Concentration and diversification evidence

- Combined Minimum Variance has 57.16% in its five largest latest holdings and only 2.65% in crypto.
- Equity Minimum Variance has 60.89% in its five largest latest holdings.
- Crypto Minimum Variance has 90.00% in BTC, ETH and TRX, and 96.80% in its top five holdings.
- Combined Risk Parity has 13.71% in its top five latest holdings, the broadest combined candidate.
- Equity Risk Parity has 14.93% in its top five latest holdings.
- The three crypto fund return paths correlate between 0.966 and 0.999 in the live sample. Owning
  several crypto funds therefore adds little independent diversification.
- Equity Minimum Variance and its sentiment extension correlate at 0.998. Treating them as two
  independent funds in the allocation lab would overstate diversification.

## 6. What “the model is working” must mean

| Level | Current conclusion | Evidence | What is still missing |
|---|---|---|---|
| Code function | Yes | Pipeline completes; all required artifacts regenerate | Continued maintenance on another machine |
| Mechanical correctness | Yes, within tested rules | Past-only weights, caps, sums, lags and filenames pass tests | Independent code review |
| Course compliance | Substantially yes | Ten funds, OOS fact sheets, sector index, fusion, six exhibits and app | Public repo and deployment remain student actions |
| Economic usefulness | Mixed | Several coherent trade-offs; Combined Risk Parity is balanced | Longer and rolling validation |
| Sentiment value | Modest | Small return/Sharpe improvement | Labelled accuracy test and stronger out-of-sample regimes |
| Production investability | No | Prototype assumptions only | Execution, capacity, fees, governance, legal and operations |

## 7. Full Yes/No/Unsure decision checklist

Write one sentence after every **No** or **Unsure** explaining what evidence would change your answer.

### A. Metric understanding

1. [ ] Yes [ ] No [ ] Unsure — I can explain why annualised return is not the same as total return.
2. [ ] Yes [ ] No [ ] Unsure — I understand why geometric compounding is used for the annualised return.
3. [ ] Yes [ ] No [ ] Unsure — I can explain why equity uses 252 and crypto uses 365 periods.
4. [ ] Yes [ ] No [ ] Unsure — I understand that volatility measures variation, not only losses.
5. [ ] Yes [ ] No [ ] Unsure — I can calculate the direction of a Sharpe change when return rises and volatility stays constant.
6. [ ] Yes [ ] No [ ] Unsure — I understand that a Sharpe above another fund is a relative sample result, not a guarantee.
7. [ ] Yes [ ] No [ ] Unsure — I can explain maximum drawdown using peak, trough and recovery.
8. [ ] Yes [ ] No [ ] Unsure — I understand why -15% is a shallower drawdown than -73%.
9. [ ] Yes [ ] No [ ] Unsure — I can explain why turnover creates cost and operational risk.
10. [ ] Yes [ ] No [ ] Unsure — I understand that the 10 bps cost is an assumption rather than observed execution cost.
11. [ ] Yes [ ] No [ ] Unsure — I understand what an ending value of $1.45 means.
12. [ ] Yes [ ] No [ ] Unsure — I can explain why one attractive metric cannot define “best”.

### B. Backtest design and leakage

13. [ ] Yes [ ] No [ ] Unsure — I understand that every live weight uses only earlier returns.
14. [ ] Yes [ ] No [ ] Unsure — I can explain why the first live date is after the estimation window.
15. [ ] Yes [ ] No [ ] Unsure — I understand monthly rebalancing and when a target becomes active.
16. [ ] Yes [ ] No [ ] Unsure — I can explain why crypto returns are calculated on the seven-day calendar first.
17. [ ] Yes [ ] No [ ] Unsure — I understand why combined funds use the equity decision calendar.
18. [ ] Yes [ ] No [ ] Unsure — I can distinguish look-ahead bias from selection bias.
19. [ ] Yes [ ] No [ ] Unsure — I accept the zero risk-free-rate assumption for this course analysis.
20. [ ] Yes [ ] No [ ] Unsure — I accept a one-year rolling estimation window as my design choice.
21. [ ] Yes [ ] No [ ] Unsure — I understand covariance shrinkage and why it is used for minimum variance.
22. [ ] Yes [ ] No [ ] Unsure — I will call the implemented risk parity “inverse-volatility risk parity”, not full-covariance equal-risk contribution.

### C. Fund objective and personal preference

23. [ ] Yes [ ] No [ ] Unsure — My primary objective is capital stability rather than maximum growth.
24. [ ] Yes [ ] No [ ] Unsure — I would accept a modeled 20% peak-to-trough loss for higher return.
25. [ ] Yes [ ] No [ ] Unsure — I would accept a modeled 73% peak-to-trough loss for the crypto return opportunity.
26. [ ] Yes [ ] No [ ] Unsure — I prefer a simple equal-weight rule to an estimate-sensitive optimiser.
27. [ ] Yes [ ] No [ ] Unsure — I value low turnover enough to reject a small return improvement.
28. [ ] Yes [ ] No [ ] Unsure — I require meaningful crypto exposure in a fund labelled combined.
29. [ ] Yes [ ] No [ ] Unsure — I consider an 8.15% latest crypto weight meaningful for Combined Risk Parity.
30. [ ] Yes [ ] No [ ] Unsure — I consider a 2.65% latest crypto weight meaningful for Combined Minimum Variance.
31. [ ] Yes [ ] No [ ] Unsure — I would select Combined Risk Parity as the balanced flagship fund.
32. [ ] Yes [ ] No [ ] Unsure — I would keep Combined Minimum Variance as a lower-volatility alternative.
33. [ ] Yes [ ] No [ ] Unsure — I would keep Equity Equal Weight as the simple transparent benchmark.
34. [ ] Yes [ ] No [ ] Unsure — I would label every crypto-only fund high risk regardless of Sharpe.

### D. Reading the actual fund evidence

35. [ ] Yes [ ] No [ ] Unsure — I can explain why Crypto Minimum Variance has the best Sharpe but is not the safest fund.
36. [ ] Yes [ ] No [ ] Unsure — I can explain why Equity Minimum Variance reduces risk but has weak return efficiency.
37. [ ] Yes [ ] No [ ] Unsure — I can explain why Combined Risk Parity is preferred over Combined Equal Weight for balance.
38. [ ] Yes [ ] No [ ] Unsure — I understand that Combined Equal Weight delivered more return but a worse drawdown than Combined Risk Parity.
39. [ ] Yes [ ] No [ ] Unsure — I understand that the strongest crypto result may be regime-specific.
40. [ ] Yes [ ] No [ ] Unsure — I accept that three live years are insufficient to establish persistent superiority.
41. [ ] Yes [ ] No [ ] Unsure — I can identify the best fund under at least three different objectives.
42. [ ] Yes [ ] No [ ] Unsure — I will not describe a historical rank as an expected future rank.

### E. Holdings and concentration

43. [ ] Yes [ ] No [ ] Unsure — I have inspected the latest holdings for all funds in the app.
44. [ ] Yes [ ] No [ ] Unsure — I accept 60.89% top-five concentration in Equity Minimum Variance.
45. [ ] Yes [ ] No [ ] Unsure — I accept 90% concentration in the top three Crypto Minimum Variance holdings.
46. [ ] Yes [ ] No [ ] Unsure — I understand that a single-name cap does not guarantee broad diversification.
47. [ ] Yes [ ] No [ ] Unsure — I understand that owning two highly correlated offered funds can duplicate exposure.
48. [ ] Yes [ ] No [ ] Unsure — I would warn users when an allocation includes overlapping underlying holdings.
49. [ ] Yes [ ] No [ ] Unsure — I can explain why risk parity is more broadly spread than minimum variance here.
50. [ ] Yes [ ] No [ ] Unsure — I accept the chosen 20%, 30% and 15% position caps.

### F. Sentiment model and fusion

51. [ ] Yes [ ] No [ ] Unsure — I can explain why headline casing, punctuation and negation are retained for VADER.
52. [ ] Yes [ ] No [ ] Unsure — I understand why a weekend headline is mapped forward and then lagged again.
53. [ ] Yes [ ] No [ ] Unsure — I accept neutral zero as the primary no-news rule.
54. [ ] Yes [ ] No [ ] Unsure — I understand the observed-only sensitivity and the 0.0356 mean absolute difference.
55. [ ] Yes [ ] No [ ] Unsure — I can explain the purpose of the 18-term finance lexicon.
56. [ ] Yes [ ] No [ ] Unsure — I accept that the lexicon was defined transparently but not independently labelled and validated.
57. [ ] Yes [ ] No [ ] Unsure — I understand that finance augmentation changes the sign of only 2.48% of headlines.
58. [ ] Yes [ ] No [ ] Unsure — I understand that 46.83% of augmented scores remain exactly neutral.
59. [ ] Yes [ ] No [ ] Unsure — I can explain why publisher missingness weakens reliability assessment.
60. [ ] Yes [ ] No [ ] Unsure — I will describe the fusion result as modest and non-causal.
61. [ ] Yes [ ] No [ ] Unsure — I consider a 0.52 percentage-point return increase worth about 1.00x extra turnover.
62. [ ] Yes [ ] No [ ] Unsure — I understand why 0.998 correlation means the augmented fund is not a distinct return source.

### G. Data and model limitations

63. [ ] Yes [ ] No [ ] Unsure — I understand why adjusted close, not all OHLC columns, drives return estimation.
64. [ ] Yes [ ] No [ ] Unsure — I can explain the diagnostic role of OHLCV, publisher and URL fields.
65. [ ] Yes [ ] No [ ] Unsure — I understand why 2,847 duplicate headlines were removed.
66. [ ] Yes [ ] No [ ] Unsure — I understand why ten crypto rows after 31 December 2023 were excluded.
67. [ ] Yes [ ] No [ ] Unsure — I accept retaining plausible extreme market returns rather than silently deleting them.
68. [ ] Yes [ ] No [ ] Unsure — I recognise survivorship and universe-selection risk in the supplied sample.
69. [ ] Yes [ ] No [ ] Unsure — I recognise covariance estimation error in a short rolling window.
70. [ ] Yes [ ] No [ ] Unsure — I recognise that one historical regime cannot establish robustness.
71. [ ] Yes [ ] No [ ] Unsure — I would test rolling subperiods and later data before commercial use.
72. [ ] Yes [ ] No [ ] Unsure — I would test higher transaction costs, spread and market impact before commercial use.

### H. Investability and product governance

73. [ ] Yes [ ] No [ ] Unsure — I distinguish an investable fund concept from a production-ready financial product.
74. [ ] Yes [ ] No [ ] Unsure — I understand that no live trades or fills validate the modeled weights.
75. [ ] Yes [ ] No [ ] Unsure — I understand that backtested liquidity proxies do not prove execution capacity.
76. [ ] Yes [ ] No [ ] Unsure — I would define management fees before showing net client returns.
77. [ ] Yes [ ] No [ ] Unsure — I would define custody and venue rules for crypto assets.
78. [ ] Yes [ ] No [ ] Unsure — I would include tax, legal, regulatory and client-suitability review.
79. [ ] Yes [ ] No [ ] Unsure — I would establish rebalance controls and exception handling.
80. [ ] Yes [ ] No [ ] Unsure — I would monitor realised slippage against the 10 bps assumption.
81. [ ] Yes [ ] No [ ] Unsure — I would monitor concentration, turnover and drawdown limits after launch.
82. [ ] Yes [ ] No [ ] Unsure — I would pause or review a fund after a predeclared governance trigger.

### I. Report authorship and defensible claims

83. [ ] Yes [ ] No [ ] Unsure — I have personally checked every percentage in the report against the regenerated tables.
84. [ ] Yes [ ] No [ ] Unsure — I can explain all six figures without reading their captions.
85. [ ] Yes [ ] No [ ] Unsure — I agree that Combined Risk Parity is the most balanced flagship in this sample.
86. [ ] Yes [ ] No [ ] Unsure — I agree that Crypto Minimum Variance must not be called low risk.
87. [ ] Yes [ ] No [ ] Unsure — I agree that the sentiment result is a modest extension, not causal evidence.
88. [ ] Yes [ ] No [ ] Unsure — I agree that “working prototype” is accurate but “production ready” is not.
89. [ ] Yes [ ] No [ ] Unsure — I have personally opened every external source retained in the references.
90. [ ] Yes [ ] No [ ] Unsure — I can defend the three recommendations in my own words.
91. [ ] Yes [ ] No [ ] Unsure — I have rewritten any sentence that I do not naturally understand or endorse.
92. [ ] Yes [ ] No [ ] Unsure — My final report clearly separates observation, hypothesis, inference and recommendation.

### J. Market position and commercial intent

93. [ ] Yes [ ] No [ ] Unsure — I understand that none of the individual components is unique by itself.
94. [ ] Yes [ ] No [ ] Unsure — I can state the customer problem in one sentence without referring to grades or coursework.
95. [ ] Yes [ ] No [ ] Unsure — My target user is a learner or self-directed investor seeking transparent comparisons.
96. [ ] Yes [ ] No [ ] Unsure — I accept that the first marketable version should be research or education, not custody of client money.
97. [ ] Yes [ ] No [ ] Unsure — I can explain how Signal & Story differs from a robo-adviser.
98. [ ] Yes [ ] No [ ] Unsure — I can explain how Signal & Story differs from a strategy-builder platform.
99. [ ] Yes [ ] No [ ] Unsure — I can explain how Signal & Story differs from institutional news analytics.
100. [ ] Yes [ ] No [ ] Unsure — I would keep the evidence and decision trail as the main product distinction.
101. [ ] Yes [ ] No [ ] Unsure — I would reduce the ten funds to a smaller, clearly tiered commercial menu.
102. [ ] Yes [ ] No [ ] Unsure — I would not market the sentiment tilt as proven alpha.
103. [ ] Yes [ ] No [ ] Unsure — I would run a live shadow portfolio before accepting client money.
104. [ ] Yes [ ] No [ ] Unsure — I would seek legal advice or an appropriately licensed partner before offering advice or dealing.
105. [ ] Yes [ ] No [ ] Unsure — I would define fees and demonstrate value after all fees.
106. [ ] Yes [ ] No [ ] Unsure — I would test willingness to pay with target users rather than infer it from backtest performance.
107. [ ] Yes [ ] No [ ] Unsure — I can identify a credible reason a user would switch from a low-cost ETF portfolio.
108. [ ] Yes [ ] No [ ] Unsure — I can identify a credible reason a user would not switch.
109. [ ] Yes [ ] No [ ] Unsure — I understand that product-market fit has not yet been demonstrated.
110. [ ] Yes [ ] No [ ] Unsure — I can defend why this model is the right prototype for the stated customer problem.

## 8. Comparable products and models at scale

Signal & Story is not a direct copy of one scaled product. It overlaps with several established
categories. This is useful evidence that the problem is real, but it also means “systematic” or “AI
sentiment” alone is not a market position.

| Comparator | What exists at scale | Similarity to Signal & Story | Important difference |
|---|---|---|---|
| [Wealthfront Automated Investing](https://www.wealthfront.com/) | Automated portfolios of stocks, bonds and ETFs, assigned through a risk score | Investor onboarding, diversified portfolios and automation | Broader household product and operational infrastructure; Signal & Story is a transparent prototype with direct equity/crypto models |
| [Stockspot](https://www.stockspot.com.au/what-are-etfs/our-chosen-etfs/) | Australian model and sustainable portfolios using diversified low-fee ETFs | Australian investor journey and managed portfolio comparison | ETF implementation, adviser operations and broad asset classes rather than ten direct systematic funds and headline fusion |
| [Betashares Direct](https://www.betashares.com.au/direct/custom-portfolios) | Custom portfolios, screening, automatic reinvestment and rebalancing | User-controlled allocation and automated portfolio maintenance | Execution and tax/reporting platform; it does not make your specific risk-parity and sentiment research the product |
| [Composer by SoFi](https://www.composer.trade/) | Build, backtest and execute rules-based strategies; its site reports more than $37bn trading volume, 18m orders and 2m rebalances | Rule transparency, backtesting and user-directed systematic investing | Strategy-building marketplace and execution infrastructure rather than a curated fact-sheet fund menu |
| [eToro Smart Portfolios](https://www.etoro.com/investing/portfolios/) | Curated long-term portfolios across investment themes; eToro has also launched data-driven crypto portfolios | Packaged portfolio ideas, crypto access and investor-facing charts | Primarily thematic/curated portfolios; methodology and evidence journey differ from your constrained multi-method comparison |
| [AQR risk-allocation research and funds](https://www.aqr.com/-/media/AQR/Documents/Insights/Alternative-Thinking/Alternative-Thinking-Strategic-Portfolio-Construction.pdf) | Institutional risk-balanced portfolios across market risk premia and alternative strategies | Risk parity and systematic multi-asset allocation | Far wider asset classes, research depth and institutional implementation; your risk parity is inverse volatility under a diagonal covariance assumption |
| [BlackRock Systematic Active Equity](https://www.blackrock.com/au/solutions/systematic-active-equity) | Big data, algorithms and human expertise used to select stocks; its systematic material describes sentiment signals from electronic text | Structured and unstructured data combined in investment models | Institutional scale, extensive data and signal libraries; your model uses a small transparent lexicon and course headline sample |
| [RavenPack News Analytics](https://www.ravenpack.com/products/edge/data/news-analytics) | News analytics from more than 40,000 sources for allocation, risk and trading use cases | Sector sentiment, signal construction and news-based risk information | Enterprise data product with point-in-time tagging and much larger coverage; your strength is transparency, not data scale |

One especially useful caution is that Wealthfront's own support page states that its Risk Parity Fund
was liquidated in January 2025. A valid portfolio method is therefore not, by itself, a durable product
or business moat. [Wealthfront risk-parity update](https://support.wealthfront.com/hc/en-us/articles/29855382055060-Important-Updates-Regarding-the-Risk-Parity-Fund).

## 9. Is Signal & Story marketable?

### 9.1 Short answer

**Marketable as an educational and research prototype: yes. Marketable today as a retail managed-fund
or automated-advice business: no.**

The current product has a clear demonstration value: it makes risk-return trade-offs visible, lets a
user inspect holdings, exposes model assumptions, preserves the supplied data audit and shows a
look-ahead-safe sentiment experiment. That is credible for a portfolio-learning lab, a graduate
showcase, an adviser research prototype or a paper-investing tool.

It has not demonstrated product-market fit or legal/operational readiness. In Australia, ASIC states
that financial product advice requires authorisation under an Australian financial services licence,
and its digital-advice guidance covers licensing through actual delivery. Operating a registered
managed investment scheme, custody and dealing can also create licensing obligations. The 2026 digital
asset reforms add another moving layer. This is not legal advice; it is a reason to keep the product in
research mode until qualified advice and the right authorisations or partnerships are obtained.

- [ASIC: Giving financial product advice](https://www.asic.gov.au/regulatory-resources/financial-services/giving-financial-product-advice/)
- [ASIC RG 255: Digital financial product advice](https://www.asic.gov.au/regulatory-resources/find-a-document/regulatory-guides/rg-255-providing-digital-financial-product-advice-to-retail-clients)
- [ASIC: Do you need an AFS licence?](https://www.asic.gov.au/for-finance-professionals/afs-licensees/do-you-need-an-afs-licence/)
- [ASIC: Digital-assets reform roadmap](https://asic.gov.au/about-asic/news-centre/news-items/asic-s-roadmap-for-digital-assets-law-reform-implementation/)
- [Moneysmart: Crypto assets](https://moneysmart.gov.au/complex-investment-products/crypto-assets)

### 9.2 Marketability scorecard

| Dimension | Current state | Decision |
|---|---|---|
| Customer problem | Comparing opaque risk, return, holdings and news evidence is a genuine problem | Credible |
| Target segment | Not yet explicitly narrowed | Must choose one |
| Differentiation | Evidence-first decision trail, multi-method comparison and transparent sentiment gate | Promising but easy to imitate |
| Performance evidence | Three-year OOS record with coherent relative results | Too short for commercial claims |
| Sentiment evidence | Small positive change, openly measured | Interesting, not proven alpha |
| User experience | Complete prototype journey and downloadable allocation audit | Strong for coursework/MVP |
| Data advantage | No proprietary or real-time data moat | Weak |
| Execution and custody | Not implemented | Blocker |
| Fees and unit economics | Not defined | Blocker |
| Legal and governance | Not implemented | Blocker |
| Distribution and trust | No live users, partner or track record | Blocker |

### 9.3 The most defensible first customer and product

The best initial positioning is **an evidence-first portfolio learning and research lab for self-directed
investors**, not “an AI fund that beats the market”. The customer promise could be:

> Compare simple and optimised equity, crypto and combined portfolios; see exactly what drove each
> risk result; test an allocation; and understand when news sentiment changes the decision.

This position uses what the prototype genuinely does well and avoids claiming regulated execution or
prediction. A sensible staged path is:

1. educational dashboard with delayed data and no personalised recommendation;
2. live shadow portfolios with predeclared rules, incident logs and performance attribution;
3. user research testing whether the evidence trail improves decisions and whether anyone will pay;
4. calibrated costs, capacity, custody, fee and tax analysis;
5. independent model validation and security review; and
6. only then, a licensed partnership or properly advised regulatory path to execution.

## 10. Why this model rather than another model?

The defensible answer is not “because it has the highest return”. The model family was chosen because
the product must teach and expose different portfolio objectives using the supplied data:

- **Equal weight** is the transparent baseline. It has minimal estimation risk and low turnover.
- **Minimum variance** asks how smooth the portfolio can be using past covariance. It exposes the cost
  of stability: lower return, higher concentration and higher turnover in this sample.
- **Inverse-volatility risk parity** spreads exposure according to standalone risk without relying on
  expected returns. It produced the best combined-fund balance here and is easier to explain than a
  full covariance risk-budget solver.
- **Equity, crypto and combined families** reveal that asset-class choice can dominate optimiser choice.
  This prevents a user from mistaking an algorithm name for the source of performance.
- **The reliability-gated sentiment tilt** directly uses the supplied unstructured data while respecting
  coverage weakness and a trading lag. Its modest result is more credible than an exaggerated AI claim.
- **Precomputed artifacts and a lightweight app** make every fact-sheet number traceable and keep the
  product runnable on a basic deployment.

The commercial “why” is therefore **transparent decision quality**, not proprietary forecasting. The
model shows what a user gains and gives up under each objective. Its weakness is that transparency can
be copied. A lasting advantage would require a trusted live record, superior data, validated decision
outcomes, distinctive user workflow or distribution partnership.

## 11. Your market decision record

1. My first customer is ____________________ who struggles with ________________________________.
2. My one-sentence value proposition is ______________________________________________________.
3. The closest competitor is ____________________ and I differ because ________________________.
4. The feature users cannot easily obtain elsewhere is ______________________________________.
5. The first evidence of willingness to pay would be ________________________________________.
6. I will market this first as [ ] education [ ] research [ ] advice [ ] managed investment.
7. I will remove or change ____________________ before showing it to a real user.
8. I will consider execution only after ______________________________________________________.

## 12. Your investment decision record

Complete these sentences in your own words.

1. My flagship fund is ____________________ because ________________________________.
2. The metric I prioritise is ____________________ because ___________________________.
3. The maximum drawdown I regard as tolerable for this product is ___________________.
4. I will / will not offer crypto-only funds because _________________________________.
5. I will / will not keep the sentiment fund because ________________________________.
6. The strongest evidence that the model works is _________________________________ .
7. The strongest evidence against overconfidence is ________________________________.
8. The first additional test I would run is ________________________________________.
9. The result that surprised me most is ____________________________________________.
10. The claim I changed after reviewing the evidence is _____________________________.

## 13. A defensible conclusion you should be able to reach independently

The evidence supports calling Signal & Story a functioning, course-aligned prototype. The pipeline
regenerates ten long-only, capped, cost-adjusted, walk-forward funds; the app exposes fact sheets,
holdings, allocation analysis and sentiment; and the required files and exhibits agree. Combined Risk
Parity is the most balanced diversified candidate in this particular sample, not a universal winner.
Crypto Minimum Variance has the strongest return and Sharpe, but its drawdown and concentration make
it a high-risk satellite at most. The sentiment extension works technically and improves two headline
metrics modestly, but it is nearly identical to its base fund and does not establish prediction or
causality. The funds are model-implementable, but none should be described as production-investable
until longer validation, execution, fee, capacity, governance and regulatory work is completed.

Do not copy that paragraph automatically. If you cannot reproduce its logic from the tables, return to
the corresponding checklist section and mark the item **Unsure**.

## 14. Evidence map

- Fund metrics: `results/tables/performance_metrics.csv`
- Daily returns, growth and drawdowns: `results/data/fund_returns.csv`
- Historical and latest weights: `results/data/fund_weights.csv`
- Latest holdings: `results/tables/current_holdings.csv`
- Sentiment index: `results/data/sector_sentiment_index.csv`
- Sentiment validation: `results/tables/sentiment_validation.csv`
- Fusion comparison: `results/tables/fusion_comparison.csv`
- Model decisions: `results/tables/model_specification.csv`
- Crypto-sleeve sensitivity: `results/tables/crypto_sleeve_floor_sensitivity.csv`
- Supplied-field use: `results/tables/asset_data_use_register.csv`
- Data integrity audit: `results/tables/carried_forward_integrity_audit.csv`
- Final report: `report/report.docx` and `report/report.pdf`

## 15. Is the movie-plus-finance sentiment direction correct?

### 15.1 Verdict

**Green flag:** use a movie-review benchmark to test general evaluative language, then use a separate
expert-labelled finance benchmark to test investor meaning. Compare standard VADER with the finance
extension in both domains.

**Amber flag:** star ratings and movie preferences are noisy labels. A person can give three stars to a
film they enjoyed, or one star because of delivery, politics or platform experience rather than the
language in the review. Report subgroup results and disagreement rather than assuming perfect labels.

**Red flag:** never use Marvel, Disney, Netflix, Prime, Australian casts or movie star ratings as
investment signals. They may be review-analysis tags only. Do not merge movie and finance examples into
one accuracy figure because “positive” has a different target meaning in each domain.

### 15.2 Define positive, neutral and negative before testing

For a **five-star movie scale**, the proposed predeclared mapping is:

- 1-2 stars: negative;
- 3 stars: neutral; and
- 4-5 stars: positive.

For a **ten-point movie scale**, the equivalent mapping is:

- 1-4: negative;
- 5-6: neutral; and
- 7-10: positive.

For **finance**, label from the perspective of the named company's investor:

- positive: the sentence contains explicit information reasonably favourable to firm value or outlook;
- negative: it contains explicit information reasonably adverse to firm value or outlook; and
- neutral: it has no clear directional economic implication from the text alone.

Do not label a finance sentence positive merely because it contains a pleasant word. “Costs fell” may be
positive; “revenue fell” is negative; “the meeting will occur on Tuesday” is neutral. Entity direction
matters when a headline names more than one company.

### 15.3 What the current external stress test says

The NLTK movie-review corpus contains 2,000 binary positive/negative reviews. It does not contain star
ratings, platform, franchise, cast-nationality or preference fields. Standard VADER achieved 63.50%
accuracy and approximately 0.621 macro-F1. The finance-augmented version also achieved 63.50% accuracy
and approximately 0.621 macro-F1. Therefore, the 18 finance terms did not materially damage this coarse
general-language benchmark. This is a useful non-degradation check, not proof of high accuracy.

The star-labelled movie test and expert-labelled finance test are correctly flagged as not yet run in
`results/tables/dual_domain_sentiment_validation.csv`. For coursework, a properly licensed
Financial PhraseBank configuration can be used with attribution. Its dataset card states a
CC BY-NC-SA 3.0 licence and requires separate permission for commercial use. For a marketable product,
use a licensed commercial benchmark or a documented proprietary human-labelled holdout.

### 15.4 Long direction checklist

#### A. Label design

- S1. [ ] Yes [ ] No [ ] Unsure — I will define rating thresholds before looking at model results.
- S2. [ ] Yes [ ] No [ ] Unsure — I accept 1-2/3/4-5 as negative/neutral/positive on a five-star scale.
- S3. [ ] Yes [ ] No [ ] Unsure — I accept 1-4/5-6/7-10 on a ten-point scale.
- S4. [ ] Yes [ ] No [ ] Unsure — I will preserve the original star value as well as the mapped label.
- S5. [ ] Yes [ ] No [ ] Unsure — I understand that a star label is a proxy for reviewer satisfaction.
- S6. [ ] Yes [ ] No [ ] Unsure — I will not infer a missing star rating from the review text.
- S7. [ ] Yes [ ] No [ ] Unsure — I will define finance sentiment from an investor perspective.
- S8. [ ] Yes [ ] No [ ] Unsure — I will label multi-company finance text at entity level or exclude it.
- S9. [ ] Yes [ ] No [ ] Unsure — I will retain neutral as a genuine class in finance.
- S10. [ ] Yes [ ] No [ ] Unsure — I will document annotator disagreement rather than erase it.

#### B. Movie preference and metadata slices

- S11. [ ] Yes [ ] No [ ] Unsure — Marvel is a franchise tag, not a sentiment label.
- S12. [ ] Yes [ ] No [ ] Unsure — Disney is a studio/distributor tag, not a sentiment label.
- S13. [ ] Yes [ ] No [ ] Unsure — Netflix and Prime are platform tags and may change by date or region.
- S14. [ ] Yes [ ] No [ ] Unsure — Australian cast is a metadata slice, not a positive or negative class.
- S15. [ ] Yes [ ] No [ ] Unsure — I will define “Australian cast” from a reliable source, not name guessing.
- S16. [ ] Yes [ ] No [ ] Unsure — I understand that one film can be Marvel, Disney and available on a platform.
- S17. [ ] Yes [ ] No [ ] Unsure — I will allow overlapping slice tags rather than force false exclusivity.
- S18. [ ] Yes [ ] No [ ] Unsure — I will record review date and country when platform availability matters.
- S19. [ ] Yes [ ] No [ ] Unsure — I will treat stated genre preference as a subgroup, not ground truth.
- S20. [ ] Yes [ ] No [ ] Unsure — I will compare preference-match and preference-mismatch performance.

#### C. Data rights and sample integrity

- S21. [ ] Yes [ ] No [ ] Unsure — I have a legitimate licence for every review dataset used.
- S22. [ ] Yes [ ] No [ ] Unsure — I will not redistribute Financial PhraseBank commercially under its research licence.
- S23. [ ] Yes [ ] No [ ] Unsure — I will not scrape Netflix, Prime or another platform contrary to its terms.
- S24. [ ] Yes [ ] No [ ] Unsure — I will remove exact duplicate reviews before splitting data.
- S25. [ ] Yes [ ] No [ ] Unsure — Reviews for the same film will not leak across tuning and test sets.
- S26. [ ] Yes [ ] No [ ] Unsure — I will report class counts for positive, neutral and negative.
- S27. [ ] Yes [ ] No [ ] Unsure — I will report sample counts for every platform/franchise/cast slice.
- S28. [ ] Yes [ ] No [ ] Unsure — I will not publish a subgroup metric with too few observations.
- S29. [ ] Yes [ ] No [ ] Unsure — I will preserve punctuation, casing, negation, emoji and intensifiers for VADER.
- S30. [ ] Yes [ ] No [ ] Unsure — I will separate review text from unrelated delivery or customer-service complaints.

#### D. Model comparison

- S31. [ ] Yes [ ] No [ ] Unsure — Standard VADER is the predeclared baseline.
- S32. [ ] Yes [ ] No [ ] Unsure — Finance-augmented VADER is tested on exactly the same examples.
- S33. [ ] Yes [ ] No [ ] Unsure — Thresholds are not tuned on the final test set.
- S34. [ ] Yes [ ] No [ ] Unsure — I will report accuracy and macro-F1, not accuracy alone.
- S35. [ ] Yes [ ] No [ ] Unsure — I will inspect precision and recall for each class.
- S36. [ ] Yes [ ] No [ ] Unsure — I will inspect a confusion matrix, especially neutral errors.
- S37. [ ] Yes [ ] No [ ] Unsure — I will manually inspect false positives and false negatives.
- S38. [ ] Yes [ ] No [ ] Unsure — I will test whether the finance lexicon harms movie-review performance.
- S39. [ ] Yes [ ] No [ ] Unsure — I will test whether the finance lexicon improves expert-labelled finance performance.
- S40. [ ] Yes [ ] No [ ] Unsure — I will reject the extension if it only changes scores without improving valid labels.

#### E. Matching the domains correctly

- S41. [ ] Yes [ ] No [ ] Unsure — Movie and finance results remain separate in the scorecard.
- S42. [ ] Yes [ ] No [ ] Unsure — I will not average movie and finance accuracy into one headline number.
- S43. [ ] Yes [ ] No [ ] Unsure — General-domain non-degradation and finance-domain improvement are separate gates.
- S44. [ ] Yes [ ] No [ ] Unsure — Movie preference never enters the portfolio optimiser.
- S45. [ ] Yes [ ] No [ ] Unsure — Star ratings never enter the portfolio optimiser.
- S46. [ ] Yes [ ] No [ ] Unsure — Finance sentiment remains lagged before investment use.
- S47. [ ] Yes [ ] No [ ] Unsure — A good movie benchmark does not prove finance validity.
- S48. [ ] Yes [ ] No [ ] Unsure — A good finance benchmark does not prove return predictability.
- S49. [ ] Yes [ ] No [ ] Unsure — Classification value and portfolio value are evaluated separately.
- S50. [ ] Yes [ ] No [ ] Unsure — I will keep the current sentiment claim modest until both gates pass.

#### F. Product decision

- S51. [ ] Yes [ ] No [ ] Unsure — The movie benchmark will be shown as model assurance, not an investor feature.
- S52. [ ] Yes [ ] No [ ] Unsure — The app will explain why two validation domains are used.
- S53. [ ] Yes [ ] No [ ] Unsure — Users will see the finance label definition before interpreting scores.
- S54. [ ] Yes [ ] No [ ] Unsure — Users will see coverage and reliability beside sentiment.
- S55. [ ] Yes [ ] No [ ] Unsure — A subgroup failure will be disclosed even if aggregate accuracy is acceptable.
- S56. [ ] Yes [ ] No [ ] Unsure — I will predeclare the maximum acceptable general-domain deterioration.
- S57. [ ] Yes [ ] No [ ] Unsure — I will predeclare the finance improvement required to keep the lexicon.
- S58. [ ] Yes [ ] No [ ] Unsure — I will not call a lexicon “AI learning”; it is a transparent rule extension.
- S59. [ ] Yes [ ] No [ ] Unsure — I will distinguish sentiment classification from causal return prediction.
- S60. [ ] Yes [ ] No [ ] Unsure — My final direction is dual-domain validation, not movie-driven investing.

## 16. Week 10 course-alignment checklist

The supplied Week 10 revision deck is a worked reference, not an instruction to
force every number to match. Use `student_review/WEEK10_AND_MARKET_FEASIBILITY_PLAN.md`
for the exact Sharpe comparison and evidence map.

### A. Structured funds and benchmarks

- W1. [ ] Yes [ ] No [ ] Unsure — I understand why out-of-sample performance is the investable evidence and in-sample performance is not.
- W2. [ ] Yes [ ] No [ ] Unsure — I can explain how each monthly weight uses only information available before its live date.
- W3. [ ] Yes [ ] No [ ] Unsure — I understand the difference between this project's rolling one-year window and Week 10's expanding window.
- W4. [ ] Yes [ ] No [ ] Unsure — I can explain why equity/combined use 252 and crypto uses 365 annualisation periods.
- W5. [ ] Yes [ ] No [ ] Unsure — I know that the brief's minimum is two combined methods, not exactly twelve funds.
- W6. [ ] Yes [ ] No [ ] Unsure — I can defend the choice to offer Equal Weight, Minimum Variance and Risk Parity.
- W7. [ ] Yes [ ] No [ ] Unsure — I can explain that tangency was omitted because expected-return estimates can create unstable out-of-sample weights.
- W8. [ ] Yes [ ] No [ ] Unsure — I will not say this project beats tangency because it was not run here.
- W9. [ ] Yes [ ] No [ ] Unsure — I understand why Equal Weight is a serious benchmark rather than a naive failure.
- W10. [ ] Yes [ ] No [ ] Unsure — I will compare return, volatility, Sharpe and drawdown together rather than select the highest ending value.

### B. Exact Week 10 comparison

- W11. [ ] Yes [ ] No [ ] Unsure — I know Combined Risk Parity exceeds the Week 10 Sharpe reference by about 0.07 under a different specification.
- W12. [ ] Yes [ ] No [ ] Unsure — I know Combined Equal Weight is only about 0.01 above the lecture and should be called approximately tied.
- W13. [ ] Yes [ ] No [ ] Unsure — I know the other seven comparable core Sharpe results are below the lecture reference.
- W14. [ ] Yes [ ] No [ ] Unsure — I will not hide the below-reference results.
- W15. [ ] Yes [ ] No [ ] Unsure — I understand that different windows, caps, shrinkage and costs prevent a clean product-performance league table.
- W16. [ ] Yes [ ] No [ ] Unsure — I understand why repeatedly tuning until every benchmark is beaten would be overfitting.
- W17. [ ] Yes [ ] No [ ] Unsure — I can explain Week 10's example where a discovery Sharpe of 0.84 fell to 0.08 in the holdout.
- W18. [ ] Yes [ ] No [ ] Unsure — I accept that a negative extension result can still earn innovation credit when carefully evidenced.
- W19. [ ] Yes [ ] No [ ] Unsure — I will describe Combined Risk Parity as the strongest combined trade-off in this sample, not a universal winner.
- W20. [ ] Yes [ ] No [ ] Unsure — I will disclose that Crypto Minimum Variance has a 1.01 Sharpe and a -72.99% maximum drawdown.

### C. Sentiment, app and submission

- W21. [ ] Yes [ ] No [ ] Unsure — I understand why VADER text must preserve casing, punctuation, boosters and negation.
- W22. [ ] Yes [ ] No [ ] Unsure — I understand that a zero VADER score may be neutral language or missing news.
- W23. [ ] Yes [ ] No [ ] Unsure — I can explain equal-weight ticker aggregation, the no-news rule and the one-trading-day lag.
- W24. [ ] Yes [ ] No [ ] Unsure — I know the sentiment fund's Sharpe improvement from 0.49 to 0.53 is small and not causal proof.
- W25. [ ] Yes [ ] No [ ] Unsure — I know the expert-labelled finance holdout remains a blocker before strong validity claims.
- W26. [ ] Yes [ ] No [ ] Unsure — I have checked that every one of the seven Week 10 exhibits is present as a table or figure.
- W27. [ ] Yes [ ] No [ ] Unsure — I have tested compare, fact sheet, holdings, allocation and sentiment journeys locally.
- W28. [ ] Yes [ ] No [ ] Unsure — I understand why the app loads precomputed artifacts instead of rebuilding models on each click.
- W29. [ ] Yes [ ] No [ ] Unsure — I know the public GitHub repo, live Streamlit link and logged-out accessibility test remain unfinished by instruction.
- W30. [ ] Yes [ ] No [ ] Unsure — I will submit truthful prompt logs showing AI errors, my checks and my corrections rather than inventing authorship.

## 17. Should the combined fund hold a bigger crypto pool?

### 17.1 Evidence-based flag

All ten cryptocurrencies supplied by the course are already used in the crypto
and combined universes. Therefore, there is no unused asset pool to add without
obtaining new external data and changing the course-data scope. The issue visible
in the Week 10 slide is **allocation size**, not missing crypto names.

At the latest rebalance, crypto is 16.67% of Combined Equal Weight, 8.15% of
Combined Risk Parity and 2.65% of Combined Minimum Variance. The low
minimum-variance allocation is expected: the objective minimises total variance,
so it avoids the most volatile sleeve unless a crypto floor is imposed.

The added walk-forward sensitivity imposes minimum total crypto weights while
keeping the same 60-asset universe, 252-day estimation window, monthly rebalance,
15% per-asset cap and 10 bps turnover cost:

| Minimum crypto sleeve | Return | Volatility | Sharpe | Maximum drawdown | Interpretation |
|---:|---:|---:|---:|---:|---|
| 0% | 5.99% | 12.62% | 0.52 | -15.77% | Existing unconstrained minimum variance |
| 10% | 6.22% | 13.95% | 0.50 | -19.84% | More crypto, but worse Sharpe and downside |
| 20% | 8.10% | 17.44% | 0.53 | -24.93% | Roughly equal Sharpe with materially deeper loss |
| 30% | 12.60% | 22.79% | 0.63 | -32.88% | Higher return and Sharpe, but approximately twice the baseline drawdown |

Even the 30% floor remains below Combined Equal Weight's 0.77 Sharpe and Combined
Risk Parity's 0.85 Sharpe. This is evidence for offering a **crypto-risk choice**,
not evidence that forcing more crypto makes minimum variance superior. The four
variants stay research-only in the app.

### 17.2 Crypto-sleeve decision checklist

- C1. [ ] Yes [ ] No [ ] Unsure — I understand that all ten supplied crypto assets are already used.
- C2. [ ] Yes [ ] No [ ] Unsure — I distinguish a larger asset pool from a larger portfolio allocation.
- C3. [ ] Yes [ ] No [ ] Unsure — I will not add external crypto data without checking course scope, provenance and licences.
- C4. [ ] Yes [ ] No [ ] Unsure — I understand why unconstrained minimum variance allocates very little to volatile crypto.
- C5. [ ] Yes [ ] No [ ] Unsure — I consider 2.65% latest crypto exposure too small for my intended combined-product label.
- C6. [ ] Yes [ ] No [ ] Unsure — I understand that a crypto floor changes the optimisation objective.
- C7. [ ] Yes [ ] No [ ] Unsure — I will label each floor as a separate research specification.
- C8. [ ] Yes [ ] No [ ] Unsure — I know the 10% floor lowers Sharpe from 0.52 to 0.50.
- C9. [ ] Yes [ ] No [ ] Unsure — I know the 20% floor only raises Sharpe to 0.53 while drawdown worsens to -24.93%.
- C10. [ ] Yes [ ] No [ ] Unsure — I know the 30% floor raises Sharpe to 0.63 but drawdown worsens to -32.88%.
- C11. [ ] Yes [ ] No [ ] Unsure — I will not describe the 30% floor as lower risk.
- C12. [ ] Yes [ ] No [ ] Unsure — I know the 30% floor still trails Combined Risk Parity on Sharpe.
- C13. [ ] Yes [ ] No [ ] Unsure — I know the 30% floor still trails Combined Equal Weight on Sharpe.
- C14. [ ] Yes [ ] No [ ] Unsure — I will compare crypto floors under later periods and higher crypto trading costs.
- C15. [ ] Yes [ ] No [ ] Unsure — I will define weekend valuation and trading rules before calling a combined sleeve executable.
- C16. [ ] Yes [ ] No [ ] Unsure — I will test whether stablecoins, failed coins or changing market-cap ranks alter the universe definition.
- C17. [ ] Yes [ ] No [ ] Unsure — I will not select 30% merely because it looks best among the tested floors in this sample.
- C18. [ ] Yes [ ] No [ ] Unsure — I prefer Combined Risk Parity if my objective is the best combined-fund historical Sharpe.
- C19. [ ] Yes [ ] No [ ] Unsure — I prefer an explicit crypto sleeve only if the customer promise requires meaningful crypto exposure.
- C20. [ ] Yes [ ] No [ ] Unsure — I can explain the final crypto-sleeve decision in my own words using both upside and downside evidence.

### 17.3 If external crypto data are added later

The ability to pull more data is useful, but the expanded experiment must remain
separate from the authoritative course-data baseline. Predeclare the selection
rule (for example, top 20 non-stablecoin assets by market capitalisation known at
each rebalance), obtain point-in-time membership rather than today's winners,
retain delisted or failed assets, use prices and volume available at the time,
document source/licence/time zone, screen missingness and stale prices, and apply
liquidity-sensitive costs. Save the result under a new `expanded_universe` label;
never overwrite the four required course artifacts. Compare like with like over
the common date range and report whether the conclusion survives. Without those
controls, a larger pool can make the backtest look better simply because failed
coins disappeared from the selected history.
