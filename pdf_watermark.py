#!/usr/bin/env python
import pdfquery
from pyPdf import PdfFileWriter, PdfFileReader
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

#Custom Libraries
from inv import *

print "Check Logfile"


def main():
	#1. Loads up the PDF and gets the number of pages
	if len(sys.argv) >= 2:
		pdf_name = sys.argv[1]
		log_name = pdf_name + ".log.txt"
		sys.stdout = open(log_name, 'w')
		print "About to open " + str(pdf_name)
		sys.stdout.flush()
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
		print "About to load " + str(page+1),
		sys.stdout.flush()
		try:
			pdf.load(page)
		except:
			print "ERROR: Couldn't load page " + str(page+1)
			sys.stdout.flush()
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
			print ""
			
	printToPDF(pdf_name,invoices)





#Pass in invoice, and current page
def getWaterMarkedPage(invoice,page):

	invoice_string = ''
	job_string = ''
	po_string = ''

	if(invoice != None):
		invoice.cleanInvoice()
		if(invoice.num == None):
			invoice_string = ""
		else:
			invoice_string = str(invoice.num)
		if(invoice.job == None):
			invoice.job = ""
		else:
			job_string = str(invoice.job)
		if(invoice.po == None):
			invoice.po = ""
		else:
			po_string = str(invoice.po)
	
		

	packet = StringIO.StringIO()
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

	packet.seek(0)

	watermark = PdfFileReader(packet);
	
	page.mergePage(watermark.getPage(0))

	return  page;
		
		



#missing the PO or Job


def printToPDF(pdf_name,invoices):
	# read your existing PDF
	existing_pdf = PdfFileReader(file(pdf_name, "rb"))
	output_file = pdf_name + ".watermarked.pdf"
	invoices = invoices.getInvoices()
	# Number of pages in input document
	page_count = existing_pdf.getNumPages()

	#PDF output
	outputPDF = PdfFileWriter()

	incomplete_pages = []
	for p in range(page_count):
		

		invoice = invoices[p];
		if(invoice != None):
			complete_flag = invoice.setCompletionFlag()
		else:
			complete_flag = False
		#CHECK TO SEE IF PAGE IS BROKEN

		#Create a watermarked version of the page
		watermarked_page = getWaterMarkedPage(invoice,existing_pdf.getPage(p))
		
		#Print the page with the PDF
		if(complete_flag == True):
			outputPDF.addPage(watermarked_page)	
			print "Added COMPLETE PDF page # " + str(p + 1)	
		#Don't move pages that don't have invoice, assume they are placeholder pages
		elif(complete_flag == False and invoice != None):
			outputPDF.addPage(watermarked_page)	
			print "Added NON INVOICE PDF page # " + str(p + 1)
		#Save the PDF page for printing later	
		else:
			incomplete_pages.append([watermarked_page,p])
		sys.stdout.flush()

	#Add incomplete pages
	for page in incomplete_pages:
		outputPDF.addPage(page[0]);
		print "Added [missing PO or JOB#] PDF page # " + str(page[1] + 1) 
		sys.stdout.flush()
	

	# finally, write "output" to a real file
	#new_pdf = PdfFileReader(packet)
	
	outputStream = file(output_file, "wb")
	outputPDF.write(outputStream)
	outputStream.close()
	print "success: printed PDF to "+ output_file





#When printing to PDF, if previous invoice number matches current invoice number, and no PO, copy over PO
if __name__ == '__main__':
	main()
