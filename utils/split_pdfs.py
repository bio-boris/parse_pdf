import sys
from pyPdf import PdfFileWriter, PdfFileReader


document = sys.argv[1];
inputpdf = PdfFileReader(file(document, "rb"))


filename = 100;
output = PdfFileWriter()

for i in xrange(inputpdf.numPages):
	output.addPage(inputpdf.getPage(i))
	if(i > filename):
		outputStream = file(document + "_" + str(filename) + ".pdf", "wb")
		output.write(outputStream)
		outputStream.close()
		output = PdfFileWriter()
		filename +=100;
