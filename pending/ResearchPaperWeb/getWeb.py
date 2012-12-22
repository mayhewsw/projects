from GoogleScholarSearch import *
import urllib2

from ReferenceExtractor import *

def downloadPaper(url, name):
    u = urllib2.urlopen(url)
    localFile = open('out.pdf', 'w')
    localFile.write(u.read())
    localFile.close()
    return name
    


# Connect to google scholar search
GSS = GoogleScholarSearch()

while(running):
    
    pubs = GSS.search(["oren etzioni", "language"])
    url = pubs[0]['URL']

    name = "etzioni1.pdf"
    downloadPaper(url, name)
    
    paperObj, paperList = getPaperListFromPaper(name)

    # keep track of references
    
    

