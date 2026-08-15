# Authentic Project B AI prompt log

## Entry 1 — scope and continuity

**Date:** 13 August 2026

**Student prompt:**

> Develop the ultimate understanding of part A to the latest one. Make sure it is not stray away from the course requirement. I do worry about the assets data given to me. Why dont we use it all? With the same structure, set up project B and complete it. Do not push to GitHub yet, but I want the prototype to be built. I need you to give prefinalised Project B that I can insert into my PyCharm.

**AI action:** The assistant audited the latest Part A against the official Project B rubric, created a full field-use register, reused the official starter structure, implemented the models and app, and kept all work local.

**Correction produced through execution:** The first risk-parity implementation used a nonlinear equal-risk-contribution optimiser across 50 assets. The solver reached its iteration limit during the real run. The assistant replaced it with transparent inverse-volatility risk parity, which is stable and interpretable as volatility-contribution parity under a diagonal covariance model. The report and labels were revised so the implementation is not misrepresented.

**Reason:** A solver which silently stalls would violate the course warning and could create weights which appear valid without being a solved portfolio. The implemented method must match the stated method.

## Entry 2 — date alignment correction

**AI output/problem:** The first headline alignment run failed because pandas represented the news and equity keys at different datetime precisions (`datetime64[us]` and `datetime64[s]`).

**Correction:** Both keys were converted explicitly to timezone-naive `datetime64[ns]` before `merge_asof`.

**Reason:** Converting both keys explicitly makes the calendar rule reproducible and prevents a version-dependent merge failure.

## Entry 3 — sentiment resource correction

**AI output/problem:** NLTK could not initially download the VADER lexicon in the controlled build environment because proxied network access was blocked.

**Correction:** The build was rerun with the environment's documented trusted-proxy opt-in. The project code still uses the normal NLTK lookup/download path for the student's local machine and the deployed app does not import NLTK.

**Reason:** Sentiment scoring belongs in the offline build. The app must load the precomputed index, which keeps deployment fast and removes a fragile runtime download.

## Entry 4 — empirical verification

**Checks performed by the assistant:**

- ten funds were produced;
- all dated target-weight vectors sum to one within numerical tolerance;
- portfolio caps hold;
- required CSV filenames exist;
- the first live date follows the estimation window;
- 146,830 usable headlines were scored and six end-of-sample headlines were transparently excluded from signal alignment;
- the sentiment extension was compared against the exact base fund after transaction costs.

## Student review required before submission

Complete this section in your own words after inspecting the code and app:

- What I challenged or changed in the model: `[STUDENT TO COMPLETE]`
- One result I initially interpreted differently and why: `[STUDENT TO COMPLETE]`
- What I checked manually in PyCharm: `[STUDENT TO COMPLETE]`
- Why I accept or reject the finance lexicon terms and assigned scores: `[STUDENT TO COMPLETE]`

These fields must not be completed by the AI because the rubric requires the student's own critical evaluation.
