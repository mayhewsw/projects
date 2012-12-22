#!/usr/bin/env python

import feedparser
import re
import datetime
from urllib import urlopen
import smtplib
import string
from email.mime.text import MIMEText
import os

filedir = os.getcwd()

aptopheadlines = "http://hosted2.ap.org/atom/APDEFAULT/3d281c11a96b4ad082fe88aa0db04305"
apusnat = "http://hosted2.ap.org/atom/APDEFAULT/386c25518f464186bf7a2ac026580ce7"
apworld = "http://hosted2.ap.org/atom/APDEFAULT/cae69a7523db45408eeb2b3a98c0c9c5"
appolitics = "http://hosted2.ap.org/atom/APDEFAULT/89ae8247abe8493fae24405546e9a1aa"
apbusiness = "http://hosted2.ap.org/atom/APDEFAULT/f70471f764144b2fab526d39972d37b3"
aptech = "http://hosted2.ap.org/atom/APDEFAULT/495d344a0d10421e9baa8ee77029cfbd"
apscience = "http://hosted2.ap.org/atom/APDEFAULT/b2f0ca3a594644ee9e50a8ec4ce2d6de"

yahoo_ind_oilgas = "http://finance.yahoo.com/rss/IndependentOilGas"
yahoo_major_oilgas = "http://finance.yahoo.com/rss/MajorIntegratedOilGas"
yahoo_oilgas_exp = "http://finance.yahoo.com/rss/OilGasDrillingExploration"
yahoo_oilgas_equip = "http://finance.yahoo.com/rss/OilGasEquipmentServices"
yahoo_oilgas_pipe ="http://finance.yahoo.com/rss/OilGasPipelines"
yahoo_oilgas_refine = "http://finance.yahoo.com/rss/OilGasRefiningMarketing"

# eia feeds from http://205.254.135.7/tools/rssfeeds/
#Today in energy http://205.254.135.7/rss/todayinenergy.xml
# What's new 'http://205.254.135.7/about/new/WNtest3.cfm
# Press releases http://205.254.135.7/rss/press_rss.xml
#Energy in brief http://205.254.135.7/energy_in_brief/eibinfo.cfm
# Gas and diesel update http://205.254.135.7/petroleum/gasdiesel/includes/gas_diesel_rss.xml
# This week in petroleum http://205.254.135.7/oog/info/twip/week_in_petroleum_rss.xml

# Nymex futures prices
#http://www.eia.gov/dnav/pet/pet_pri_fut_s1_d.htm

# from http://www.cmegroup.com/rss/index.html
# http://feeds.feedburner.com/EnergyMarketCommentary
# http://feeds.feedburner.com/EconomicEventsEnergy

# From http://www.ft.com/intl/cms/s/48ffafb6-5057-11da-bbd7-0000779e2340.htm?segid=70124
#http://www.ft.com/rss/companies/oil-gas

# From http://money.cnn.com/services/rss/
#http://rss.cnn.com/rss/money_markets.rss

# Oil price.net
wti_webpage = "http://www.oil-price.net/TABLE2/gen.php?lang=en"
brent_webpage = "http://www.oil-price.net/widgets/brent_crude_price_large/gen.php?lang=en"

gasbuddyfeedTH="http://www.gasbuddy.com/GB_Detailed_RSS.aspx?state=IN&area=Terre+Haute"
gasbuddyfeedIndy="http://www.gasbuddy.com/GB_Detailed_RSS.aspx?state=IN&area=Indianapolis+-+central"
gasbuddyfeedUSA = "http://gasbuddy.com/GB_Generic.aspx"


news_feed_urls = [aptopheadlines, apusnat, apworld, appolitics, apbusiness, aptech, apscience]
gasnews_feed_urls = [yahoo_ind_oilgas, yahoo_major_oilgas, yahoo_oilgas_exp, yahoo_oilgas_equip, yahoo_oilgas_pipe, yahoo_oilgas_refine]
gasbuddy_feed_urls = [ gasbuddyfeedTH, gasbuddyfeedIndy, gasbuddyfeedUSA]


def cleanup_GB_feed(data):
    ''' This is specifically tailored for custom GasBuddy feeds '''
    beg= "&nbsp;"
    end = "</td>"
    p = re.compile(r'&nbsp;\d.\d\d</td>')
    return [float(x.lstrip(beg).rstrip(end)) for x in p.findall(data)]


def get_gas_prices():
    feed = feedparser.parse(gasbuddyfeedTH)
    thprices = cleanup_GB_feed(feed['items'][0]['summary'])
    thaverage = sum(thprices) / len(thprices)

    feed = feedparser.parse(gasbuddyfeedIndy)
    indyprices = cleanup_GB_feed(feed['items'][0]['summary'])
    indyaverage = sum(indyprices) / len(indyprices)

    feed = feedparser.parse(gasbuddyfeedUSA)
    summary = filter(lambda f: "Average" in f['title'], feed['items'])[0]['summary']
    nationaverage =  float(re.findall(r'Today</td><td>\$ \d.\d\d', summary)[0][-4:])

    return thprices, thaverage, indyprices, indyaverage, nationaverage


def get_oil_prices():
    wti_page = urlopen(wti_webpage).read()
    wti_price =  float(re.findall("\$\d+\.\d\d", wti_page)[0].strip('$'))

    brent_page = urlopen(brent_webpage).read()
    brent_price =  float(re.findall("\$\d+\.\d\d", brent_page)[0].strip('$'))

    return wti_price, brent_price


def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def send_email(msg_text):
    # Create a text/plain message
    msg = MIMEText(msg_text)
    
    me = "oil.price.warning@gmail.com"
    you = "swm.mayhew@gmail.com"
    
    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = "Rising Oil Prices"
    msg['From'] = me
    msg['To'] = you
    
    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.starttls()
    s.login("oil.price.warning", "cityslicker")
    
    
    s.sendmail(me, [you], msg.as_string())
        
    s.quit()
    
def makefilename(date):
    return 'gasdata_%d-%d.txt' % (date.month, date.day)

def dump():
    today = datetime.datetime.now()
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    
    print "Creating file..."
    outfile = open(filedir + makefilename(today), 'w')

    allnewsitems = []

    # ==== Reading now
    print "Reading news feeds..."
    for url in news_feed_urls:
        feed = feedparser.parse(url)
        allnewsitems.extend(feed['items'])

    allgasoilnewsitems = []
    print "Reading gas and oil news feeds..."
    for url in gasnews_feed_urls:
        feed = feedparser.parse(url)
        allgasoilnewsitems.extend(feed['items'])

    print "Reading gas buddy feeds..."
    thprices, thaverage, indyprices, indyaverage, nationaverage = get_gas_prices()

    print "Reading oil prices..."
    wti, brent = get_oil_prices()

    # ==== Do comparison
    try:
        yest_file = open(filedir + makefilename(yesterday), 'r')

        # read gas prices and oil prices. If difference is large between today and yesterday, send email
        yest_lines = yest_file.readlines()
        if len(yest_lines) > 0:
            yest_th = float(yest_lines[yest_lines.index("Terre Haute\n")+1])
            yest_ind = float(yest_lines[yest_lines.index("Indianapolis\n")+1])
            yest_USav = float(yest_lines[yest_lines.index("USA Average\n")+1])
            yest_wti = float(yest_lines[yest_lines.index("WTI Prices\n")+1])
            yest_brent = float(yest_lines[yest_lines.index("Brent Prices\n")+1])

            #print "TH ", thaverage - yest_th
            #print "IND ", indyaverage - yest_ind
            #print "US ", nationaverage - yest_USav
            #print "WTI ", wti - yest_wti
            #print "Brent ", brent - yest_brent

            thdiff = thaverage - yest_th
            inddiff =  indyaverage - yest_ind
            usdiff = nationaverage - yest_USav
            wtidiff = wti - yest_wti
            brentdiff = brent - yest_brent

            send = False
            msg = "Gas/Oil price warning!\n"
            if abs(thdiff) > 0.1 or abs(inddiff) > 0.1 or abs(usdiff) > 0.1:
                send = True
                msg += "Terre Haute diff: $" + str(thdiff) + "\n"
                msg += "Indianapolis diff: $" + str(inddiff) + "\n"
                msg += "United States diff: $" + str(usdiff) + "\n"

            if abs(wtidiff) > 4 or abs(brentdiff) > 4:
                send = True
                msg += "WTI: $" + str(wtidiff) + "\n"
                msg += "Brent: $" + str(brentdiff) + "\n"

            if send:
                send_email(msg)
            
    except IOError:
        print "Error opening file: " + makefilename(yesterday)
    else:
        yest_file.close()
            
    
        
    # ==== Dumping now
    print "Writing to file..."
    outfile.write("This file created: " + str(today.strftime("%B-%d %H:%M")) + "\n\n")
    outfile.write("==== NEWS ITEMS ====\n")
    for f in allnewsitems:
        outfile.write(f["title"].encode('ascii', 'ignore') + "\n")
        outfile.write(remove_html_tags(f["summary"]).encode('ascii', 'ignore') + "\n\n")

    outfile.write("==== GAS AND OIL NEWS ITEMS ====\n")
    for f in allgasoilnewsitems:
        outfile.write(f["title"].encode('ascii', 'ignore') + "\n")
        outfile.write(remove_html_tags(f["summary"]).encode('ascii', 'ignore') + "\n\n")

    outfile.write("==== GAS PRICES ====\n")
    outfile.write("Terre Haute\n" + str(thaverage) + "\n" + str(thprices) + "\n\n")

    outfile.write("Indianapolis\n" + str(indyaverage) + "\n" + str(indyprices) + "\n\n")

    outfile.write("USA Average\n" + str(nationaverage) + "\n")

    outfile.write("\n==== OIL PRICES ====\n")
    outfile.write("WTI Prices\n" + str(wti) + "\n\n")
    outfile.write("Brent Prices\n" + str(brent) + "\n\n")

    outfile.close()


if __name__ == "__main__":
    dump()
    #send_email()
