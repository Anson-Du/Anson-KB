import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pdfplumber
from pypdf import PdfReader

path = r"C:\Users\Lenovo\AppData\Local\Temp\codebuddy-dropped-files\4e2a9033-ca58-4e92-a1a0-ac88578c5b92\永昌國際控股(香港)有限公司-杜岩松-20260914.pdf"

out = []
with pdfplumber.open(path) as pdf:
    out.append("PAGES: %d" % len(pdf.pages))
    for i, page in enumerate(pdf.pages):
        txt = page.extract_text() or ""
        out.append("\n===== PAGE %d =====" % (i+1))
        out.append(txt)
        # tables
        tables = page.extract_tables()
        for j, t in enumerate(tables):
            out.append("--- TABLE %d on page %d ---" % (j+1, i+1))
            for row in t:
                out.append(" | ".join(["" if c is None else str(c).replace("\n"," ") for c in row]))

# AcroForm fields
reader = PdfReader(path)
fields = reader.get_fields()
out.append("\n===== FORM FIELDS =====")
if fields:
    for k, v in fields.items():
        out.append("%s => %s" % (k, v.get('/V')))
else:
    out.append("(none)")

with open(r"e:\11-其他\codebuddy\pdf_full.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("written, total chars:", sum(len(x) for x in out))
