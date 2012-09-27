'''
Created on Apr 29, 2012

@author: Zhen Shao
'''
import json
import urllib
import HTMLParser

URL_TEMPLATE = {'AF': 
                    'http://www.abercrombie.com/webapp/wcs/stores/servlet/%s',
                'HOLLISTER':
                    'http://www.hollisterco.com/webapp/wcs/stores/servlet/%s'}

class ItemPageParser(object):
    '''
    Parsing an item page.
    '''
    def __init__(self, brand, url, seq):
        '''
        Constructor
        '''
        self._url_tpl = HTMLParser.HTMLParser().unescape(
            URL_TEMPLATE[brand] % url.replace('ProductDisplay', 'GetColorJSON')
            + '&seq=%02d')
        self._seq = seq
        
    def GetItemDetail(self):
        item_seq = []
        for i in range(1, self._seq + 1):
            item_seq.append(
                json.loads(urllib.urlopen(self._url_tpl % i).read()))
        return item_seq

