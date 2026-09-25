import pypdfium2 as pdfium
pdf = pdfium.PdfDocument(r"e:\11-其他\codebuddy\policy.pdf")
for i in range(len(pdf)):
    page = pdf[i]
    try:
        bmp = page.render(scale=2.0, draw_annots=True)
    except TypeError:
        bmp = page.render(scale=2.0)
    bmp.to_pil().save(r"e:\11-其他\codebuddy\f_%d.png" % (i+1))
print("ok")
