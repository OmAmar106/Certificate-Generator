import fetchdata
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pdfrw import PdfReader, PdfWriter, PageMerge
import unicodedata
import qrcode
import io
from PIL import Image
from reportlab.lib.utils import ImageReader
import barcode_creator

hindi_digits = {
    '0': '०',
    '1': '१',
    '2': '२',
    '3': '३',
    '4': '४',
    '5': '५',
    '6': '६',
    '7': '७',
    '8': '८',
    '9': '९',
    '.':'.'
}

font_path = "Noto_Sans_Devanagari/static/NotoSansDevanagari-SemiBold.ttf"
pdfmetrics.registerFont(TTFont('Hindi', font_path))
t = 'DEGREE INFORMATION SHEET.xlsx'
t = input("Enter File Name : ")
date, hindidate, session, df = fetchdata.getdata(t)

def get_day_suffix(day):
    if 11<=day<=13:
        return 'th'
    return {1:'st',2:'nd',3:'rd'}.get(day%10,'th')

def draw_superscript_date(c,date_obj,x,y):
    day = date_obj.day
    suffix = get_day_suffix(day)
    month = date_obj.strftime("%B")
    year = date_obj.year
    day_str = str(day)
    textobject = c.beginText()
    textobject.setTextOrigin(x, y)
    textobject.setFont("Times-Bold", 15)
    textobject.textOut(day_str)
    textobject.setFont("Times-Bold", 9)
    textobject.setRise(7)
    textobject.textOut(suffix)
    textobject.setRise(0)
    textobject.setFont("Times-Bold", 15)
    textobject.textOut(f" {month} {year}")
    c.drawText(textobject)
    return


def write(c, string, y, x=None, fontname="Times-Bold", fontsize=15):
    c.setFont(fontname, fontsize)
    if x is None:
        text_width = c.stringWidth(string, fontname, fontsize)
        x = (letter[0] - text_width) / 2
    c.drawString(x, y, string)
    return

session = session[-4:].strip()
# print(date,type(date))
def qr_code_text(name,btid,branch,cgpa,srno):
    text = f"""
    Degree Sl. No. : {srno} Name : {name} Enrollment No. : {btid} Branch : {branch} Passing Session : Spring Jan.-May {session} CGPA : {cgpa}
    """
    return text

def func(name):
    ans = []
    name = name.strip()
    for i in range(min(3,len(name))):
        if name[i]==' ' and ans:
            break
        ans.append(str(ord(name[i].lower())-ord('a')+1))
    # print(name,ans)
    return ''.join(ans)

def create_overlay(path, nameeng, namehind, btid, branch, cgpa,srno):
    c = canvas.Canvas(path, pagesize=letter)

    text = qr_code_text(nameeng,btid,branch,cgpa,srno)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=1,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    c.drawImage(ImageReader(buffer), x=500, y=710, width=48, height=48)

    bchname = 'संगणक विज्ञान एवं अभियांत्रिकी'
    bchname = input("Enter Branch Name in Hindi : ")
    draw_superscript_date(c,date,y=letter[1]-545.63-14.999999375000016-98.5,x=289)
    write(c,namehind,y=letter[1]-545.63-14.999999375000016+381,fontname='Hindi',fontsize=18)
    write(c,unicodedata.normalize('NFC',bchname),y=letter[1]-545.63-14.999999375000016+316,fontname='Hindi',fontsize=18)
    write(c,hindidate,y=letter[1]-545.63-14.999999375000016+346.8,x=388,fontname='Hindi',fontsize=18)
    write(c,nameeng,y=letter[1]-545.63-14.999999375000016+3)
    write(c,branch,y=letter[1]-545.63-14.999999375000016+43)
    write(c,str(cgpa),y=letter[1]-545.63-14.999999375000016-73.6,x=424)
    write(c,session,y=letter[1]-545.63-14.999999375000016-22.4,x=447.5)
    write(c,''.join(list(map(lambda x:hindi_digits[x],session))),y=letter[1]-545.63-14.999999375000016+255,x=339,fontname='Hindi',fontsize=18)
    write(c,''.join(list(map(lambda x:hindi_digits[x],str(cgpa)))),y=letter[1]-545.63-14.999999375000016+225,x=414,fontname='Hindi',fontsize=18)
    c.showPage()

    write(c,btid,y=letter[1]-545.63-14.999999375000016+330,x=458.5,fontname='Helvetica',fontsize=11)
    write(c,btid,y=letter[1]-545.63-14.999999375000016+330,x=458.6,fontname='Helvetica',fontsize=11)
    write(c,btid,y=letter[1]-545.63-14.999999375000016+330,x=458.7,fontname='Helvetica',fontsize=11)
    
    x = 148.5
    write(c,srno,y=letter[1]-545.63-14.999999375000016+330,x=x+0.5,fontname='Helvetica',fontsize=11)
    write(c,srno,y=letter[1]-545.63-14.999999375000016+330,x=x+0.6,fontname='Helvetica',fontsize=11)
    write(c,srno,y=letter[1]-545.63-14.999999375000016+330,x=x+0.7,fontname='Helvetica',fontsize=11)
    
    dt = str(date.day)+'/'+str(date.month)+'/'+str(date.year)
    write(c,dt,y=letter[1]-545.63-14.999999375000016+305,x=x+0.5,fontname='Helvetica',fontsize=11)
    write(c,dt,y=letter[1]-545.63-14.999999375000016+305,x=x+0.6,fontname='Helvetica',fontsize=11)
    write(c,dt,y=letter[1]-545.63-14.999999375000016+305,x=x+0.7,fontname='Helvetica',fontsize=11)
    
    barcode_creator.draw_barcode_on_canvas(c,func(nameeng),115,296)

    c.save()

def create_file(srno, nameeng, namehind, btid, branch, cgpa):
    folder_path = os.path.join("certificate", branch)
    os.makedirs(folder_path, exist_ok=True)

    overlay_path = "temp_overlay.pdf"
    output_path = os.path.join(folder_path, f"{btid}.pdf")

    create_overlay(overlay_path, nameeng, namehind, btid, branch, cgpa,srno)

    template_pdf = PdfReader("data/template.pdf")
    overlay_pdf = PdfReader(overlay_path)

    for page, overlay in zip(template_pdf.pages, overlay_pdf.pages):
        merger = PageMerge(page)
        merger.add(overlay).render()

    PdfWriter(output_path, trailer=template_pdf).write()

for index, row in df.iterrows():
    create_file(row['Sr. No.'], row['Name in English'], row['Name in Hindi'], row['Enrollment No.'], row['Branch'], row['CGPA'])