def pdf_to_text(filename):
    from cStringIO import StringIO  
    from pdfminer.converter import LTChar, TextConverter    #<-- changed
    from pdfminer.layout import LAParams
    from pdfminer.pdfparser import PDFDocument, PDFParser
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter

    rsrc = PDFResourceManager()
    outfp = StringIO()
    device = TextConverter(rsrc, outfp, codec="utf-8", laparams=LAParams()) 

    doc = PDFDocument()
    fp = open(filename, 'rb')
    parser = PDFParser(fp)       
    parser.set_document(doc)     
    doc.set_parser(parser)       
    doc.initialize('')

    interpreter = PDFPageInterpreter(rsrc, device)

    print "There are: " + str(len(list(doc.get_pages()))) + " pages"

    for i, page in enumerate(doc.get_pages()):
        outfp.write("START PAGE %d\n" % i)
        if page is not None:
            interpreter.process_page(page)
        outfp.write("END PAGE %d\n" % i)

    device.close()
    fp.close()

    return outfp.getvalue()

if __name__== "__main__":
    text = pdf_to_text("test.pdf")
    print text

