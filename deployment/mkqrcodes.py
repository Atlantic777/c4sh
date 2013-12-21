import pyqrcode
import uuid
import Image

for i in xrange(10,99):
	qr = pyqrcode.MakeQRImage(str(uuid.uuid4()), 3)
	qr = qr.resize((100,100), Image.ANTIALIAS)
	qr.save("qrcode0%d.png" % i, "PNG")
