"""Generate samples/sample_card_statement.pdf, a fake credit-card statement for testing."""
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

OUT = Path(__file__).with_name("sample_card_statement.pdf")
LINES = [
    ("12/08", "12/09", "TRADER JOE'S #552", "54.21"),
    ("12/14", "12/15", "UNITED AIRLINES 0162", "412.60"),
    ("12/20", "12/21", "DOORDASH*THAI PALACE", "38.47"),
    ("12/28", "12/28", "PAYMENT THANK YOU", "-500.00"),
    ("01/02", "01/03", "SPOTIFY USA", "11.99"),
    ("01/03", "01/04", "SHELL OIL 5744", "47.15"),
]


def main() -> None:
    c = canvas.Canvas(str(OUT), pagesize=letter)
    y = 740
    for text in ["Example Bank Visa Signature", "Account ending in 9876",
                 "Statement Period: Dec 06, 2026 - Jan 05, 2027",
                 "New Balance: $1,064.42    Payment Due Date: Feb 01, 2027", "",
                 "Trans Date  Post Date  Description  Amount"]:
        c.drawString(60, y, text)
        y -= 18
    for trans, post, desc, amt in LINES:
        c.drawString(60, y, trans)
        c.drawString(130, y, post)
        c.drawString(200, y, desc)
        c.drawRightString(540, y, amt)
        y -= 16
    y -= 10
    c.drawString(60, y, "Total fees charged in 2026    $0.00")
    c.save()
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
