import qrcode

url = "https://elysia-plan-1f2ffd0a93a1.netlify.app"
output = r"C:\Users\Lenovo\.qoderworkcn\workspace\msg3usob6k94fhku\outputs\elysia-plan-qrcode.png"

qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
qr.add_data(url)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save(output)
print(f"QR code saved: {output}")
print(f"URL: {url}")
