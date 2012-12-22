## {{{ http://code.activestate.com/recipes/523047/ (r1)
import httplib
import urllib
from BeautifulSoup import BeautifulSoup, NavigableString
import re

class GoogleScholarSearch:
    """
    @brief This class searches Google Scholar (http://scholar.google.com)

    Search for articles and publications containing terms of interest.
    
    Usage example:\n
    <tt>
    > from google_search import *\n
    > searcher = GoogleScholarSearch()\n
    > searcher.search(['breast cancer', 'gene'])
    </tt>
    """
    def __init__(self):
        """
        @brief Empty constructor.
        """
        self.SEARCH_HOST = "scholar.google.com"
        self.SEARCH_BASE_URL = "/scholar"

    # Taken from: http://stackoverflow.com/questions/1765848/remove-a-tag-using-beautifulsoup-but-keep-its-contents
    def strip_tags(self, s):
        if isinstance(s, NavigableString):
            return s
        ret = ""
        for c in s.contents:
            if not isinstance(c, NavigableString):
                c = self.strip_tags(c)
            ret += unicode(c)

        return ret
        
    def search(self, terms, limit=10):
        """
        @brief This function searches Google Scholar using the specified terms.
        
        Returns a list of dictionarys. Each
        dictionary contains the information related to the article:
            "URL"       : link to the article/n
            "Title"             : title of the publication/n
            "Authors"   : authors (example: DF Easton, DT Bishop, D Ford)/n
            "JournalYear"   : journal name & year (example: Nature, 2001)/n
            "JournalURL"    : link to the journal main website (example: www.nature.com)/n
            "Abstract"  : abstract of the publication/n
            "NumCited"  : number of times the publication is cited/n
            "Terms"             : list of search terms used in the query/n

        @param terms List of search terms
        @param limit Maximum number of results to be returned (default=10)
        @return List of results, this is the empty list if nothing is found
        """
        params = urllib.urlencode({'q': "+".join(terms), 'num': limit})
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

        url = self.SEARCH_BASE_URL+"?"+params
        conn = httplib.HTTPConnection(self.SEARCH_HOST)
        #conn.request("GET", url, {}, headers)
        conn.request("GET", url, "", headers)
        
        resp = conn.getresponse()        
        
        if resp.status==200:
            html = resp.read()
            results = []

            html = html.decode('ascii', 'ignore')

            
            # Screen-scrape the result to obtain the publication information
            soup = BeautifulSoup(html)
            #print soup.prettify()
            citations = 0
            for record in soup('div', {'class': 'gs_r'}):
                # Get title
                pubTitle = ""
                titlePart = record.first('h3', {'class': 'gs_rt'})
                for part in titlePart.a.contents:
                    pubTitle += str(self.strip_tags(part)) # perhaps consider removing <b> tags?
                # End get title
             
                # Get paper URL
                urlPart = record.first('div', {'class': 'gs_ggs gs_fl'})
                if urlPart is not None:
                    pubURL = urlPart.a['href']
                    # Clean up the URL, make sure it does not contain '\' but '/' instead
                    pubURL = pubURL.replace('\\', '/')
                else:
                    pubURL = "[Empty]"
                # End get paper URL
                

                # Get author
                authorPart = record.first('div', {'class' : 'gs_a'})
                pubAuthors = ""
                for part in authorPart.contents:
                    if "&hellip;" in part:
                        break
                    pubAuthors += self.strip_tags(part)
                # End get author

                stripAuthorPart = self.strip_tags(authorPart)
                num =  stripAuthorPart.count(" - ")
                
                # Assume that the fields are delimited by ' - ', the first entry will be the
                # list of authors, the last entry is the journal URL, anything in between
                # should be the journal year
                idx_start = stripAuthorPart.find(' - ')
                idx_end = stripAuthorPart.rfind(' - ')
                #pubAuthors = stripAuthorPart[:idx_start]
                pubJournalYear = re.search('\d\d\d\d', stripAuthorPart[idx_start + 3:idx_end]).group(0)
                
                pubJournalURL = stripAuthorPart[idx_end + 3:]
                # If (only one ' - ' is found) and (the end bit contains '\d\d\d\d')
                # then the last bit is journal year instead of journal URL
                if pubJournalYear=='' and re.search('\d\d\d\d', pubJournalURL)!=None:
                    pubJournalYear = pubJournalURL
                    pubJournalURL = ''

                # Find Abstract
                # This can potentially fail if all of the abstract can be contained in the space
                # provided such that no '...' is found
                abstractPart = record.first('div', {'class': 'gs_rs'})
                pubAbstract = self.strip_tags(abstractPart)
                
                match = re.search("Cited by ([^<]*)", str(record))
                pubCitation = ''
                if match != None:
                    pubCitation = match.group(1)
                results.append({
                    "URL": pubURL,
                    "Title": pubTitle,
                    "Authors": pubAuthors,
                    "JournalYear": pubJournalYear,
                    "JournalURL" : pubJournalURL,
                    "Abstract": pubAbstract,
                    "NumCited": pubCitation,
                    "Terms": terms
                })
            return results
        else:
            print "ERROR: ",
            print resp.status, resp.reason
            return []

if __name__ == '__main__':
    search = GoogleScholarSearch()
    pubs = search.search(["oren etzioni", "language"])
    for pub in pubs:
        print pub['Title']
        print pub['URL']
        print pub['Authors']
        print pub['JournalYear']
        print pub['JournalURL']
        print pub['Abstract']
        print pub['NumCited']
        print pub['Terms']
        print "======================================"
## end of http://code.activestate.com/recipes/523047/ }}}

