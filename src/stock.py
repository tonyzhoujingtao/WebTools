import urllib
import re


def get_price_from_yahoo(symbols):
    symbol_to_price = {}
    
    for symbol in symbols:
        url = 'http://finance.yahoo.com/q?s=' + symbol + '%2C+&ql=1'
        html_file = urllib.urlopen(url)
        html_text = html_file.read()
        html_file.close()
        regexpr = '<span id="yfs_l84_' + symbol + '">(.+?)</span>'
        pattern = re.compile(regexpr)
        price = re.findall(pattern, html_text)
        symbol_to_price[symbol] = price
        
    return symbol_to_price


def main():
    symbols = ["aapl", "msft", "ibm"]
    print get_price_from_yahoo(symbols)

if __name__ == "__main__":
    main()    
    

