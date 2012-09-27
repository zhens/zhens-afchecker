'''
Created on Apr 29, 2012

@author: Zhen Shao
'''
import IndexPageParser
import CategoryParser 
import ItemPageParser

import pickle
import time

AF_MEN_INDEX = ('http://www.abercrombie.com/webapp/wcs/stores/servlet/'
                'CategoryDisplay?catalogId=10901&storeId=10051&langId=-1'
                '&topCategoryId=12202&categoryId=12245&parentCategoryId=12204')

AF_WOMEN_INDEX = ('http://www.abercrombie.com/webapp/wcs/stores/servlet/'
                  'CategoryDisplay?catalogId=10901&storeId=10051&langId=-1'
                  '&topCategoryId=12203&categoryId=12699&parentCategoryId='
                  '12205')

HOLLISTER_MEN_INDEX = ('http://www.hollisterco.com/webapp/wcs/stores/servlet/'
                       'CategoryDisplay?catalogId=10201&storeId=10251&langId=-1'
                       '&topCategoryId=12551&categoryId=12636&parentCategoryId='
                       '12634')

HOLLISTER_WOMEN_INDEX = ('http://www.hollisterco.com/webapp/wcs/stores/servlet/'
                         'CategoryDisplay?catalogId=10201&storeId=10251&'
                         'langId=-1&topCategoryId=12552&categoryId=92708&'
                         'parentCategoryId=12635')


def SaveItemListToFile(items, promos, filename):
    print 'Save to file: %s' % filename
    FILE = open(filename, 'w')
    pickle.dump({'item': items, 'promo': promos}, FILE)
    print 'Saved successfully.'


def UpdateCategoryData(category_urls):
    items = {}
    for brand, gender, category in sorted(category_urls):
        category_parser = CategoryParser.CategoryParser(
            brand, gender, category, category_urls[(brand, gender, category)])
        item_list = category_parser.GetItemList()
        print 'Found items: ', len(item_list)
        items.update(item_list)
    return items

def UpdateItemData(items):
    for brand, gender, category, name in sorted(items):
        item_parser = ItemPageParser.ItemPageParser(
            brand,
            items[(brand, gender, category, name)]['Link'],
            len(items[(brand, gender, category, name)]['Swatches']))
        items[(brand, gender, category, name)]['Details'] = (
            item_parser.GetItemDetail())
        print 'Get Item Detail for %s, %s, %s, %s.' % (brand, 
                                                       gender, 
                                                       category, 
                                                       name)

if __name__ == '__main__':
    index_parser = IndexPageParser.IndexPageParser(AF_MEN_INDEX, 
                                                             'AF', 'MEN')
    url_list, AF_promo = index_parser.GetCategoryUrls()
    
    index_parser = IndexPageParser.IndexPageParser(AF_WOMEN_INDEX, 
                                                      'AF', 'WOMEN')

    new_url_list, _ = index_parser.GetCategoryUrls()
    url_list.update(new_url_list)

    index_parser = IndexPageParser.IndexPageParser(
        HOLLISTER_MEN_INDEX, 'HOLLISTER', 'MEN')

    new_url_list, HOLLISTER_promo = index_parser.GetCategoryUrls()
    url_list.update(new_url_list)

    index_parser = IndexPageParser.IndexPageParser(HOLLISTER_WOMEN_INDEX, 
                                                   'HOLLISTER', 'WOMEN')
    
    new_url_list, _ = index_parser.GetCategoryUrls()
    url_list.update(new_url_list)

    print AF_promo
    print HOLLISTER_promo

    items = UpdateCategoryData(url_list)
    
    UpdateItemData(items)
    
    SaveItemListToFile(items, {'AF': AF_promo, 
                               'HOLLISTER': HOLLISTER_promo},
                       'data/data.%d' % time.time())
