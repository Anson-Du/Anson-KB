import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = r"C:\Users\Lenovo\AppData\Local\Temp\codebuddy-dropped-files\4e2a9033-ca58-4e92-a1a0-ac88578c5b92\永昌國際控股(香港)有限公司-杜岩松-20260914.pdf"

# 1) Render pages to PNG
renderer = None
try:
    import pypdfium2 as pdfium
    pdf = pdfium.PdfDocument(path)
    print("pypdfium2 pages:", len(pdf))
    for i in range(len(pdf)):
        page = pdf[i]
        bitmap = page.render(scale=2.0)
        pil = bitmap.to_pil()
        out = r"e:\11-其他\codebuddy\page_%d.png" % (i+1)
        pil.save(out)
        print("saved", out, pil.size)
    renderer = "pypdfium2"
except Exception as e:
    print("pypdfium2 failed:", repr(e))
    try:
        import fitz
        doc = fitz.open(path)
        for i, page in enumerate(doc):
            pix = page.get_pixmap(matrix=fitz.Matrix(2,2))
            out = r"e:\11-其他\codebuddy\page_%d.png" % (i+1)
            pix.save(out)
            print("saved", out, pix.width, pix.height)
        renderer = "fitz"
    except Exception as e2:
        print("fitz failed:", repr(e2))

# 2) Field rects per page
from pypdf import PdfReader
reader = PdfReader(path)
print("\n===== FIELD RECTS BY PAGE =====")
for pi, page in enumerate(reader.pages):
    annots = page.get("/Annots")
    if not annots:
        continue
    print("---- page", pi+1, "----")
    for a in annots:
        obj = a.get_object()
        if obj.get("/Subtype") != "/Widget":
            continue
        name = obj.get("/T")
        rect = obj.get("/Rect")
        ftype = obj.get("/FT")
        val = obj.get("/V")
        print("%s | type=%s | rect=%s | val=%s" % (name, ftype, rect, val))
