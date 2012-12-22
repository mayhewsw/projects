#! /usr/lib/python

from pdftotext import pdf_to_text
from Paper import *

# This will accept the text of an academic paper, parse the references and return them.

def getPaperListFromPaper(paperPDF):
    ''' pass PDF '''
    # find the references.
    # parse out all interesting information
    # return a list of Paper objects
    paperList = []

    paperText = pdf_to_text(paperPDF)
    paperObj = Paper()

    # Make paper object for the paper itself.

    # Then make list of paper objects for all the references.

    # Can assume that papers are error free.
    # Person names will be capitalized
    # Year will be on there.
    
    return paperObj, paperList



    

