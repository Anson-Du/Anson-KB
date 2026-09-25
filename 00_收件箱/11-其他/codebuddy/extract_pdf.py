import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pdfplumber

path = r"C:\Users\Lenovo\AppData\Local\Temp\codebuddy-dropped-files\4e2a9033-ca58-4e92-a1a0-ac88578c5b92\永昌國際控股(香港)有限公司-杜岩松-20260914.pdf"

with pdfplumber.open(path) as pdf:
    print("PAGES:", len(pdf.pages))
    for i, page in enumerate(pdf.pages):
        txt = page.extract_text() or ""
        print(f"\n===== PAGE {i+1} (len={len(txt)}) =====")
        print(txt)
