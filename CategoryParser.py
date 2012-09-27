'''
Created on Apr 29, 2012

@author: Zhen Shao
'''
import re
import urllib
import HTMLParser

URL_TEMPLATE = {'AF':'http://www.abercrombie.com%s',
                'HOLLISTER': 'http://www.hollisterco.com%s'}

class CategoryParser(object):
    '''
    Parse a category listing page.
    '''
    def __init__(self, brand, gender, category, url):
        '''
        Constructor
        '''
        self._url = HTMLParser.HTMLParser().unescape(URL_TEMPLATE[brand] % url)
        self._brand = brand
        self._gender = gender
        self._category = category
        print 'Loading Category %s, %s, %s' % (brand, gender, category)
    
    def GetItemList(self):
        item_list = {}
        webpage = urllib.urlopen(self._url)
        expected = 'ProductWrap'
        for line in webpage:
            if expected == 'ProductWrap':
                if re.search('product\-wrap', line):
                    item = {}
                    expected = 'Image'
            elif expected == 'Image':
                m = re.search('<img.*src="(.*)"/>', line)
                if m:
                    item['Image'] = m.group(1)
                    expected = 'NameWrapper'
            elif expected == 'NameWrapper':
                if re.search('<span class="name">', line):
                    expected = 'Name'
            elif expected == 'Name':
                m = re.search('<a href="(.*)">(.*)</a>', line)
                if m:
                    item['Name'] = m.group(2)
                    item['Link'] = m.group(1)
                    expected = 'Desc'
            elif expected == 'Desc':
                m = re.search('<span class="desc">(.*)</span>', line)
                if m:
                    item['Desc'] = m.group(1)
                    expected = 'ListPrice'
            elif expected == 'ListPrice':
                m = re.search('<span class="list-price">\$([0-9]*).*</span>', line)
                if m:
                    item['ListPrice'] = float(m.group(1))
                    expected = 'OfferPrice' 
            elif expected == 'OfferPrice':
                m = re.search('<span class="offer-price">\$([0-9]*\.?[0-9]+).*', line)
                if m:
                    item['OfferPrice'] = float(m.group(1))
                    expected = 'Swatches'
                    item['Swatches'] = []
            elif expected == 'Swatches':
                if re.search('product\-wrap', line):
                    expected = 'ProductWrap'
                    item_list[(self._brand, 
                               self._gender, 
                               self._category, 
                               item['Name'])] = item
                    continue
                if re.search('footer\-wrap', line):
                    expected = 'End'
                    item_list[(self._brand, 
                               self._gender, 
                               self._category, 
                               item['Name'])] = item
                    break
                m = re.search('<span>(.*)</span>', line)
                if m:
                    item['Swatches'].append(m.group(1))
                    expected = 'Swatches'
            else:
                break
        return item_list