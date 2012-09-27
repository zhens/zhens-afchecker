'''
Created on Apr 29, 2012

@author: Zhen Shao
'''

import re
import HTMLParser
import ItemPageParser

class ItemShow(object):
    '''
    Generate HTML for a certain item.
    '''


    def __init__(self, brand, gender, category, item):
        '''
        Constructor
        '''
        self._brand = brand
        self._gender = gender
        self._category = category
        self._item = item
        
        
    def GenerateHTML(self):
            
        def escape(content):
            return HTMLParser.HTMLParser().escape(content)
        
        def div(content='', style=''):
            return '<div style="%s">%s</div>' % (style, content)
        
        def img(url=''):
            return '<img src="http:%s" width="360"/>' % url
        
        def a(url='', content=''):
            return '<a href="%s">%s</a>' % (url, content)
        
        def br():
            return '<br/>'
        
        def h2(content=''):
            return '<h2>%s</h2>' % content
        
        ITEM_TEMPLATE = """
        %(item_name)s
        %(image)s
        %(price)s
        %(colorsize)s
        """
        
        parts = {}
        parts['item_name'] = h2(a(
            ItemPageParser.URL_TEMPLATE[self._brand] % self._item['Link'],
            '%s - %s - %s - %s' % (self._brand,
                                   self._gender, 
                                   self._category, 
                                   self._item['Name'])))
        m = re.search('(.*)\$.*\$', self._item['Image'])
        parts['image'] = img(m.group(1))
        
        parts['price'] = div('$%.2f -> $%.2f, %d Percent OFF' %
            (self._item['ListPrice'],
             self._item['OfferPrice'],
             100 * (1 - self._item['OfferPrice'] / self._item['ListPrice'])))
        
        sizes = {}
        for color in self._item['Details']:
            if not color: continue
            sizes[color['name']] = []
            for size in color['items']:
                if not size: continue
                if size['soldOut'] == 'true': continue
                sizes[color['name']].append(size['size'])
         
        color_string = '<ul>'
        for color in sizes:
            color_string += '<li>Color: %s  --  Size:' % color
            for size in sizes[color]:
                color_string += size + ' '
            color_string += '</li>'
        color_string += '</ul>'
        
        parts['colorsize'] = color_string
        
        return div(ITEM_TEMPLATE % parts, 
                   'border: 5px silver solid; margin-bottom: 30px; '
                   'width: 380px; padding: 20px; overflow: hidden;')
                        
