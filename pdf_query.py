#!/usr/bin/env python
import pdfquery
from pyPdf import PdfFileWriter, PdfFileReader
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import re
import sys



class Invoice:
	page = None;
	num = None;
	po = None;
	job = None;
	identifier = None;

class Invoices:
	invoices = []


	def add(__self__,page,invoice):
		invoice.page = page
		__self__.invoices.append( invoice)

	def getInvoices(__self__):
		return __self__.invoices

	def getIdentifiers(__self__):
		return __self__.identifiers

	

	def anixter(invoice,pdf):
		#Get InvoiceNumber
		#invoice_string = str('INVOICE')
		x1 = 500
		y1 = 740
		x2 = 580
		y2 = 760
		invoice.num = pdf.pq(':in_bbox("%s, %s, %s, %s")' % (x1,y1,x2,y2)).text()

		#Get Purchase Order PO#
		po_string = 'PURCHASE ORDER NUMBER'
		pdf_id =  pdf.pq('LTTextLineHorizontal:contains("'+str(po_string)+'")')
		left_corner = float(pdf_id.attr('x0'))
		bottom_corner = float(pdf_id.attr('y0'))
		invoice.po  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (left_corner, bottom_corner-15, left_corner+150, bottom_corner)).text()
	
		return invoice

	def wesco(invoice,pdf):
		#INVOICE
		invoice.num  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (525, 736, 600, 745)).text()
		

		return invoice





	def apache_rentals(invoice,pdf):
		#INVOICE
		invoice.num  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (453.6, 694.106, 473.142, 703.193)).text()
		invoice.num = invoice.num.replace("Invoice",'')
		invoice.num = re.sub("[#: ]", "", invoice.num)

		#PO
		po_string = 'PO #:'
		pdf_id =  pdf.pq('LTTextLineHorizontal:contains("'+str(po_string)+'")')
		left_corner = float(pdf_id.attr('x0'))
		bottom_corner = float(pdf_id.attr('y0'))
		#print left_corner,bottom_corner

		invoice.po  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (left_corner+1,bottom_corner,left_corner+100,bottom_corner+15)).text()
		
		return invoice

	def fisher_tools(invoice,pdf):
		invoice_string = 'Invoice Number'
		pdf_id =  pdf.pq('LTTextLineHorizontal:contains("'+str(invoice_string)+'")')
		x0 = float(pdf_id.attr('x0')) #Left X 
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.num  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x0, y0, x0+300, y1)).text()
		
		invoice.num = re.sub("Customer", "", invoice.num)
		invoice.num = re.sub("Invoice", "", invoice.num)
		invoice.num = re.sub("Repair", "", invoice.num)
		invoice.num = re.sub("Number", "", invoice.num)
		invoice.num = re.sub("[ :]", "", invoice.num)
		invoice.num = re.sub("#[0-9].", "", invoice.num)
		invoice.num = re.sub("#", "", invoice.num)
		

		#print "About to find PO"
		po_string = 'Customer PO'
		#This is in case there is no Customer PO, but there is something else instead
		pdf_id =  pdf.pq('LTTextLineHorizontal:contains("'+str(po_string)+'")')

		if(pdf_id):
			x0 = float(pdf_id.attr('x0')) #Left X 
			y0 = float(pdf_id.attr('y0')) #Lower Y
			x1 = float(pdf_id.attr('x1')) #Right X
			y1 = float(pdf_id.attr('y1')) #Upper Y
			invoice.po  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x0,y0,x1+100,y1)).text()
			invoice.po = invoice.po.replace("Customer PO","")
			invoice.po = re.sub("[#: ]", "", invoice.po)
		
		return invoice

	def arizona_electric(invoice,pdf):
		invoice.num  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (400, 724, 455, 734)).text()
		invoice.num = re.sub("[^0-9^-]", "", invoice.num)
		return invoice

	#CED PHOENIX
	#CREDIT STATEMENT	
	def ced(invoice,pdf):
		invoice.num  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (400, 724, 460, 734)).text()
		invoice.num = re.sub("[^0-9^-]", "", invoice.num)
		
		return invoice


	def crescent(invoice,pdf):
		invoice.num  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (520, 738, 570, 746)).text()
		invoice.num = re.sub(" .+", "", invoice.num)
		invoice.num = re.sub(" .+", "", invoice.num)

		invoice.po = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (220, 515, 290, 523)).text()
		invoice.po = re.sub(" .+", "", invoice.po)
		invoice.po = re.sub(" .+", "", invoice.po)

		return invoice

	def ies_supply(invoice,pdf):
		invoice.num  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (520, 707, 600, 720)).text()

		invoice.po  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (165, 513, 210, 525)).text()
		invoice.po = re.sub(" .+", "", invoice.po)

		invoice.job  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (340, 510, 450, 525)).text()
		invoice.job = invoice.job .replace("TERMS","")

		return invoice


	identifiers = {'Anixter Power Solutions, LLC' : anixter,
	'WESCO.COM' : wesco,
	'apacherentals.com': apache_rentals,
	'fishertools.com' : fisher_tools,
	'CED-PHOENIX': arizona_electric,
	'CED - PHOENIX': ced,
	'www.cesco.com': crescent,
	'iesupply.billtrust.com': ies_supply}



def printToPDF(pdf_name,invoices):
	# read your existing PDF
	existing_pdf = PdfFileReader(file(pdf_name, "rb"))
	output_file = pdf_name + ".watermarked.pdf"
	output = PdfFileWriter()
	invoices = invoices.getInvoices()

	# Number of pages in input document
	page_count = existing_pdf.getNumPages()

	# create and add the "watermark" 
	#(which is the new pdf) on the existing page
	for p in range(page_count):
		packet = StringIO.StringIO()
		# create a new PDF with Reportlab
		x= 200
		y_min = 150
		y_max = 200

		invoice_string = job_string = po_string = ""

		for invoice in invoices:
			if(invoice.page == p):
				invoice_string = str(invoice.num)
				job_string = str(invoice.job)
				po_string = str(invoice.po)


		can = canvas.Canvas(packet, pagesize=letter)
		can.rect(x-20, y_min-20, 200, 100)
		can.drawString(x, y_max,		"Invoice   #: " + invoice_string)
		can.drawString(x, (y_min+y_max)/2,	"JOB       #: " + job_string)
		can.drawString(x, y_min,		"PO        #: " + po_string)
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


def main():
	if len(sys.argv) > 1:
		pdf_name = sys.argv[1]
		print "About to open " + str(pdf_name)
	else:
		exit("Error: Please Input a PDF")
	
	pdf = pdfquery.PDFQuery(pdf_name)
	pdf_count = pdf.doc.catalog['Pages'].resolve()['Count']

	invoices = Invoices()
	for page in range(pdf_count):
		print "About to load " + str(page)
		pdf.load(page)
		identifiers = invoices.getIdentifiers();
		for identifier in identifiers:
			pdf_id =  pdf.pq('LTTextLineHorizontal:contains("'+str(identifier)+'")')
			if(pdf_id):
				print identifier,
				searchFunction = identifiers[identifier];
				#Call the search function with a blank invoice Object
				obj = searchFunction(Invoice(),pdf ) 
				invoices.add (page, searchFunction(Invoice(),pdf) )
				print "Invoice:",obj.num,"PO:",obj.po,"JOB:",obj.job
				continue;
	printToPDF(pdf_name,invoices)

#When printing to PDF, if previous invoice number matches current invoice number, and no PO, copy over PO
if __name__ == '__main__':
	main()
