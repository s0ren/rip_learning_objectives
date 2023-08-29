import sys
import pdfquery

#read the PDF
# pdf = pdfquery.PDFQuery('customers.pdf')
pdf = pdfquery.PDFQuery(sys.argv[1])
pdf.load(18, 19, 20)

print(pdf.doc.catalog)

#convert the pdf to XML
# pdf.tree.write('customers.xml', pretty_print = True)
pdf.tree.write(sys.argv[2], pretty_print = True)

# for e in pdf.tree:
#     print(e)
