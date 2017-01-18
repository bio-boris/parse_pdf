#!/usr/bin/env python
import pdfquery
import textwrap
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


	def splitLongLines(self,string):
		return string



	#Removes whitespace
	def cleanInvoice(self):
		if self.num != None:
			self.num = self.num.lstrip().rstrip()
			self.num = self.splitLongLines(self.num)
			if(not self.num):
				self.num = None
		if self.po != None:
			self.po = self.po.lstrip().rstrip()
			self.po = self.splitLongLines(self.po)
			if(not self.po):
				self.po = None
		if self.job !=None:
			self.job = self.job.lstrip().rstrip()
			self.job = self.splitLongLines(self.job)
			if(not self.job):
				self.job = None

	def printInvoice(self):
		self.cleanInvoice()
		print 'Invoice:' + str(self.num),
		print 'PO:' + str(self.po),
		print "Job:" + str(self.job)

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
		invoice.num = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (500,740,580,760)).text()

		#Get Purchase Order PO#
		po_string = 'PURCHASE ORDER NUMBER'
		pdf_id =  pdf.pq('LTTextLineHorizontal:contains("'+str(po_string)+'")')
		left_corner = float(pdf_id.attr('x0'))
		bottom_corner = float(pdf_id.attr('y0'))
		invoice.po  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (left_corner, bottom_corner-15, left_corner+150, bottom_corner)).text()


		#pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('RELEASE NUMBER')+'")') 
		#x0 = float(pdf_id.attr('x0')) #Left X
		#y0 = float(pdf_id.attr('y0')) #Lower Y
		#x1 = float(pdf_id.attr('x1')) #Right X
		#y1 = float(pdf_id.attr('y1')) #Upper Y
		#print(x0,y0,x1,y1)
		#invoice.job  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (400,0,1000,1000)).text()
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
		x0 = float(pdf_id.attr('x0'))
		y0 = float(pdf_id.attr('y0'))
		x1 = float(pdf_id.attr('x0'))
		y1 = float(pdf_id.attr('y1'))
		invoice.po  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x0,y1-1,x1+40,y1+1)).text()
		if(invoice.po):
			invoice.po = invoice.po.replace(po_string,'')
			invoice.po = invoice.po.replace(' ','')

		#JOB
		invoice.job  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (450, 645, 600, 656)).text()
	

	
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

	#Arizona Electric Supply
	def arizona_electric(invoice,pdf):
		invoice.num  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (400, 724, 455, 734)).text()
		invoice.num = re.sub("[^0-9^-]", "", invoice.num)

		#pdf_id =  pdf.pq('LTTextLineHorizontal:contains("'+str('201666')+'")')
		#x0 = float(pdf_id.attr('x0')) #Left X
		#y0 = float(pdf_id.attr('y0')) #Lower Y
		#x1 = float(pdf_id.attr('x1')) #Right X
		#y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.po  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (495, 516, 600, 527)).text()
		print invoice.po
			

	
		return invoice

	#Consolidated Electrical Distributors
	#CED PHOENIX
	#CREDIT STATEMENT
	def ced(invoice,pdf):
		invoice.num  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (400, 724, 460, 734)).text()
		invoice.num = re.sub("[^0-9^-]", "", invoice.num)

		invoice.job  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (315, 515, 360, 527)).text()
		invoice.job = invoice.job.replace("JOB",'')
		invoice.job = invoice.job.replace("NAME",'')

		
		invoice.po  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (500, 515, 600, 527)).text()
		invoice.po = invoice.po.replace("CUSTOMER ORDER NO.",'')
		

		
		return invoice

	#Cesco.co
	def crescent(invoice,pdf):
		invoice.num  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (520, 738, 570, 746)).text()
		invoice.num = re.sub(" .+", "", invoice.num)
		invoice.num = re.sub(" .+", "", invoice.num)

			
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('SHIP VIA')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.po  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x0,y0,x1,y1+5)).text()
		invoice.po = invoice.po.replace("SHIP VIA",'')

		invoice.job  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (480, 593.305-10, 520, 603)).text()
		invoice.job = invoice.job.replace("REFERENCE",'')

		return invoice

	def ies_supply(invoice,pdf):
		invoice.num  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (520, 707, 600, 720)).text()

		invoice.po  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (165, 513, 210, 525)).text()
		invoice.po = re.sub(" .+", "", invoice.po)

		invoice.job  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (340, 510, 450, 525)).text()
		invoice.job = invoice.job .replace("TERMS","")

		return invoice

	def a_breaker(invoice,pdf):
		#invoice_string = "60033"
		#pdf_id =  pdf.pq('LTTextLineHorizontal:contains("'+str(invoice_string)+'")')
		#x0 = float(pdf_id.attr('x0')) #Left X
		#y0 = float(pdf_id.attr('y0')) #Lower Y
		#x1 = float(pdf_id.attr('x1')) #Right X
		#y1 = float(pdf_id.attr('y1')) #Upper Y
		#print(x0,y0,x1,y1)

		return invoice

	def acme_tool(invoice,pdf):
		#invoice_string = "S2587453 .001"
		#pdf_id =  pdf.pq('LTTextLineHorizontal:contains("'+str(invoice_string)+'")')
		#x0 = float(pdf_id.attr('x0')) #Left X
		#y0 = float(pdf_id.attr('y0')) #Lower Y
		#x1 = float(pdf_id.attr('x1')) #Right X
		#y1 = float(pdf_id.attr('y1')) #Upper Y
		#print(x0,y0,x1,y1)
		invoice.num  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (500, 709, 600, 728)).text()
		invoice.num = invoice.num.replace(" ",'')
		
		#invoice_string = "48223"
		#pdf_id =  pdf.pq('LTTextLineHorizontal:contains("'+str(invoice_string)+'")')
		#x0 = float(pdf_id.attr('x0')) #Left X
		#y0 = float(pdf_id.attr('y0')) #Lower Y
		#x1 = float(pdf_id.attr('x1')) #Right X
		#y1 = float(pdf_id.attr('y1')) #Upper Y
		#print(x0,y0,x1,y1)
		invoice.po  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (108, 524, 150, 543)).text()
		return invoice

	def bazzille(invoice,pdf):
		#INVOICE 
		invoice.num  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (410, 617, 500, 633)).text()
		invoice.num = invoice.num.replace("INVOICE","")
		invoice.num = invoice.num.replace("#","")
		invoice.num = invoice.num.replace(" ","")


		#JOB
		invoice.job  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (240, 522, 290, 537)).text()
		
		#PO
		#invoice_string = "2016-03"
		#pdf_id =  pdf.pq('LTTextLineHorizontal:contains("'+str(invoice_string)+'")')
		#x0 = float(pdf_id.attr('x0')) #Left X
		#y0 = float(pdf_id.attr('y0')) #Lower Y
		#x1 = float(pdf_id.attr('x1')) #Right X
		#y1 = float(pdf_id.attr('y1')) #Upper Y
		#print (x0,y0,x1,y1)
		invoice.po  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (355, 521, 400, 537)).text()
		return invoice

	def border_state_electric(invoice,pdf):
		#INVOICE
		invoice.num  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (270, 753, 320, 763)).text()
		invoice.num = invoice.num.replace("Invoice",'')
		invoice.num = invoice.num.replace(":",'')
		invoice.num = invoice.num.replace(" ",'')
		#PO
		invoice.po = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (270, 735, 320, 747)).text()
		#JOB
		invoice.job =  pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (270, 725, 320, 740)).text()

		return invoice

	#First Cut Identifier: 602-431-0068
	def first_cut(invoice,pdf):
		#pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('61111')+'")') 
		#x0 = float(pdf_id.attr('x0')) #Left X
		#y0 = float(pdf_id.attr('y0')) #Lower Y
		#x1 = float(pdf_id.attr('x1')) #Right X
		#y1 = float(pdf_id.attr('y1')) #Upper Y

		invoice.num  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (530, 715, 600, 730)).text()
		invoice.num = re.sub("[^0-9]", "", invoice.num)

		#pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('Job #')+'")') 
		#x0 = float(pdf_id.attr('x0')) #Left X
		#y0 = float(pdf_id.attr('y0')) #Lower Y
		#x1 = float(pdf_id.attr('x1')) #Right X
		#y1 = float(pdf_id.attr('y1')) #Upper Y

		invoice.job = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (300, 550, 600, 630)).text()
		invoice.job = invoice.job.replace("Job # / Name / Address: ",'')


		#PO
		invoice.po = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (185, 509, 230, 524)).text()
		invoice.po = invoice.po.replace("Customer PO",'')
		return invoice

	#Identifier:
	def glendale_industrial(invoice,pdf):
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('INVOICE NUMBER')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.num  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x0-20,y0-5,x1,y1)).text()
		invoice.num = invoice.num.replace("INVOICE NUMBER",'')
	

		#pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('2015-71')+'")') 
		#x0 = float(pdf_id.attr('x0')) #Left X
		#y0 = float(pdf_id.attr('y0')) #Lower Y
		#x1 = float(pdf_id.attr('x1')) #Right X
		#y1 = float(pdf_id.attr('y1')) #Upper Y
		#print(x0,y0,x1,y1)
		invoice.po  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (335, 537, 390, 557)).text()
		#invoice.po = invoice.po.replace("CUSTOMER P.O. NO.",'')
		
		#pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('SHIP')+'")') 
		#x0 = float(pdf_id.attr('x0')) #Left X
		#y0 = float(pdf_id.attr('y0')) #Lower Y
		#x1 = float(pdf_id.attr('x1')) #Right X
		#y1 = float(pdf_id.attr('y1')) #Upper Y
		#JOB
		invoice.job  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (320, 608, 500, 660)).text()
		invoice.job = invoice.job.replace("SHIP TO",'')
		return invoice

	#Identifier: graybar.com
	def graybar(invoice,pdf):
		#INVOICE
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('Invoice No:')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.num  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x0,y0,x1+200,y1)).text()
		invoice.num = invoice.num.replace("Invoice No:",'')
		
		#PO
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('Order No:')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.po  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x0,y0,x1+200,y1)).text()
		invoice.po= invoice.po.replace("Order No:",'')
		
		#JOB
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('Rt.')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.job  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x0,y0,x1+200,y1)).text()
		invoice.job= invoice.job.replace("Rt.",'')
		invoice.job= invoice.job.replace("TO",'')

		return invoice

	#Identifier: whitecap.com
	#HD Supply Construction
	def white_cap(invoice,pdf):
		#INVOICE
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('INVOICE NUMBER')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.num  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x0-1,y0-10,x1+200,y1)).text()
		invoice.num = invoice.num.replace("INVOICE NUMBER",'')
		invoice.num = re.sub(r'\W+', "", invoice.num)
	

		#PO
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('CUSTOMER')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.po  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x0-1,y0-10,x1+200,y1)).text()
		invoice.po = invoice.po.replace("CUSTOMER PO NUMBER",'')
		
	
		#JOB
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('CUSTOMER JOB NO.')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.job  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x0-1,y0-10,x1+200,y1)).text()
		invoice.job = invoice.job.replace("CUSTOMER JOB NO.",'')
		invoice.job = re.sub(r'\W+', "", invoice.job)
		return invoice
		
	#Identifier: us.hilti.com
	def hilti(invoice,pdf):
		#INVOICE
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('INVOICE NUMBER')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.num  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x1,y0-1,x1+200,y1+1)).text()
		invoice.num = invoice.num.replace("INVOICE NUMBER:",'')
		invoice.num = re.sub(r'\W+', "", invoice.num)
	

		#PO
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('CUSTOMER P.O. NUMBER')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.po  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x0-1,y0-15,x1+200,y1)).text()
		invoice.po = invoice.po.replace("CUSTOMER P.O. NUMBER:",'')
		
	
		#JOB
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('FEDERAL ID:')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.job  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x0-100,y0-100,x1,y0)).text()
		
		return invoice

	#Identifier: lu-az.com
	def lightning_unlimited(invoice,pdf):
		#INVOICE
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('Invoice')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.num  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x1,y0-10,x1+10,y0)).text()
		invoice.num = invoice.num.replace("Invoice",'')
		invoice.num = invoice.num.replace("#",'')
		
		#PO
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('Ship Via')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.po  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x0-100,y0-15,x0-1,y0-1)).text()
	
		#JOB
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('Job Number')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.job  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x0-1,y0-10,x1+10,y0)).text()
			
		return invoice

	#Identifier: newwesternrentals.com
	def new_western(invoice,pdf):
		#INVOICE
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('Invoice')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.num  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x1,y0,x1+100,y1)).text()
	
		
		#PO
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('PO #:')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.po  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x1+1,y0,x1+200,y1)).text()

	
		#JOB
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('Job Descr')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.job  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x1+1,y0,x1+200,y0)).text()

		return invoice

	#Identifier: ProBox Portable Storage
	def pro_box(invoice,pdf):
		#INVOICE
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('Invoice #')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.num  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x1+1,y0,x1+200,y1)).text()
	
		
		#PO
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('PO #')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.po  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x1+1,y0,x1+200,y1)).text()

	
		#JOB
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('Delivered To')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.job  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x0-1,y1-50,x1+50,y0-1)).text()

		return invoice

	#Identifier: Damage Waiver is NOT INSURANCE
	def ross_equipment(invoice,pdf):
		#INVOICE
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('Invoice #')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.num  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x1+1,y0,x1+200,y1)).text()
		invoice.num = re.sub('[\W]','',invoice.num)
		
		#PO
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('P.O.')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.po  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x1+58,y0-1,x1+200,y1+1)).text()
		invoice.po = invoice.po.replace(".",'')
	
		#JOB
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('job No')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y

		invoice.job  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x1+1,y0-1,x1+200,y1+1)).text()
		invoice.job = invoice.job.replace(".",'')
		return invoice

	#Identifier: Southwest Fastener LLC
	def southwest_fastener(invoice,pdf):
		#INVOICE
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('Invoice')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.num  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x1,y1,x1+200,y1+10)).text()
		invoice.num = re.sub('Invoice','',invoice.num)
		
		#PO
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('PO Number')+'")') 
		
		if(pdf_id):
			x0 = float(pdf_id.attr('x0')) #Left X
			y0 = float(pdf_id.attr('y0')) #Lower Y
			x1 = float(pdf_id.attr('x1')) #Right X
			y1 = float(pdf_id.attr('y1')) #Upper Y
			invoice.po  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x0-1,y0-30,x1+50,y1-1)).text()
			invoice.po = invoice.po.replace("PO Number",'')
	
		#JOB
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('Ship To:')+'")') 
		if(pdf_id):
			x0 = float(pdf_id.attr('x0')) #Left X
			y0 = float(pdf_id.attr('y0')) #Lower Y
			x1 = float(pdf_id.attr('x1')) #Right X
			y1 = float(pdf_id.attr('y1')) #Upper Y
			invoice.job = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x0-1,y0-50,x0+200,y0)).text()
			invoice.job = invoice.job.replace(".",'')

		return invoice

	#Identifier: summit.com
	def summit_electric(invoice,pdf):
		#INVOICE
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('INVOICE')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.num  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x0-10,y0-5,x1+50,y1)).text()
		invoice.num = invoice.num.replace("INVOICE",'')
		invoice.num = invoice.num.replace("NUMBER",'')
		
		#PO
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('PURCHASE ORDER')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.po  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x0-10,y0-5,x1+50,y1)).text()
		invoice.po = invoice.po.replace("PURCHASE",'')
		invoice.po = invoice.po.replace("ORDER",'')
		invoice.po = re.sub("[^0-9^-]", "", invoice.po)
		#For some reason the 2016 is not proper
		if(not invoice.po[0] == '2' and invoice.po[0] == '0' ):
			invoice.po = '2' + str(invoice.po)

		#JOB
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('JOB NAME')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.job  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x0-10,y0-5,x1+50,y1)).text()
		invoice.job = invoice.job.replace("JOB",'')
		invoice.job = invoice.job.replace("NAME",'')
		return invoice

	#Identifier: ur.com
	def united_rentals(invoice,pdf):
		#INVOICE
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('INVOICE')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.num  = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x0-30,y0-15,x1+200,y0)).text()
		invoice.num =invoice.num.replace("#",'').replace('INVOICE','')

		
		#PO
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('P.O.')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.po  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x1+1,y0,x1+200,y1)).text()
		invoice.po =invoice.po.replace(":",'')
		invoice.po =invoice.po.replace("#",'')
	
		#JOB
		pdf_id = pdf.pq('LTTextLineHorizontal:contains("'+str('job Ldc')+'")') 
		x0 = float(pdf_id.attr('x0')) #Left X
		y0 = float(pdf_id.attr('y0')) #Lower Y
		x1 = float(pdf_id.attr('x1')) #Right X
		y1 = float(pdf_id.attr('y1')) #Upper Y
		invoice.job  = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x1+1,y0,x1+200,y1)).text()
		invoice.job =invoice.job.replace(":",'')
		invoice.job =invoice.job.replace("#",'')

		return invoice




	identifiers = {'Anixter Power Solutions, LLC' : anixter,
	'WESCO.COM' : wesco,
	'apacherentals.com': apache_rentals,
	'fishertools.com' : fisher_tools,
	'CED-PHOENIX': arizona_electric,
	'CED - PHOENIX': ced,
	'www.cesco.com': crescent,
	'iesupply.billtrust.com': ies_supply,
	'abreakerco.com' :a_breaker,
	'acmetool.com' : acme_tool,
	'bazzillengraving.com' : bazzille,
	'BSE Invoice': border_state_electric,
	'602-431-0068' : first_cut,
	'GLENDALE': glendale_industrial,
	'graybar.com' : graybar,
	'whitecap.com' : white_cap,
	'us.hilti.com' : hilti, 
	'lu-az.com' : lightning_unlimited,
	'newwesternrentals.com' : new_western,
	'ProBox Portable Storage': pro_box,
	'Damage Waiver is NOT INSURANCE' : ross_equipment,
	'Southwest Fastener LLC': southwest_fastener,
	'summit.com':summit_electric,
	'ur.com':united_rentals}


#TODO
#Invoices that are missing PO or JOB field go to the end





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

	#Sort pages
	#pages_to_print_first = []
	#pages_to_print_last = []
	#for p in range(page_count):
	#	for invoice in invoices:
	#		if(invoice.page == p):
	#			if(invoice.num != None and
	#				invoice.po != None and
	#				invoice.job != None):
#						pages_to_print_first.append(p)
	#			else:
	#				pages_to_print_last.append(p)

	#pages_to_print = pages_to_print_first + pages_to_print_last#

	#print pages_to_print
	#print len(pages_to_print)
	#exit()



	for p in range(page_count):
		packet = StringIO.StringIO()
		# create a new PDF with Reportlab
	
		invoice_string = job_string = po_string = ""

		for invoice in invoices:
			if(invoice.page == p):
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
	for page in range(pdf_count):

		print "About to load " + str(page)
		try:
			pdf.load(page)
		except:
			print "ERROR: Couldn't load page " + str(page) 
			continue
		identifiers = invoices.getIdentifiers();
		for identifier in identifiers:
			pdf_id =  pdf.pq('LTTextLineHorizontal:contains("'+str(identifier)+'")')
			if(pdf_id):
				print identifier,
				searchFunction = identifiers[identifier];
				#Call the search function with a blank invoice Object
				obj = searchFunction(Invoice(),pdf )
				invoices.add (page, searchFunction(Invoice(),pdf) )
				#print "Invoice:",obj.num,"PO:",obj.po,"JOB:",obj.job
				obj.printInvoice()
				continue;
	printToPDF(pdf_name,invoices)

#Orange = Invoice
#Purple = PO
#Yellow = JOB

#When printing to PDF, if previous invoice number matches current invoice number, and no PO, copy over PO
if __name__ == '__main__':
	main()
