'''
Created on Apr 29, 2012

@author: Zhen Shao
'''

import os
import time

if __name__ == '__main__':
    for filename in sorted(os.listdir('data')):
        if filename[0:4] == 'data':
            timestamp = filename[5:]
            time_outdate = '%d' % (time.time() - 3600 * 2)
            if timestamp < time_outdate:
                print 'File %s is older than 2 hours, delete it.' % filename
                os.remove(os.path.join('data', filename))
