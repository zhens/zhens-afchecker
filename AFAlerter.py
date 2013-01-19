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

ALERT_CONFIGS = (
  ('AF', ['WOMEN'], 'data/af_women_alerts'),
  ('AF', ['MEN'], 'data/af_men_alerts'),
  ('HOLLISTER', ['WOMEN', 'MEN'], 'data/hollister_alerts')
)

def LoadItemListFile(filename):
    print 'Load file %s' % filename
    FILE = open(filename, 'r')
    file_content = pickle.load(FILE)
    return file_content['item'], file_content['promo']


def AppendAlertToFile(alert, filename):
    print 'Alert cached to file: %s' % filename
    FILE = open(filename, 'a')
    FILE.write(alert)

def GenerateAlert(brand, gender_selector, alert_file):
    latest_data_file = ''
    second_latest_data_file = ''
    for filename in sorted(os.listdir('data')):
        if filename[0:4] == 'data':
            second_latest_data_file = latest_data_file
            latest_data_file = filename
            
    timestamp = float(latest_data_file[5:])
    time_string = str(datetime.datetime.fromtimestamp(timestamp))
    items_new, promo_new = LoadItemListFile(os.path.join('data', latest_data_file))
    items_old, promo_old = LoadItemListFile(os.path.join('data', second_latest_data_file))
    
    if promo_new != promo_old:
        AppendAlertToFile('<h2>' + promo_new[brand] + '</h2>', alert_file)

    new_item_checker = AFWhatsNew.AFWhatsNew(items_old, items_new)
    new_item_index = new_item_checker.WhatsNew(brands=[brand],
                                               genders=gender_selector,
                                               discount=50)

    if not new_item_index: return

    alerts = '<h2>Updated at %s (NY)</h2>' % time_string
    for brand, gender, category, item_name in new_item_index:
        item_show = ItemShow.ItemShow(
            brand, gender, category, items_new[(brand, gender, category, item_name)])
        alerts += item_show.GenerateHTML()
    
    AppendAlertToFile(alerts, alert_file)


if __name__ == '__main__':
    for brand, genders, filename in ALERT_CONFIGS:
        print '\nGenerating alert for ', brand, genders
        GenerateAlert(brand, genders, filename)
