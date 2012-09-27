'''
Created on Apr 29, 2012

@author: Zhen Shao
'''
import re
import urllib

class IndexPageParser(object):
    '''
    Parsing an index page.
    '''

    def __init__(self, url, brand, gender):
        '''
        Constructor
        '''
        self._url = url
        self._brand = brand
        self._gender = gender
    
    def GetCategoryUrls(self):
        urls = {}
        webpage = urllib.urlopen(self._url)
        concerned_area = False
        shortPromo_area = False
        for line in webpage:
            if not concerned_area:
                if re.search('<a href="(.*)">Clearance</a>', line):
                    concerned_area = True
            else:
                if re.search('category\-content', line):
                    break
                m = re.search('<a href="(.*)">(.*)</a>', line)
                if m:
                    urls[(self._brand, self._gender, m.group(2))] = m.group(1)
            if not shortPromo_area:
                if re.search('shortPromo', line):
                    shortPromo_area = True
            else:
                promo = line.strip();
                shortPromo_area = False
        return urls, promo
