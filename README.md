# Description

Python script that parses fund holdings pulled from EDGAR, given a ticker or CIK, and writes a .csv file from them.

# Output

CSV file called `<CIK>_data.csv` in project folder that includes parsed results 

# Setup

1. Download `virtualenv` (if not already downloaded) using `pip install virtualenv` or `brew install virtualenv`
2. In your terminal, make your current directory this directory `edgar`
3. Run `virtualenv venv --python=python3`
4. Run `source venv/bin/activate`
5. Run `pip install -r requirements.txt`

You should now have all dependencies installed. Feel free to run the script or run `deactivate` to turn off the virtual environment.

# How to Execute Script

1. Run `source venv/bin/activate`
2. This script takes one `CIK` (or ticker) as a required argument. It also takes one OPTIONAL `recent` argument to fetch the `nth` recent document (1 for most recent, 2 for second most recent, etc.) Most recent (1) is the default if no `recent` argument is applied. 
3. Run `python app.py -t=0001756111 -r=2` as an example (fetches 2nd most recent document for ticker `0001756111`)

# Testing

Tested using the following tickers:

Gates Foundation | 0001166559 <br/>
CALEDONIA FUND LTD. | 0001037766<br/>
Peak6 Investments LLC | 0001756111 <br/>
Kemnay Advisory Services Inc. | 0001555283 <br/>
HHR Asset Management, LLC | 0001397545 <br/>
Benefit Street Partners LLC | 0001543160 <br/>
Okumus Fund Management Ltd. | 0001496147 <br/>
PROSHARE ADVISORS LLC | 0001357955 <br/>
TOSCAFUND ASSET MANAGEMENT LLP | 0001439289 <br/>
Black Rock | 0001086364 <br/>

# Notes and Future Work
1. Implement pagination to accomadate for multiple pages on EDGAR results page. `Count` is currently set at 100, and no ticker under the "Testing" section above returns more than 100 `13F` type documents so this is not a concern at the moment, but maybe worthwhile to implement for the future.
2. Last ticker in section above (`Black Rock | 0001086364`) did not return any `13F` type `INFORMATION TABLE` documents.
3. Current implementation to accomodate for change in format in the `INFORMATION TABLE` XML document is quite "hacky". Future work would be to make something more dynamic when faced with varying formats. A possible implmentation would be to check which investment object in the XML object has the most attributes and use that object's titles as the template for the whole CSV output. 
3. To get previous reports for a ticker I have added the `recent` flag in the arguments list (See the "How to Execute Script" section). 
4. Future work might be to implement some unit testing for this script using Python's `uniittest` framework. Although this might be difficult as this script is not class-based and its output is a CSV file (correct me if I am wrong on this assumption). 

# Created By

Brandon Ling<br/>
brandonling27@gmail.com<br/>
New York, NY
  
