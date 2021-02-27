import concurrent.futures
from configparser import ConfigParser
import bot_flipkart,bot_amazon
import re

config = ConfigParser()
config.read('config.ini')

threads = []
lst = []

email_checker='.*'
upi_checker='.*'

def get_details(site):
    if 'flipkart' in site:
        user = config['accounts']['flipkart_username']
        pwd = config['accounts']['flipkart_password']
    elif 'amazon' in site:
        user = config['accounts']['amazon_username']
        pwd = config['accounts']['amazon_password']

    if not user or not pwd:
        print('email id or password is blank')
        return False,None
    elif not re.search(email_checker,user):
        print('email format is wrong...check config file')
        return False,None

    upi = config['accounts']['UPI-id']
    if not re.search(upi_checker,upi):
        print('wrong upi format')
        return False,None
    
    telegram_api = config['telegram']['bot_api']
    telegram_chat_id = config['telegram']['chat_group_id']
    
    try:
        retry_count = int(config['counters']['max_number_of_retries'])
        time = float(config['counters']['max_wait_for_each_retry'])
    except:
        print('wrong format for counters in config file, please enter whole numbers')
        return False,None

    return True,user,pwd,upi,telegram_api,telegram_chat_id,time,retry_count

def get_browser():
    from winreg import HKEY_CURRENT_USER, OpenKey, QueryValueEx
    with OpenKey(HKEY_CURRENT_USER,"SOFTWARE\\Microsoft\\Windows\\Shell\\Associations\\URLAssociations\\https\\UserChoice") as key:
        (wb,type) = QueryValueEx(key,'ProgId')
        key.Close()
    if 'Firefox' in wb:
        return 'Firefox'
    elif 'Chrome' in wb:
        return 'Chrome'
    else:
        return 'Edge'

try:
    all_item_links = open("urls.txt",'r')
except:
    print('no such file found')
#with concurrent.futures.ThreadPoolExecutor() as executor:
id=0

browser=get_browser()

for url in all_item_links:
    url=url.strip()
    if 'flipkart.' in url:
        id+=1
        lst=get_details('flipkart.com')
        if lst[0]:
            obj=bot_flipkart.flipkart(lst[1],lst[2],lst[3],lst[4],lst[5],lst[6],lst[7],url,'url '+str(id),browser)
    elif 'amazon.' in url:
        id+=1
        lst=get_details('amazon.com')
        if lst[0]:
            obj=bot_amazon.amazon(lst[1],lst[2],lst[3],lst[4],lst[5],lst[6],lst[7],url,'url '+str(id),browser)
    else:
        print('cannot process for this site yet')

    obj.run()

all_item_links.close()