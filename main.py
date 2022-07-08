from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account
import requests
import pandas as pd
from time import sleep
from lxml import html
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class updater:
    SCOPES = None
    creds = None
    sheet_id_target = None
    sheet = None


    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        SERVICE_ACCOUNT_FILE = 'endless-fire.json'

        self.creds = None
        self.creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)

        self.sheet_id_target = '1HHGVnpIxfGZz-icG9Uom-iWUsCFUlMMh_Kw5jIIktpw'
        service = build('sheets', 'v4', credentials=self.creds)
        self.sheet = service.spreadsheets()
 
    def torob_data(self, url):
        with requests.Session() as s:
            header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',}
            req = s.get(url, headers=header)

#         req = requests.get(url, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'})
        page_info = req.text
        xpath = html.fromstring(page_info)
        # resp = xpath.xpath("//div[@class='jsx-1883554428 purchase-info seller-element']/a/text()")
        prices = xpath.xpath("//div[@class='jsx-375537398 purchase-info seller-element']/a/text()")
        sellers = xpath.xpath("//div[@class='css-1nd33m6']/a/text()")
        price_ls = []
        try:
            for price in prices:
                if price != 'ناموجود':
                    p1 = int(price.replace('٫','').replace('تومان', ''))
                    p2 = convert_numbers.hindi_to_english(p1)
                    price_ls.append(int(p2))
        except ValueError:
            pass
        if 'ابزاربرند' in sellers:
            ind = sellers.index('ابزاربرند')
            if len(price_ls) > ind:
                del price_ls[ind]
            del sellers[ind]
        return {'sellers': sellers, 'price list': price_ls}
    
    def final_price(self, buy_price, price_list):
        buy_price = int(buy_price)
        for i in range(len(price_list)):
            if buy_price < price_list[0]:
                plc = 1
            elif buy_price >= price_list[-1]:
                plc = len(price_list) + 1
            elif price_list[i] <= buy_price < price_list[i + 1]:
                plc = i + 2
            
        if plc <= len(price_list):
            return price_list[plc - 1] - 1000
        else:
            return buy_price + 150000
    def post_prices(self, startRow, lastRow, st):
        progress = st.empty()
        
        df = self.get_data()
        batch = {'update':[]}
        for i in range(startRow, lastRow):
            progress.markdown(f'Initial updating row is: {i}')
            torob_data = self.torob_data(df['torob link'][i])
            buy_price = df['buy price'][i]
            if len(buy_price) > 0:
                final_price = self.final_price(buy_price, torob_data['price list'])
                batch['update'].append(
                    {
                        'id':df['id'][i],
                        'sale_price':'',
                        'regular_price': final_price,
                        'stock_status': 'instock'
                    }
                )
            else:
                batch['update'].append(
                    {
                        'id':df['id'][i],
                        'sale_price':'',
                        'stock_status': 'outofstock'
                    }
                )
        print(wcapi.post("products/batch", batch).json()) 
        return batch
    def get_data(self):
        result = self.sheet.values().get(spreadsheetId=self.sheet_id_target, range= "data!A1:E200").execute()
        data = result['values']
        
        for l in data:
            max = len(data[0])
            if len(l) < max:
                while True:
                    l.append('')
                    if len(l) == len(data[0]):
                        break
#         index = [first[0] for first in data][1:]
        headless_data = data[1:]
        df = pd.DataFrame(headless_data, columns=data[0])
        
        return df 
