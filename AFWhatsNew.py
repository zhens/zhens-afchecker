'''
Created on Apr 29, 2012

@author: Zhen Shao
'''

class AFWhatsNew(object):
    '''
    Compare two runs and find out the modifications.
    '''


    def __init__(self, items_old, items_new):
        '''
        Constructor
        '''
        self._items_old = items_old
        self._items_new = items_new
        
    def WhatsNew(self, 
                 brands = [],          # Only choose these brands
                 genders = [],         # Only choose these genders
                 categories = [],      # Only choose these categories
                 items = [],           # Only choose these items
                 colors = [],          # Only choose these colors
                 sizes = [],           # Only choose these sizes
                 price_bound = 10000,  # Only choose price < a
                 discount = 0):        # Only choose discount > a% off
        new_items = set()
        for brand, gender, category, item in self._items_new:
            if brands and brand not in brands: continue
            if genders and gender not in genders: continue
            if categories and category not in categories: continue
            if items and item not in items: continue
            
            if (brand, gender, category, item) not in self._items_old:
                # This a new coming item.
                item_data = self._items_new[(brand, gender, category, item)]
                
                # Kill that is too expensive.
                offer_price = item_data['OfferPrice']
                if offer_price > price_bound: continue
                
                # Kill that is no discount.
                list_price = item_data['ListPrice']
                if offer_price / list_price > (1-discount/100.0): continue
                
                detail = item_data['Details']
                for color_seq in detail:
                    if not color_seq: continue
                    # Kill that has no good color.
                    if colors and color_seq['name'] not in colors: continue
                    for size in color_seq['items']:
                        # Kill that has no good size.
                        if sizes and size['size'] not in sizes: continue
                        # Kill that this size has sold out.
                        if size['soldOut'] == 'true': continue
                        # Finally we find one.
                        new_items.add((brand, gender, category, item))
        return new_items