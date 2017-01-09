#!/usr/bin/env python
#Concatenate PDFS in a directory

from PyPDF2 import PdfFileMerger

import os
cwd = os.getcwd()

files = os.listdir(cwd)

pdfs = [i for i in files if i.endswith('.pdf') and i !='concatenated.pdf']


merger = PdfFileMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("concatenated.pdf")
