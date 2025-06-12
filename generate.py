from PIL import Image
import fetchdata

date,hindidate,session,df = fetchdata.getdata('DEGREE INFORMATION SHEET.xlsx')

def create_file(srno,nameeng,namehind,btid,branch,cgpa):
    print(srno,nameeng,namehind,btid,branch,cgpa,date,hindidate,session)

for index,row in df.iterrows():
    create_file(row['Sr. No.'],row['Name in English'],row['Name in Hindi'],row['Enrollment No.'],row['Branch'],row['CGPA'])