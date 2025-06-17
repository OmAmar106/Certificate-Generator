# Certificate Generator for IIIT Nagpur

This project is developed to automate the process of generating degree certificates for students of IIIT Nagpur. It includes automatic insertion of QR codes and barcodes for verification, dynamic data placement, and PDF generation using Python.

## Functionalities

* Automatically generate degree certificates in PDF format.
* Add QR codes (for verification URLs) and barcodes (for roll numbers or certificate IDs).
* Supports custom fonts including Hindi (Noto Sans Devanagari) and English (Arial, Times).
* Uses ReportLab to create and manipulate PDFs.
* Supports bulk generation from structured data (like CSV).
## Technologies used

* Python
* Libraries: reportlab, qrcode, python-barcode, pillow, datetime, io

## Setup

- Add the template and the excel file to the data folder.
- Run 
    ~~~bash
    >> pip install requirements.txt
    >> python3 generate.py
    ~~~
- The Certificate will be generated as certificate/branch/rollno.pdf