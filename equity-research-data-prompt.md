Build the data part of an equity research desk in Python. Use Section 3.1 of Francis & Zhang (2026) as the reference. The model roles will come later.

Read `SEC_USER_AGENT` from the `.env` file in this folder. Send this value in the `User-Agent` header of every HTTP request.

The program must accept:

- A ticker as a required argument.
- `--peers` as an optional list of tickers.
- `--price` as an optional number.
- `--step` as an optional number that runs only the selected step.

Do not hard-code a company name or ticker.

Implement these seven steps. Print each step’s number and name when it starts.

1. **Find the CIK.** Resolve the input ticker to its CIK. Use the SEC file `company_tickers.json`.

2. **Select the filings.** Get the company’s filings from the EDGAR submissions API. Select the latest 10-K, the latest 10-Q, and the latest 8-K whose document reports Item 2.02, the earnings release. For each selected filing, print its accession number. Also print the “Accepted” time shown on its EDGAR index page.

3. **Download and save the documents.** Download the selected 10-K and 10-Q. For the selected 8-K, download Exhibit 99.1, which contains the earnings release. Convert each document to plain text. Save the texts in a folder whose name includes the company name and the date and time of the run.

4. **Get the annual financial facts.** Fetch the company’s XBRL company facts. For the latest fiscal year, print:
   - Total revenue.
   - Operating income.
   - Net income.
   - Diluted EPS.
   - Stockholders’ equity.
   - Long-term debt.
   - The current portion of long-term debt.
   - Cash from operations.
   - Additions to property and equipment.

   For each concept, compare its candidate tags. Select the tag whose latest available fiscal year is the newest. Use revenue to set the fiscal year for all concepts. Read every concept for that same fiscal year. Show the prior-year value beside each current-year value. Include the tag, period end, and source filing for each value.

5. **Calculate the financial measures.** Use Python code for all arithmetic. Print each result and the arithmetic used to calculate it:
   - Revenue growth.
   - Operating margin.
   - Return on average equity.
   - Debt to equity, with the current portion of long-term debt included in debt.
   - Free cash flow, calculated as cash from operations minus additions to property and equipment.
   - P/E, using the price supplied through `--price`.

6. **Find the quarterly results.** Read the saved earnings release text. Print the lines that state the quarter’s total revenue and diluted EPS.

7. **Compare peers.** For each ticker supplied through `--peers`, get the same financial facts. Calculate its operating margin. Use the same operating margin definition for the company and all peers.

Save the financial facts in the same folder as the document texts.

When the work is complete, give me the exact commands to:

- Install all required packages.
- Run the program with a ticker, peers, and a price.
