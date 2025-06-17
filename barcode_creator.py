import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from barcode import Code128
from barcode.writer import ImageWriter
from reportlab.lib.utils import ImageReader

def draw_barcode_on_canvas(c, number_str, x, y, width=190, height=47):
    buffer = io.BytesIO()
    Code128(number_str, writer=ImageWriter()).write(buffer)
    buffer.seek(0)
    barcode_image = ImageReader(buffer)
    c.drawImage(barcode_image, x, y, width=width, height=height)