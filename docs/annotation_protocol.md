# SignalScope finance-headline annotation protocol

Purpose:
Create an independent labelled holdout for evaluating finance-headline sentiment in SignalScope.

Date frozen:
15 August 2026

Unit of labelling:
One headline.

Classes:
- Positive
- Neutral
- Negative

Task:
Label the likely immediate financial tone of the headline for the referenced company or asset, not whether the writing sounds emotional.

Definitions

Positive:
The headline signals information that would usually be interpreted as favourable for the company, such as stronger earnings, upgrades, successful launches, raised guidance, regulatory approval, improved margins, or beneficial deals.

Neutral:
The headline is descriptive, mixed, ambiguous, purely factual, backward-looking without clear directional implication, or contains offsetting positive and negative information.

Negative:
The headline signals information that would usually be interpreted as unfavourable for the company, such as earnings misses, downgrades, fraud, lawsuits, losses, falling demand, guidance cuts, regulatory penalties, distress, or bankruptcy risk.

Rules

1. Label only from the headline text shown.
2. Do not use model outputs before labelling.
3. Do not discuss labels with the other reviewer during first-pass labelling.
4. If a headline is unclear, assign Neutral rather than guessing direction.
5. If a headline contains both good and bad news with no dominant direction, assign Neutral.
6. Ignore your personal market view. Label the headline's likely financial tone.
7. Do not relabel after seeing performance metrics unless a new frozen round is created.

Examples

Positive:
- Company raises full-year profit guidance
- Broker upgrades stock after strong sales growth

Neutral:
- Company announces investor day next month
- Firm completes previously announced acquisition

Negative:
- Company misses earnings expectations
- Regulator fines firm over disclosure failures

Review process

Stage 1:
Two reviewers label independently.

Stage 2:
Measure agreement using Cohen's kappa.

Stage 3:
Resolve disagreements through adjudication and record the final label.

Required outputs
- reviewer_1_label
- reviewer_2_label
- final_label
- disagreement_flag
- adjudication_note
