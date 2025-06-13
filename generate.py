import fetchdata
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pdfrw import PdfReader, PdfWriter, PageMerge

font_path = "Noto_Sans_Devanagari/NotoSansDevanagari-VariableFont_wdth,wght.ttf"
pdfmetrics.registerFont(TTFont('Hindi', font_path))
date, hindidate, session, df = fetchdata.getdata('DEGREE INFORMATION SHEET.xlsx')

def write(c, string, y, x=None, fontname="Times-Bold", fontsize=15):
    c.setFont(fontname, fontsize)
    if x is None:
        text_width = c.stringWidth(string, fontname, fontsize)
        x = (letter[0] - text_width) / 2
    c.drawString(x, y, string)
    
def create_overlay(path, nameeng, namehind, btid, branch, cgpa):
    c = canvas.Canvas(path, pagesize=letter)
    write(c,nameeng,y=letter[1]-545.63-14.999999375000016+3)
    write(c,branch,y=letter[1]-545.63-14.999999375000016+43)
    c.save()

def create_file(srno, nameeng, namehind, btid, branch, cgpa):
    folder_path = os.path.join("certificate", branch)
    os.makedirs(folder_path, exist_ok=True)

    overlay_path = "temp_overlay.pdf"
    output_path = os.path.join(folder_path, f"{btid}.pdf")

    create_overlay(overlay_path, nameeng, namehind, btid, branch, cgpa)

    template_pdf = PdfReader("data/template.pdf")
    overlay_pdf = PdfReader(overlay_path)

    for page, overlay in zip(template_pdf.pages, overlay_pdf.pages):
        merger = PageMerge(page)
        merger.add(overlay).render()

    PdfWriter(output_path, trailer=template_pdf).write()

for index, row in df.iterrows():
    create_file(row['Sr. No.'], row['Name in English'], row['Name in Hindi'], row['Enrollment No.'], row['Branch'], row['CGPA'])