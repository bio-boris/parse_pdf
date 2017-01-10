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
		#invoice_string = 'INVOICE NUMBER'
		#pdf_id =  pdf.pq('LTTextLineHorizontal:contains("'+str(invoice_string)+'")')
		#left_corner = float(pdf_id.attr('x0'))
		#bottom_corner = float(pdf_id.attr('y0'))
		#509 752
		#print left_corner,bottom_corner
		#invoice_string = '942510'
		#pdf_id =  pdf.pq('LTTextLineHorizontal:contains("'+str(invoice_string)+'")')
		#x0 = float(pdf_id.attr('x0')) #Left X 
		#y0 = float(pdf_id.attr('y0')) #Lower Y
		#x1 = float(pdf_id.attr('x1')) #Right X
		#y1 = float(pdf_id.attr('y1')) #Upper Y
		#print (x0,y0,x1,y1)

		invoice.num  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (525, 736, 600, 745)).text()
		

		return invoice





	def apache_rentals(invoice,pdf):
	#INVOICE
	#		x1 = 500
	#		y1 = 740
	#		x2 = 580
	#		y2 = 760
		#invoice_string = '77795A '
		#pdf_id =  pdf.pq('LTTextLineHorizontal:contains("'+str(invoice_string)+'")')
		#x0 = float(pdf_id.attr('x0')) #Left X 
		#y0 = float(pdf_id.attr('y0')) #Lower Y
		#x1 = float(pdf_id.attr('x1')) #Right X
		#y1 = float(pdf_id.attr('y1')) #Upper Y

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
		#if(not pdf_id):
		#	return invoice;

		#x0 = float(pdf_id.attr('x0')) #Left X 
		#y0 = float(pdf_id.attr('y0')) #Lower Y
		#x1 = float(pdf_id.attr('x1')) #Right X
		#y1 = float(pdf_id.attr('y1')) #Upper Y
		#width = (pdf_id.attr('width'))
		#height = (pdf_id.attr('height'))
		#print x0,x1,y0,y1
		#print width,height
		#print left_corner,bottom_corner
		#invoice.po  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x0,y0,x1,y1)).text()
		#invoice.po = invoice.po.replace(po_string,'')
		#return invoice

	def arizona_electric(invoice,pdf):
		#invoice_string = 'INVOICE NO.'
		#pdf_id =  pdf.pq('LTTextLineHorizontal:contains("'+str(invoice_string)+'")')
		#x0 = float(pdf_id.attr('x0')) #Left X 
		#y0 = float(pdf_id.attr('y0')) #Lower Y
		#x1 = float(pdf_id.attr('x1')) #Right X
		#y1 = float(pdf_id.attr('y1')) #Upper Y
		#print (x0,y0,x1,y1)
		#invoice_string = '5921-600318'
		#pdf_id =  pdf.pq('LTTextLineHorizontal:contains("'+str(invoice_string)+'")')
		#x0 = float(pdf_id.attr('x0')) #Left X 
		#y0 = float(pdf_id.attr('y0')) #Lower Y
		#x1 = float(pdf_id.attr('x1')) #Right X
		#y1 = float(pdf_id.attr('y1')) #Upper Y
		#print (x0,y0,x1,y1)
		invoice.num  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (400, 724, 455, 734)).text()
		invoice.num = re.sub("[^0-9^-]", "", invoice.num)
		return invoice

	#CED PHOENIX
	#CREDIT STATEMENT	
	def ced(invoice,pdf):
		#invoice_string = '5924-693095'
		#pdf_id =  pdf.pq('LTTextLineHorizontal:contains("'+str(invoice_string)+'")')
		#x0 = float(pdf_id.attr('x0')) #Left X 
		#y0 = float(pdf_id.attr('y0')) #Lower Y
		#x1 = float(pdf_id.attr('x1')) #Right X
		#y1 = float(pdf_id.attr('y1')) #Upper Y
		#print (x0,y0,x1,y1)
		invoice.num  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (400, 724, 460, 734)).text()
		invoice.num = re.sub("[^0-9^-]", "", invoice.num)
		
		return invoice


	def crescent(invoice,pdf):
		#invoice_string = 'S503002690.001'
		#pdf_id =  pdf.pq('LTTextLineHorizontal:contains("'+str(invoice_string)+'")')
		#x0 = float(pdf_id.attr('x0')) #Left X 
		#y0 = float(pdf_id.attr('y0')) #Lower Y
		#x1 = float(pdf_id.attr('x1')) #Right X
		#y1 = float(pdf_id.attr('y1')) #Upper Y
		#print (x0,y0,x1,y1)
		invoice.num  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (520, 738, 570, 746)).text()
		invoice.num = re.sub(" .+", "", invoice.num)
		invoice.num = re.sub(" .+", "", invoice.num)

		#invoice_string = '2016-62/49016'
		#pdf_id =  pdf.pq('LTTextLineHorizontal:contains("'+str(invoice_string)+'")')
		#x0 = float(pdf_id.attr('x0')) #Left X 
		#y0 = float(pdf_id.attr('y0')) #Lower Y
		#x1 = float(pdf_id.attr('x1')) #Right X
		#y1 = float(pdf_id.attr('y1')) #Upper Y
		#print (x0,y0,x1,y1)
		invoice.po = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (220, 515, 290, 523)).text()
		invoice.po = re.sub(" .+", "", invoice.po)
		invoice.po = re.sub(" .+", "", invoice.po)

		return invoice

	def ies_supply(invoice,pdf):
		#invoice_string = 'S103035222.001'
		#pdf_id =  pdf.pq('LTTextLineHorizontal:contains("'+str(invoice_string)+'")')
		#x0 = float(pdf_id.attr('x0')) #Left X 
		#y0 = float(pdf_id.attr('y0')) #Lower Y
		#x1 = float(pdf_id.attr('x1')) #Right X
		#y1 = float(pdf_id.attr('y1')) #Upper Y
		#print (x0,y0,x1,y1)
																			#521.28, 707.258, 586.055, 720.89
		invoice.num  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (520, 707, 600, 720)).text()


		#invoice_string = '2016-03'
		#pdf_id =  pdf.pq('LTTextLineHorizontal:contains("'+str(invoice_string)+'")')
		#x0 = float(pdf_id.attr('x0')) #Left X 
		#y0 = float(pdf_id.attr('y0')) #Lower Y
		#x1 = float(pdf_id.attr('x1')) #Right X
		#y1 = float(pdf_id.attr('y1')) #Upper Y
		#print (x0,y0,x1,y1)													#171.36, 513.218, 202.561, 526.85
		invoice.po  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (165, 513, 210, 525)).text()
		invoice.po = re.sub(" .+", "", invoice.po)
		
		#invoice_string = 'CHRISTIAN CARE'
		#pdf_id =  pdf.pq('LTTextLineHorizontal:contains("'+str(invoice_string)+'")')
		#x0 = float(pdf_id.attr('x0')) #Left X 
		#y0 = float(pdf_id.attr('y0')) #Lower Y
		#x1 = float(pdf_id.attr('x1')) #Right X
		#y1 = float(pdf_id.attr('y1')) #Upper Y
		#print (x0,y0,x1,y1)
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



#, ,  and IES



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
		can.drawString(x, y_max,    		"Invoice   #: " + invoice_string)
		can.drawString(x, (y_min+y_max)/2,  "JOB       #: " + job_string)
		can.drawString(x, y_min, 			"PO        #: " + po_string)
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




#DEBUG CODE
	#invoices = Invoices()
	#identifiers = invoices.getIdentifiers();
	#identifier='ARIZONA ELECTRIC SUPPLY'
	#searchFunction = identifiers[identifier];
	#pdf.load(19)
	#obj = searchFunction(Invoice(),pdf ) 
	#print obj.num
	#print obj.po
	#exit()


'''
ANXITER
<text font="Arial Bold" bbox="500.001,743.900,506.671,757.840" size="13.940">S</text>
<text font="Arial Bold" bbox="506.671,743.900,513.341,757.840" size="13.940">E</text>
<text font="Arial Bold" bbox="513.341,743.900,518.901,757.840" size="13.940">4</text>
<text font="Arial Bold" bbox="518.901,743.900,524.461,757.840" size="13.940">0</text>
<text font="Arial Bold" bbox="524.461,743.900,530.021,757.840" size="13.940">2</text>
<text font="Arial Bold" bbox="530.021,743.900,535.581,757.840" size="13.940">1</text>
<text font="Arial Bold" bbox="535.581,743.900,541.141,757.840" size="13.940">9</text>
<text font="Arial Bold" bbox="541.141,743.900,546.701,757.840" size="13.940">8</text>
<text font="Arial Bold" bbox="546.701,743.900,552.261,757.840" size="13.940">8</text>
<text font="Arial Bold" bbox="552.261,743.900,557.821,757.840" size="13.940">3</text>
<text font="Arial Bold" bbox="557.821,743.900,560.601,757.840" size="13.940">.</text>
<text font="Arial Bold" bbox="560.601,743.900,566.161,757.840" size="13.940">0</text>
<text font="Arial Bold" bbox="566.161,743.900,571.721,757.840" size="13.940">0</text>
<text font="Arial Bold" bbox="571.721,743.900,577.281,757.840" size="13.940">1</text>


X1,Y1,X2,Y2

X1 = 500
X2 = 580

Y1 = 740
Y2 = 760
'''

'''

WESCO
<textbox id="8" bbox="533.250,733.305,561.598,743.505">
<textline bbox="533.250,733.305,561.598,743.505">
<text font="Arial" bbox="533.250,733.305,537.975,743.505" size="10.200">9</text>
<text font="Arial" bbox="537.975,733.305,542.699,743.505" size="10.200">4</text>
<text font="Arial" bbox="542.699,733.305,547.424,743.505" size="10.200">0</text>
<text font="Arial" bbox="547.424,733.305,552.149,743.505" size="10.200">9</text>
<text font="Arial" bbox="552.149,733.305,556.873,743.505" size="10.200">8</text>
<text font="Arial" bbox="556.873,733.305,561.598,743.505" size="10.200">6</text>
<text>
</text>
</textline>
</textbox>
X1 = 520
X2 = 565
Y1 = 730
Y2 = 745

'''

'''
APACHE
X =440
X =485
Y =685
Y =705

<textline bbox="453.050,692.183,480.971,703.239">
<text font="AAAAAA+Arial" bbox="453.050,692.183,457.554,703.239" size="11.057">7</text>
<text font="AAAAAA+Arial" bbox="457.554,692.183,462.057,703.239" size="11.057">7</text>
<text font="AAAAAA+Arial" bbox="462.057,692.183,466.561,703.239" size="11.057">7</text>
<text font="AAAAAA+Arial" bbox="466.561,692.183,471.064,703.239" size="11.057">9</text>
<text font="AAAAAA+Arial" bbox="471.064,692.183,475.568,703.239" size="11.057">5</text>
<text font="AAAAAA+Arial" bbox="475.568,692.183,480.971,703.239" size="11.057">A</text>
<text>
</text>
</textline>
'''

'''
Fishertools
X=460
X=530
y=581
y=594

<text font="Calibri" bbox="460.730,581.080,465.911,594.037" size="12.957">C</text>
<text font="Calibri" bbox="465.911,581.080,472.345,594.037" size="12.957">O</text>
<text font="Calibri" bbox="472.345,581.080,478.625,594.037" size="12.957">N</text>
<text font="Calibri" bbox="478.625,581.080,484.602,594.037" size="12.957">D</text>
<text font="Calibri" bbox="484.602,581.080,490.843,594.037" size="12.957">U</text>
<text font="Calibri" bbox="490.843,581.080,495.887,594.037" size="12.957">X</text>
<text font="Calibri" bbox="495.887,581.080,498.084,594.037" size="12.957"> </text>
<text font="Calibri" bbox="498.084,581.080,502.818,594.037" size="12.957">T</text>
<text font="Calibri" bbox="502.818,581.080,509.058,594.037" size="12.957">U</text>
<text font="Calibri" bbox="509.058,581.080,515.191,594.037" size="12.957">G</text>
<text font="Calibri" bbox="515.191,581.080,521.324,594.037" size="12.957">G</text>
<text font="Calibri" bbox="521.324,581.080,526.068,594.037" size="12.957">E</text>
<text font="Calibri" bbox="526.068,581.080,531.346,594.037" size="12.957">R</text>
<text>
'''

