"""Takes one "CIK" (or ticker) as a required argument. Takes one OPTIONAL "recent" argument to fetch most recent document (1 for most recent, 2 for second most recent, etc.)
Run using the command as an example (fetches 2nd most recent document for ticker <CIK>):
python app.py -t="<CIK>" -r=2
"""
import requests
import os
import sys
import argparse
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import csv
from lxml.html.soupparser import fromstring

def fetchXml(links, recent):
    url = 'https://www.sec.gov' + links[recent-1]
    try:
        res = requests.get(url)
    except requests.exceptions.RequestException as e:
        print("Could not reach SEC site")
        sys.exit(1)
     # store the result html in variable to parse
    html_doc = res.content
    # use BeautifulSoup as parser
    soup = BeautifulSoup(html_doc, 'html.parser')
    div = soup.find_all(match_class(["tableFile"]))
    # get table rows
    table_rows = div[0].find_all('tr')
    allDocuments = {}
    for tr in table_rows:
        td = tr.find_all('td')
        if len(td) > 0:
            documentType = (td[3].text)
            link = (td[2].find('a')['href'])
            allDocuments.update({documentType:link})
            # TODO: check why not returning all rows
    infoTables =  {k:v for k,v in allDocuments.items() if 'INFORMATION TABLE' in k}
    if len(infoTables) == 0:
        print("Could not find INFORMATION TABLE for this ticker")
        sys.exit(1)
    return infoTables['INFORMATION TABLE']

def goToEdgar(ticker):
    # params for query string
    getcompany = 'getcompany'
    tickerType = '13f'
    count = 100
    url = 'https://www.sec.gov/cgi-bin/browse-edgar?action={getcompany}&CIK={ticker}&type={tickerType}&count={count}'.format(getcompany=getcompany,ticker=ticker, tickerType=tickerType, count=count)
    
    # make the request to EDGAR site
    try:
        res = requests.get(url)
    except requests.exceptions.RequestException as e:
        print("Could not reach EDGAR site")
        sys.exit(1)
    
    # store the result html in variable to parse
    html_doc = res.content
    # use BeautifulSoup as parser
    soup = BeautifulSoup(html_doc, 'html.parser')
    # target the tableFile2 class
    div = soup.find_all(match_class(["tableFile2"]))
    # get table rows
    table_rows = div[0].find_all('tr')
    # initialize list of href
    listOfLinks = []
    # find the <a href> to documents
    for tr in table_rows:
        td = tr.find_all('td')
        if len(td) > 0:
            listOfLinks.append(td[1].find('a')['href'])
    return listOfLinks

def createCSV(infoLink, ticker):
    url = 'https://www.sec.gov' + infoLink
    try:
        res = requests.get(url)
    except requests.exceptions.RequestException as e:
        print("Could not reach SEC site")
        sys.exit(1)

    root = ET.fromstring(res.content)
    
    # open a file for writing
    file_name = '{}_data.csv'.format(ticker)
    with open(file_name, mode='w') as ticker_data:
        csvwriter = csv.writer(ticker_data)
        headers = ['Name of Issuer', 'Title of Class', 'Cusip', 'Value', 'SSH Prnamt', 'SSH Prnamt Type', 'Put Call' , 'Investment Discretion', 'Other Manager', 'Voting Sole', 'Voting Shared', 'Voting None']
        csvwriter.writerow(headers)

        for member in root:
            fund = []
            if len(member) == 7:
                fund.append(member[0].text)
                fund.append(member[1].text)
                fund.append(member[2].text)
                fund.append(member[3].text)
                fund.append(member[4][0].text)
                fund.append(member[4][1].text)
                fund.append("n/a")
                fund.append(member[5].text)
                fund.append("n/a")
                fund.append(member[6][0].text)
                fund.append(member[6][1].text)
                fund.append(member[6][2].text)
                # write row to CSV
                csvwriter.writerow(fund)
            # with OtherManager Object
            elif len(member) == 8:
                fund.append(member[0].text)
                fund.append(member[1].text)
                fund.append(member[2].text)
                fund.append(member[3].text)
                fund.append(member[4][0].text)
                fund.append(member[4][1].text)
                fund.append("n/a")
                fund.append(member[5].text)
                fund.append(member[6].text)
                fund.append(member[7][0].text)
                fund.append(member[7][1].text)
                fund.append(member[7][2].text)
                # write row to CSV
                csvwriter.writerow(fund)
            # with PUT and OtherManager Object    
            elif len(member) == 9:
                fund.append(member[0].text)
                fund.append(member[1].text)
                fund.append(member[2].text)
                fund.append(member[3].text)
                fund.append(member[4][0].text)
                fund.append(member[4][1].text)
                fund.append(member[5].text)
                fund.append(member[6].text)
                fund.append(member[7].text)
                fund.append(member[8][0].text)
                fund.append(member[8][1].text)
                fund.append(member[8][2].text)
                # write row to CSV
                csvwriter.writerow(fund)
        ticker_data.close() 
        
    return True

def match_class(target):                                                        
    def do_match(tag):                                                          
        classes = tag.get('class', [])                                          
        return all(c in classes for c in target)                                
    return do_match 

def main():
    parser = argparse.ArgumentParser(
        description="""
        Takes one argument of a CIK (or ticker).
        This script will then search the EDGAR site for information on this mutual fund
        """)
    parser.add_argument(
        '--ticker',
        '-t',
        type=str,
        required=True,
        help="ticker of mutual fund that you would like to explore")
    parser.add_argument(
        '--recent',
        '-r',
        type=int,
        required=False,
        default=1,
        help="how recent the report is (newest=1, 2nd newest=2, etc). Default is 1")
    args = parser.parse_args()
    
    # store ticker in variable
    ticker = args.ticker
    recent = args.recent

    # query Edgar site with ticker
    listOfLinks = goToEdgar(ticker)

    # check if recent is "recent" enough haha
    if recent > len(listOfLinks):
        print("Accessing document that is not recent enough")
        sys.exit(1)

    # fetch the xml
    infoLink = fetchXml(listOfLinks,recent)

    # create CSV file from XML
    success = createCSV(infoLink, ticker)

if __name__ == "__main__":
    main()
