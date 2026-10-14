# Finance statement tracker

Feed bank and credit-card statements (CSV or PDF) into one Excel workbook that
keeps every transaction in one place and rebuilds monthly, category and account
summaries each time you add a statement.

## What's here

| Path | What it is |
| --- | --- |
| `ingest.py` | The script that reads statements and updates the tracker |
| `template/finance_tracker_template.xlsx` | An empty tracker with all tabs set up |
| `categories.csv` | Starter keyword → category rules, copied into a new tracker |
| `samples/` | Example statements (checking CSV, card CSV, card PDF) to try it on |
| `tests/` | Unit tests |

## One-time setup

```bash
cd finance_tracker
python3 -m pip install -r requirements.txt     # openpyxl, pdfplumber
python3 ingest.py --init                       # creates tracker.xlsx here
```

You can instead copy `template/finance_tracker_template.xlsx` wherever you like
and point the script at it with `--tracker path/to/file.xlsx`. `tracker.xlsx`
is git-ignored so your real numbers don't get committed.

## Feeding in a new statement

1. Download the statement from your bank. **Prefer the CSV export** (often
   labelled "Download transactions" or "Export to spreadsheet"); PDF works, but
   CSV is more reliable.
2. Close the tracker in Excel if it's open.
3. Run the script, naming the account the statement belongs to:

   ```bash
   python3 ingest.py ~/Downloads/chase_sep_2026.csv --account "Chase Checking"
   python3 ingest.py ~/Downloads/amex_statement.pdf --account "Amex" --flip-sign
   ```

   Several files for the same account can go in one run:
   `python3 ingest.py ~/Downloads/chase_*.csv --account "Chase Checking"`.
4. Open `tracker.xlsx`. Check the **Uncategorized** row on *By Category*, then
   fix those rows on *Transactions* or add a rule (see below).

Use the same `--account` name every time for a given account; the summaries
group by that exact text.

Not sure a file will parse correctly? Add `--dry-run` to print what was
recognized without touching the tracker.

### Signs: money in is positive, money out is negative

Bank account exports usually already follow this. Most **credit-card**
statements show purchases as positive and payments as negative, so add
`--flip-sign` for those. A `--dry-run` makes it obvious which way a file goes:
groceries should come out negative.

### Re-importing is safe

Each transaction gets an ID from its account, date, description and amount, so
importing the same file twice, or two downloads with overlapping dates, only adds
the rows that are new. Two genuinely identical charges on the same day in one
statement (two coffees, say) are both kept.

## The tabs

| Tab | Contents |
| --- | --- |
| **Monthly Summary** | Income, spending, net and transaction count per month, plus totals and a monthly average. Card payments and transfers between your own accounts are left out so they aren't counted twice (change `INTERNAL_CATEGORIES` in `ingest.py` to adjust). |
| **By Category** | Each category's total per month. |
| **By Account** | Per account: date range covered, money in, money out, net, count. |
| **Transactions** | Every transaction, sorted by date. Edit *Category* and *Notes* freely. |
| **Imports** | A log of each file imported: rows found, added, and skipped as duplicates. |
| **Categories** | Your keyword rules. |

The summary tabs are Excel formulas over *Transactions*, so if you fix a
category or amount by hand the summaries update straight away. The script
rebuilds them on each run to pick up new months and categories, so don't put
your own notes on those three tabs. Don't add or reorder columns on
*Transactions*; use the *Notes* column instead.

## Categories

When a transaction is added it gets the category of the first rule on the
*Categories* tab whose keyword appears in the description (case-insensitive,
matched from the start of a word, so `fee` doesn't match "COFFEE"). Rules are
checked top to bottom, so put specific ones (`uber eats`) above general ones
(`uber`).

- To change rules, edit the *Categories* tab in the workbook.
  `categories.csv` is only the starting set for a brand-new tracker.
- A category you type yourself on *Transactions* is never overwritten.
- After adding rules, run `python3 ingest.py --recategorize` to apply them to
  rows that are still *Uncategorized*.

## Options

| Option | Use it when |
| --- | --- |
| `--account NAME` | Always, when importing. |
| `--tracker PATH` | Your tracker isn't `finance_tracker/tracker.xlsx`. |
| `--flip-sign` | Purchases show up positive (most credit cards). |
| `--day-first` | Dates are DD/MM/YYYY (UK, EU, AU and others). |
| `--date-format FMT` | CSV dates are in an unusual format, e.g. `--date-format %d.%m.%Y`. |
| `--year YYYY` | A PDF prints dates without a year and the guess is wrong. |
| `--dry-run` | You want to preview what will be imported. |
| `--recategorize` | You added rules and want to apply them to uncategorized rows. |
| `--init` | Create a new, empty tracker. |

## When a statement doesn't parse

**CSV.** The script looks for a header row (within the first 30 lines) with a
date column, a description column, and either an amount column or separate
debit/credit columns. It recognizes common names such as *Date*, *Posting
Date*, *Transaction Date*, *Description*, *Payee*, *Merchant*, *Amount*,
*Debit*, *Credit*, *Withdrawals*, *Deposits*. If your bank uses another name,
add it to `HEADER_ALIASES` near the top of `ingest.py`.

**PDF.** PDFs have no columns, only text, so the script reads lines that start
with a date and end with an amount (optionally followed by a running balance).
That covers most card statements and many bank statements, but:

- Scanned (image-only) PDFs have no text. Use the CSV export, or OCR the PDF first.
- Statements that put withdrawals and deposits in separate columns without a
  minus sign come out all positive. Use the CSV export for those accounts.
- Transactions whose description wraps onto a second line keep only the first line.
- Dates without a year take the year of the statement's latest printed date,
  with December rows on a January statement assigned to the prior year.
  Override with `--year`.

Always run a PDF with `--dry-run` the first time you use a new bank's format.

## Running the tests

```bash
python3 -m unittest discover -s finance_tracker/tests
```

`samples/make_sample_pdf.py` regenerates the sample PDF statement (needs `reportlab`).
