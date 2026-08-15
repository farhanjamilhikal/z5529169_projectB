# UI Audit — active Streamlit application before SignalScope rebuild

Date audited: 2026-08-15

Entry point audited:

- [streamlit_app.py](/C:/Users/Farhanjamilhikal/Documents/GitHub/fins2026/projectBfinale/z5529169_projectB/streamlit_app.py)
- [app.py](/C:/Users/Farhanjamilhikal/Documents/GitHub/fins2026/projectBfinale/z5529169_projectB/app.py)

## Active identity located

The active application is the NovaFinance mock dashboard. Verified strings in the
entrypoint code included:

- `NovaFinance`
- `Spider-Man x Barbie x premium fintech demo`
- `Total Portfolio Value`
- `Tactile controls with toast confirmations`

## Current navigation inventory

Pages found in the active app:

1. Home
2. Portfolio
3. Markets
4. History
5. Settings

## Current interactive inventory

Current controls found in the active app:

- dark-mode toggle
- sidebar navigation radio
- Deposit button
- Withdraw button
- Transfer button
- asset selector
- history status filter
- history type filter
- history search field
- CSV export download
- settings toggles
- settings risk slider

## Current page-level findings

### Home

- Uses fabricated portfolio value and daily P&L from `generate_demo_data()`.
- Uses unsupported “quick actions” implying brokerage functionality.
- Uses mock allocation donut and mock asset cards.
- Uses unsupported “market pulse” and “hot” labelling.

### Portfolio

- Uses random synthetic prices and holdings.
- Uses unsupported candlestick chart disconnected from verified Project B outputs.
- Uses fabricated news snippets.

### Markets

- Uses unsupported watchlist, market indices and momentum-style labels.
- Contains invented live-market framing not backed by `results/`.

### History

- Uses mock transactions.
- Exports synthetic transaction records unrelated to the coursework product.

### Settings

- Contains presentation preferences only; no direct analytical issue, but page
  naming and information architecture are not aligned with the required product.

## Data alignment findings

- The active app does not load the verified `results/data/*.csv` and
  `results/tables/*.csv` as its primary source of truth.
- The main data provider is `generate_demo_data()`, which violates the required
  finale-only source hierarchy.
- Visible numbers are not traceable to the latest Project B finale outputs.

## Layout and UX findings

- Theme direction is useful: dark navy base, cyan and hot-pink accents, rounded
  cards and a premium visual tone can be retained.
- Information architecture is wrong for the academic analytics product.
- Page names reflect a brokerage-style demo rather than a research dashboard.
- Several controls imply unsupported transactional capability.
- Current banner discloses mock data; this confirms the app is not yet aligned
  with the verified analytical package.

## Initial conclusion

The active app is visually useful as a theme reference only. It requires a
complete in-place rebuild of content, navigation, data loading and disclosure
logic to become the required SignalScope application.
