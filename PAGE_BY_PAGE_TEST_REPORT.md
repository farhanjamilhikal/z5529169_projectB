SignalScope page-by-page verification report

Date: 2026-08-15

Local app launch

- Command path: `C:\Users\Farhanjamilhikal\Documents\GitHub\.venv\Scripts\python.exe -m streamlit run streamlit_app.py --server.headless true --server.port 8506`
- Local URL: `http://localhost:8506`
- Status: launched successfully

Automated validation completed

- Streamlit smoke and interface tests: passed
- Full pytest suite: passed
- Ruff: passed
- Hand-in checker: passed with only a removable `__pycache__` warning

Page checks

1. Overview
   - Opened in Streamlit test runner: yes
   - Opened in local browser: yes
   - Key checks: SignalScope title, academic-prototype banner, selected-fund control, verified performance metrics, growth-of-$1 chart, risk-return chart
   - Screenshot: `results/app/overview-desktop-visible.png`

2. Compare Funds
   - Opened in Streamlit test runner: yes
   - Opened in local browser: yes
   - Key checks: family filter, method filter, fund multiselect, verified comparison table, growth chart, drawdown chart, risk-return chart
   - Screenshot: `results/app/compare-funds-desktop-visible.png`

3. Fund Fact Sheet
   - Opened in Streamlit test runner: yes
   - Opened in local browser: yes
   - Key checks: verified fact-sheet metrics, holdings table, concentration summary, interpretation and limitation panels
   - Screenshot: `results/app/fund-fact-sheet-desktop-visible.png`

4. Holdings & Allocation
   - Opened in Streamlit test runner: yes
   - Opened in local browser: yes
   - Key checks: holdings chart, asset-family exposure, top-five concentration, allocation builder, duplicated-exposure warning
   - Screenshot: `results/app/holdings-allocation-desktop-visible.png`

5. News Sentiment
   - Opened in Streamlit test runner: yes
   - Opened in local browser: yes
   - Key checks: sentiment definitions, VADER and finance-lexicon explanation, validation metrics, sector coverage table, lag and limitations disclosure
   - Screenshot: `results/app/news-sentiment-desktop-visible.png`

6. Movie-to-Market Lab
   - Opened in Streamlit test runner: yes
   - Opened in local browser: yes
   - Key checks: exact page title, secondary-research badge, film selector, event-stage selector, event metrics, exposure register, evidence table, IMDb disclosure, descriptive-association limitation
   - Screenshot: `results/app/movie-to-market-lab-desktop-visible.png`

7. Methodology & Limitations
   - Opened in Streamlit test runner: yes
   - Opened in local browser: yes
   - Key checks: 2020-2023 course boundary, universe definitions, rebalancing and cost assumptions, sentiment lag, prototype-vs-production limitation set, data-licence and legal disclosures
   - Screenshot: `results/app/methodology-limitations-desktop-visible.png`

Responsive evidence

- Desktop-width activated reference capture: `results/app/overview-activated.png`
- Additional responsive probe captures saved for debugging:
  - `results/app/overview-tablet-1024.png`
  - `results/app/compare-funds-tablet-1024.png`
  - `results/app/overview-mobile-390.png`
  - `results/app/compare-funds-mobile-390.png`
  - `results/app/movie-to-market-lab-mobile-390.png`

Notes

- The desktop visible captures are usable QA evidence.
- Headless Edge screenshots produced Streamlit loading skeletons rather than rendered content, so those files were not used as the primary evidence set.
- The responsive probe captures are retained as supporting artefacts only because the host window manager did not isolate the mobile-width browser window as cleanly as the desktop-width captures.
