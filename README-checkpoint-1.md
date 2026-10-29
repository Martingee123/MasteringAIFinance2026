# Checkpoint 1 — equity research desk

Partner-selected company: **KO**. The saved KO release was filed October 27, 2026. Checkpoint 1 is due October 29, 2026, at 11:59 PM Eastern.

## Current status

- Seven data steps executed on KO with PEP and KDP, and on COST with WMT, TGT, and BJ.
- KO fallback draft: `runs/KO_20261029T171451Z/report-fallback.md`.
- OpenAI four-role workflow is implemented but has **not been executed**: the local API key is a placeholder.
- Student audit and partner marks are pending. AI must not fill those marks.
- A dated exchange or LSEG close is not supplied. P/E is missing rather than invented.
- Costco fallback report: `runs/COST_20261029T171538Z/report-fallback.md`. Its completed AI audit is `audits/COST-audit.md`; this is not a human sign-off.

The course explicitly accepts a fallback report for Checkpoint 1. This draft needs your source review and the required human disclosure before final submission. It is labeled fallback on its second line. It does not claim to be an API-generated four-role run.

## Setup and run

Use Python 3.11 or later. In this workspace `.venv` already has Python 3.11 and the dependencies.

```sh
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` only if `.env` does not already exist. Set your SEC name/email and OpenAI developer key locally. Never upload `.env`.

```sh
.venv/bin/python desk.py KO --peers PEP,KDP --data-only
.venv/bin/python desk.py COST --peers WMT,TGT,BJ --data-only
.venv/bin/python desk.py WMT --data-only
```

Generate the API report from saved data after configuring your key:

```sh
.venv/bin/python desk.py KO --resume runs/KO_20261029T171451Z
.venv/bin/python desk.py COST --resume runs/COST_20261029T171538Z
```

For a new run that includes valuation, append `--price NUMBER --price-date YYYY-MM-DD --price-source URL`. Use the last close before the release from the exchange or LSEG. The program calculates price / annual GAAP diluted EPS; it does not call this a current trailing-four-quarter P/E. A resume uses the saved price and source, so rerun the data steps when changing price.

`--step 1` through `--step 7` stops after the selected step. Earlier steps run as prerequisites. Each run saves its own source documents, numbered text, filings metadata, facts, ratios and peer facts. Cached SEC responses are local and excluded from Git. For a genuinely fresh retrieval, clear `.cache` first.

## Design and limits

The ticker is an argument. The code contains no company-specific branch. It selects the latest 10-K, 10-Q and Item 2.02 8-K, reads the filing index's acceptance time, and downloads Exhibit 99.1. Peer analysis needs only each peer's latest 10-K. A missing Exhibit 99.1 raises an error for inspection.

Annual XBRL facts must match the selected 10-K's fiscal year end. Annual durations must be 330–380 days. The prior year comes from the same filing when available. Candidate tags are selected only when they hold the target period. Review definitions in the filing: tags do not guarantee that two companies use the same revenue definition. Missing values stay missing.

Python calculates the ratios. The Financial Analyst can request additional calculations through a restricted arithmetic tool. The Research Analyst receives filing text. The Financial Analyst receives facts, ratios, peers and the release. The Investment Advisor receives only the two analyses. The Manager compiles the five sections and permits one section repair. This section check does not prove numerical or factual consistency; human review is still required. Each role's JSON input and Markdown output are saved when the API runs.

The release reader prints candidate source lines around revenue and diluted EPS. It does not claim that every printed number is a quarterly GAAP figure. A model or person must identify the correct table, period and definition.

## Validation

```sh
.venv/bin/python -m unittest -v test_desk.py
```

Three tests cover arithmetic-only evaluation, missing debt not being treated as zero, and selecting a new revenue tag for the latest annual period while excluding quarterly facts. Live SEC data runs also completed for KO and COST with their peers. These checks are software verification, not the student's report audit.

## Finish and submit

1. Open the KO report and its saved filings. Complete `audits/KO-audit.md` yourself. Add rows for every additional financial number.
2. Have your partner check two core claims and write both marks at the top of the report.
3. After your source review, replace the pending-verification footer with the course's required three-line disclosure. Do not claim verification before you do it.
4. Commit and push the reviewed changes. Submit the full GitHub **commit URL** in Brightspace → Checkpoint 1, not a branch URL.
5. For the lab training case, review the saved COST fallback report and its AI audit in `audits/COST-audit.md`. Human verification remains separate. Audit all eleven KO claims before Session 4.

Course requirements: https://cinderzhang.github.io/FIN67110-Fall2026/week-02/lab-03-make-it-yours.html

This is a learning exercise, not financial advice.
AI assistance: OpenAI Codex.
Human source verification and judgments are pending; no student sign-off is claimed.
