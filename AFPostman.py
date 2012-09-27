'''
Created on Apr 29, 2012

@author: Zhen Shao
'''
import smtplib
import datetime
from email.mime.text import MIMEText

EMAIL_TEMPLATE = """
<html>
  <head></head>
  <body>
  %s
  </body>
</html>
"""

EMAIL_ACCOUNT = 'af.checker@gmail.com'
EMAIL_PWD = '29282317'
ALERT_FILES = {'data/af_women_alerts': 'AF WOMEN', 
               'data/af_men_alerts': 'AF MEN', 
               'data/hollister_alerts': 'HOLLISTER'}
EMAIL_LIST_FILE = 'data/email_list'

def SendAndCleanAlertList(email_list_file, alert_file, email_title):
    email_list = open(email_list_file, 'r')
    alerts = open(alert_file, 'r')
    alert_content = alerts.read()
    if len(alert_content.strip()) >= 100:
        msg = MIMEText(EMAIL_TEMPLATE % alert_content, 'html')
        now = datetime.datetime.now()
        date_string = '%d/%d' % (now.month, now.day)
        msg['Subject'] = '%s has new items! %s' % (email_title, date_string)
        msg['From'] = EMAIL_ACCOUNT
        msg['To'] = ','.join([line.strip() for line in email_list.readlines() 
                                           if line.strip()])
        print 'Send email to:', msg['To']
        
        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(EMAIL_ACCOUNT, EMAIL_PWD)
        mailServer.sendmail(EMAIL_ACCOUNT, msg['To'].split(','), 
                            msg.as_string())
        mailServer.quit()
        print 'Sent successfully.'
    else:
        print 'Empty new item list, clean alert file.'

    alerts.close()
    
    # Clean the file.
    alerts = open(alert_file, 'w')
    alerts.write('')
    alerts.close()

if __name__ == '__main__':
    for alert_file in ALERT_FILES:
        SendAndCleanAlertList(EMAIL_LIST_FILE, 
                              alert_file, ALERT_FILES[alert_file])
