#!/usr/bin/env python
import pdfquery
from pyPdf import PdfFileWriter, PdfFileReader
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import sys


#Custom Libraries
from inv import *


def main():
	#1. Loads up the PDF and gets the number of pages
	if len(sys.argv) >= 2:
		pdf_name = sys.argv[1]
		print "About to open " + str(pdf_name)
	else:
		#pdf_name = "binder_combined copy.pdf"
		exit("Error: Please Input a PDF")

	pdf = pdfquery.PDFQuery(pdf_name)
	pdf_count = pdf.doc.catalog['Pages'].resolve()['Count']

	#2. Create Invoices Object, which A) holds an array of invoices
	# and B) holds
	invoices = Invoices()
	count = 0;

	for page in range(pdf_count):

		print "About to load " + str(page)
		try:
			pdf.load(page)
		except:
			print "ERROR: Couldn't load page " + str(page)
			invoices.addNonInvoicePage(); 
			continue

		identifiers = invoices.getIdentifiers();

		foundPage = False;
		for identifier in identifiers:
			pdf_id =  pdf.pq('LTTextLineHorizontal:contains("'+str(identifier)+'")')
			if(pdf_id):
				print identifier,
				searchFunction = identifiers[identifier];
				#Call the search function with a blank invoice Object
				blank_obj = Invoice();
				obj = searchFunction(blank_obj,pdf )
				invoices.add (page, searchFunction(Invoice(),pdf) )
				#print "Invoice:",obj.num,"PO:",obj.po,"JOB:",obj.job
				obj.printInvoice()
				foundPage = True;
				break;
		if(not foundPage):
			invoices.addNonInvoicePage();
			
	printToPDF(pdf_name,invoices)



def printToPDF(pdf_name,invoices):
	# read your existing PDF
	existing_pdf = PdfFileReader(file(pdf_name, "rb"))
	output_file = pdf_name + ".watermarked.pdf"
	output = PdfFileWriter()
	invoices = invoices.getInvoices()

	# Number of pages in input document
	page_count = existing_pdf.getNumPages()

	print "Page_count = " + str(page_count);
	print "Invoice Count=" + str(len(invoices));



	for p in range(page_count):
		packet = StringIO.StringIO()
		# create a new PDF with Reportlab
	
		invoice_string = job_string = po_string = ""

		invoice = invoices[p];

		#Blank Invoice
		if(invoice == None):
			page = existing_pdf.getPage(p)
			output.addPage(page)
			print "adding a non invoice page" + str(p)
			continue;
		


		invoice.cleanInvoice()
		invoice_string = str(invoice.num)
		job_string = str(invoice.job)
		po_string = str(invoice.po)

		can = canvas.Canvas(packet, pagesize=letter)
		#can.rect(x-20, y_min-20, 400, 100)
		x=150
		#x_max = 300
		y_min = 150
		y_max = 190

		y_stack = [y_max]

		if(len(invoice_string) < 50):
			last_y = y_stack[-1]
			y_stack.append(last_y - 20)
			can.drawString(x, last_y,		"INVOICE#: " + invoice_string)

		if(len(job_string) < 50):
			last_y = y_stack[-1]
			y_stack.append(last_y - 20)
			can.drawString(x, last_y,		"JOB        #: " + job_string)
		else:
			while len(job_string) > 0:
				last_y = y_stack[-1]
				y_stack.append(last_y - 20)
				can.drawString(x, last_y,	"JOB        #: " + job_string[0:50])
				job_string = job_string[50:]
			
		if(len(po_string) < 50):
			last_y = y_stack[-1]
			y_stack.append(last_y - 20)
			can.drawString(x, last_y,		"PO         #: " + po_string)

		width = 400
		height = 400
		#Shift pixels based on how many extra lines were added
		pixelShift = (len(y_stack) - 3) * 9
		can.rect(x-10,y_max-60 - pixelShift,width,100+pixelShift)

		can.save()
		#move to the beginning of the StringIO buffer
		packet.seek(0)
		new_pdf = PdfFileReader(packet)

		page = existing_pdf.getPage(p)
		page.mergePage(new_pdf.getPage(0))
		output.addPage(page)
		print "Adding to page" + str(p)


	# finally, write "output" to a real file
	outputStream = file(output_file, "wb")
	output.write(outputStream)
	outputStream.close()
	print "PRINTED TO "+ output_file
	print 'success'




#When printing to PDF, if previous invoice number matches current invoice number, and no PO, copy over PO
if __name__ == '__main__':
	main()
