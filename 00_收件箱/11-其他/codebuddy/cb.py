import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
from pypdf import PdfReader
f=PdfReader(r"e:\11-其他\codebuddy\policy.pdf").get_fields()
for k,v in f.items():
    if v.get('/FT')=='/Btn':
        print(k, v.get('/V'), v.get('/Rect'))
