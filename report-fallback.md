COCA COLA CO (KO); annual: 0001628280-26-010047 https://www.sec.gov/Archives/edgar/data/21344/000162828026010047/ko-20251231.htm; quarterly: 0001628280-26-067844 https://www.sec.gov/Archives/edgar/data/21344/000162828026067844/ko-20261002.htm; earnings: 0001628280-26-067403 https://www.sec.gov/Archives/edgar/data/21344/000162828026067403/a2026q3earningsreleaseex-9.htm
fallback
Run time (UTC): 2026-10-29T17:16:26.219185+00:00

Partner check 1: PENDING — partner must record the claim, filing line, and mark here.
Partner check 2: PENDING — partner must record the claim, filing line, and mark here.

# KO equity research report

Status: AI draft for the student's source review. This fallback was prepared by OpenAI Codex from the saved filings, XBRL facts, and Python calculator outputs. It is not an executed four-role API run. The API workflow is provided in desk.py. Source line numbers refer to the saved numbered text files. The student and partner have not supplied audit marks.

## Overview

Coca-Cola sells branded beverages through independent bottling partners, distributors, wholesalers, retailers, and its own operations. Its product groups include sparkling drinks, water, sports drinks, coffee, tea, juice, dairy, and plant-based beverages. The distribution model and brand portfolio support broad market access. This is a description of the business, not proof of future investment returns. [10-K, annual.txt L237–L238.]

The latest annual period ends December 31, 2025. The latest quarterly filing covers the period ended October 2, 2026. The latest earnings release was filed October 27, 2026. The report keeps the annual and quarterly periods separate. [filings.json; each filing's index page.]

## Market Positioning and Growth Outlook

The earnings release reports value-share gains in nonalcoholic ready-to-drink beverages. It also reports growth in unit case volume, with strength in India, China, Mexico, and Brazil. Those are management's reported observations. [earnings.txt L31–L32 and L164–L168.]

North American unit case volume was flat. This limits the claim that growth is uniform across regions. The release attributes part of concentrate-sales performance to shipment timing. Shipment timing can weaken the link between reported revenue growth and underlying consumption. [earnings.txt L176 and L198–L204.]

The following annual comparison uses operating income divided by each company's total revenue. Each peer is read from its own latest 10-K. Differences in business mix and fiscal year ends limit comparability. In particular, this comparison does not establish that differences in margins arise only from competitive strength.

| Company | Fiscal year end | Total revenue (USD millions) | Operating income (USD millions) | Operating margin | Source and arithmetic |
|---|---|---:|---:|---:|---|
| KO | 2025-12-31 | 47,941 | 13,762 | 28.71% | 0001628280-26-010047; Revenues and OperatingIncomeLoss; 13762000000 / 47941000000 |
| PEP | 2025-12-27 | 93,925 | 11,498 | 12.24% | 0000077476-26-000007; Revenues and OperatingIncomeLoss; 11498000000 / 93925000000 |
| KDP | 2025-12-31 | 16,603 | 3,575 | 21.53% | 0001418135-26-000016; RevenueFromContractWithCustomerExcludingAssessedTax and OperatingIncomeLoss; 3575000000 / 16603000000 |

## Valuation Insights

All dollar inputs in the next table are USD millions, except EPS. The source is KO's 2025 10-K, accession 0001628280-26-010047. The current-year period is January 1 to December 31, 2025. Balance-sheet amounts are as of December 31. The growth and average-equity calculations use the prior-year figures from the same filing. The raw XBRL values in facts.json are in USD, not millions.

| Core claim | Report figure | Definition, arithmetic, and source |
|---|---:|---|
| 1. Annual total revenue | $47,941 million | Revenues; annual.txt L1670–L1674. The statement labels this Net Operating Revenues. |
| 2. Annual revenue growth | 1.87% | (47,941 / 47,061 − 1) × 100; Revenues for 2025 and 2024; annual.txt L1670–L1674. |
| 3. Operating income and margin | $13,762 million; 28.71% | 13,762 / 47,941 × 100; OperatingIncomeLoss / Revenues; annual.txt L1693–L1695 and L1670–L1674. |
| 4. Net income attributable to KO | $13,107 million | NetIncomeLoss; annual.txt L1731–L1735. This excludes noncontrolling interests. |
| 5. Annual GAAP diluted EPS | $3.04 | EarningsPerShareDiluted; annual.txt L1746–L1751. |
| 6. Return on average equity | 45.97% | 13,107 / ((32,169 + 24,856) / 2) × 100; NetIncomeLoss and StockholdersEquity; annual.txt L1731–L1735 and L1962–L1964. Equity excludes noncontrolling interests. |
| 7. Long-term debt including current portion / equity | 1.3659× | (42,119 + 1,822) / 32,169; LongTermDebtAndCapitalLeaseObligations, LongTermDebtAndCapitalLeaseObligationsCurrent, and StockholdersEquity; annual.txt L1907–L1909, L1919–L1921, L1962–L1964. This follows the course definition and excludes short-term loans and notes payable. |
| 8. Free cash flow | $5,296 million | 7,408 − 2,112; NetCashProvidedByUsedInOperatingActivities − PaymentsToAcquirePropertyPlantAndEquipment; annual.txt L2058–L2060 and L2091–L2096. This is the course calculation, not a substitute for a differently adjusted company measure. |
| 9. Latest quarter total revenue | $13,380 million | Three months ended October 2, 2026; earnings.txt L459–L473. The statement labels it Net Operating Revenues. |
| 10. Quarter revenue growth | 7.43% | (13,380 / 12,455 − 1) × 100, computed in Python from the release’s quarterly columns; earnings.txt L459–L473. This differs from the release’s rounded whole-percent headline. |
| 11. Quarter GAAP diluted EPS | $0.93 | Three months ended October 2, 2026; earnings.txt L539–L544 and L28–L29. The $0.91 comparable EPS is non-GAAP and is not used as GAAP EPS. |

P/E is not stated because a dated closing price from the exchange or LSEG has not been supplied. The desk accepts that price, its date, and its source. It computes P/E as price divided by the annual GAAP diluted EPS above. This annual EPS is not a trailing-four-quarter EPS as of the earnings release. A share-price target and an estimate of upside are also not supported by the supplied evidence.

## Future Developments and Strategic Recommendations

Management raised its full-year outlook. It expects at least 5% organic revenue growth and at least 11% comparable EPS growth for 2026. Both are non-GAAP guidance measures, not realized GAAP results. [earnings.txt L344–L385.]

Monitor the pending sale of African bottling operations. Management's guidance assumes a closing in the fourth quarter, subject to regulatory approval. It does not say the transaction has already closed. Changes in portfolio scope can affect reported revenue independently of demand. [earnings.txt L432–L434.]

Tax litigation is another material uncertainty. Management says it intends to defend its position, while acknowledging that an adverse outcome could create significant additional liabilities. This report does not assume either a successful appeal or a loss. [annual.txt L1310.]

The next report should test whether volume growth persists, whether shipment timing reverses, and whether operating cash generation supports earnings. The peer margin comparison should remain on one definition and show the fiscal dates beside the figures.

## Investment Recommendation

**Hold — a provisional classroom judgment.** The deciding number is annual revenue growth of 1.87%. That is positive but modest on the period used in the annual financial analysis. The stronger recent quarter and management's raised guidance support continued monitoring. Shipment timing, litigation, and differences between GAAP and non-GAAP measures limit a simple growth narrative. [Core claim 2; quarterly evidence and outlook cited above.]

This judgment is not a finding that the stock is fairly valued. A dated price has not been supplied, so this report cannot establish the valuation needed to support a price-based Buy or Sell. No benchmark return, forecast return, or price target is asserted.

---
This is a learning exercise, not financial advice.
AI assistance: OpenAI Codex; Python data reader and calculator.
Human verification pending. After reviewing the sources yourself, replace this line with: “I verified the sources myself; the judgments are mine. Any remaining errors are my own.”
