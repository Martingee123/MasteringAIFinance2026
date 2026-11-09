COSTCO WHOLESALE CORPORATION (COST); annual: 0000909832-26-000093 https://www.sec.gov/Archives/edgar/data/909832/000090983226000093/cost-20260830.htm; quarterly: 0000909832-26-000051 https://www.sec.gov/Archives/edgar/data/909832/000090983226000051/cost-20260510.htm; earnings: 0000909832-26-000084 https://www.sec.gov/Archives/edgar/data/909832/000090983226000084/costex9918-k92426.htm
fallback
Run time (UTC): 2026-10-29T17:56:51.326986+00:00

# COST equity research report

Prepared by OpenAI Codex from the saved SEC filings and Python arithmetic. This is a newly prepared fallback report, not a successful four-role API run. Student verification and partner marks are not asserted. It is the Costco training case; KO remains the partner-selected submission company.

## Overview

Costco operates membership warehouses and e-commerce businesses. Its model combines low prices, a limited merchandise selection, high sales volumes, and rapid inventory turnover. The annual report explains that the membership model and operating efficiencies support low pricing. [annual.txt L177–L187.]

This analysis uses the fiscal year ended August 30, 2026, and the fourth quarter's comparable 16-week columns in the September 24, 2026 earnings release. The identified 10-Q is an earlier interim filing and is not substituted for the fourth-quarter release. [filings.json; earnings.txt L8–L9 and L55–L67.]

## Market Positioning and Growth Outlook

The membership model and merchandise value proposition are central to Costco's competitive position. Its filing also identifies expansion constraints, competition for locations, potential cannibalization, and the risk that new warehouses or online operations may not become profitable. These conditions mean that expansion does not ensure profitable growth. [annual.txt L180–L187 and L351–L357.]

The release reports $0.15 per diluted share of benefit from tariff refunds, after partial reinvestment in increased member values. This benefit is already inside the reported quarterly GAAP EPS; adding it again would double count it. The report uses the reported GAAP EPS rather than constructing adjusted EPS. [earnings.txt L44.]

## Valuation Insights

All dollar figures below are USD millions except per-share amounts. Total revenue includes membership fees. ROAE uses average beginning- and end-year equity. Debt/equity includes the current portion of long-term debt. Free cash flow is operating cash minus additions to property and equipment, following the course definition.

| # | Core claim | Figure | Arithmetic / definition | Source |
|---|---|---|---|---|
| 1 | Annual total revenue | $303,154 million | 297,247 net sales + 5,907 membership fees = 303,154 | annual.txt L1153–L1167 |
| 2 | Annual revenue growth | 10.14% | (303,154 / 275,235 − 1) × 100 = 10.1436953876% | annual.txt L1164–L1167 |
| 3 | Operating income and margin | $11,685 million; 3.85% | 11,685 / 303,154 × 100 = 3.8544766027% | annual.txt L1177–L1180 and L1164–L1167 |
| 4 | Net income attributable to Costco | $9,226 million | Net income: 9,226 | annual.txt L1204–L1210; NetIncomeLoss, FY 2026 |
| 5 | Annual GAAP diluted EPS | $20.76 | Diluted net income per common share: 20.76 | annual.txt L1219–L1225 |
| 6 | Return on average equity | 28.40% | 9,226 / ((35,803 + 29,164) / 2) × 100 = 28.4021118414% | annual.txt L1204–L1210 and L1386–L1388 |
| 7 | Long-term debt including current portion / equity | 0.1721× | (3,914 + 2,248) / 35,803 = 0.1721084825× | annual.txt L1331–L1333, L1341–L1343, L1386–L1388 |
| 8 | Free cash flow | $9,382 million | 15,817 operating cash − 6,435 capital expenditures = 9,382 | annual.txt L1703–L1714 |
| 9 | Latest quarter total revenue | $95,723 million | 93,873 net sales + 1,850 membership fees = 95,723 | earnings.txt L55–L85; 16 weeks ended August 30, 2026 |
| 10 | Quarter total revenue growth | 11.10% | (95,723 / 86,156 − 1) × 100 = 11.1042759645% | earnings.txt L55–L85; comparable 16-week columns |
| 11 | Quarter GAAP diluted EPS | $6.75 | Diluted net income per common share: 6.75 | earnings.txt L144–L152; also L44 |

Annual GAAP operating margins below use operating income / total consolidated revenue. Costco and BJ's denominators include membership income. Walmart uses Total revenues; Target labels its consolidated revenue Net sales. Different product mixes and fiscal dates limit the economic comparison. BJ's source statements are in thousands; its amounts have been converted to millions here.

| Company | Fiscal year end | Revenue (USD millions) | Operating income (USD millions) | Margin | Filing accession |
|---|---|---:|---:|---:|---|
| COST | 2026-08-30 | 303,154 | 11,685 | 3.85% | 0000909832-26-000093 |
| WMT | 2026-01-31 | 713,163.000 | 29,825.000 | 4.18% | 0000104169-26-000055 |
| TGT | 2026-01-31 | 104,780.000 | 5,117.000 | 4.88% | 0000027419-26-000016 |
| BJ | 2026-01-31 | 21,457.274 | 816.604 | 3.81% | 0001531152-26-000007 |

Peer statement evidence: WMT-annual.txt L2074–L2090; TGT-annual.txt L1934–L1961; BJ-annual.txt L1424–L1460. The respective revenue and operating-income XBRL facts and periods are also saved in peers.json.

P/E is missing because no dated closing price was supplied. Annual EPS is available, but a price-based valuation conclusion, price target, and estimated upside are not supported by this evidence. The desk's P/E convention is supplied price / annual GAAP diluted EPS, not a claim about a separate trailing-four-quarter EPS.

## Future Developments and Strategic Recommendations

Monitor membership retention, warehouse expansion economics, labor and merchandise costs, and the persistence of operating cash flow. The filing describes risks to membership loyalty and execution of expansion plans; these are risks rather than predictions of loss. [annual.txt L351–L358.]

Keep net sales and total revenue separate in future comparisons. The quarterly release's net-sales growth headline uses net sales; this report's core quarterly growth uses total revenue from the two comparable statement columns. Do not use an adjusted comparable-sales percentage as a substitute for total-revenue growth.

## Investment Recommendation

**Hold — provisional classroom judgment.** The deciding number is annual total-revenue growth of 10.14%, supported by the current and prior annual statement columns. Positive growth and cash generation support further monitoring. The missing share price prevents a supported price-based Buy or Sell, and execution and cost risks remain. [Core claims 2 and 8; annual.txt L351–L358.]

This is a provisional judgment, not a finding that the shares are fairly valued. No return forecast is asserted.

---
This is a learning exercise, not financial advice.
AI assistance: OpenAI Codex; Python arithmetic and SEC data reader.
AI source review only. No student or partner verification is claimed.
