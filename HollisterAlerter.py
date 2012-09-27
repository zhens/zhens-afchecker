'''
Created on Apr 29, 2012

@author: Zhen Shao
'''
import datetime
import os
import pickle
import sys

import AFWhatsNew
import ItemShow

ALERT_FILE = 'data/hollister_alerts'

def LoadItemListFile(filename):
    print 'Load file %s' % filename
    FILE = open(filename, 'r')
    file_content = pickle.load(FILE)
    return file_content['item'], file_content['promo']


def AppendAlertToFile(alert, filename):
    print 'Alert cached to file: %s' % filename
    FILE = open(filename, 'a')
    FILE.write(alert)

if __name__ == '__main__':
    latest_data_file = ''
    second_latest_data_file = ''
    for filename in sorted(os.listdir('data')):
        if filename[0:4] == 'data':
            second_latest_data_file = latest_data_file
            latest_data_file = filename
            
    timestamp = float(latest_data_file[5:])
    time_string = str(datetime.datetime.fromtimestamp(timestamp))
    items_new, promo = LoadItemListFile(os.path.join('data', latest_data_file))
    items_old, _ = LoadItemListFile(os.path.join('data', second_latest_data_file))
    
    AppendAlertToFile('<h2>' + promo['HOLLISTER'] + '</h2>', ALERT_FILE)
    
    new_item_checker = AFWhatsNew.AFWhatsNew(items_old, items_new)
    new_item_index = new_item_checker.WhatsNew(brands=['HOLLISTER'], discount=50)
    if not new_item_index: sys.exit() 
    alerts = '<h2 style="color: olive">Updated at %s (NY)</h2>' % time_string
    for brand, gender, category, item_name in new_item_index:
        item_show = ItemShow.ItemShow(
            brand, gender, category, items_new[(brand, gender, category, item_name)])
        alerts += item_show.GenerateHTML()
    
    AppendAlertToFile(alerts, ALERT_FILE)
