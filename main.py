from __future__ import print_function

import requests,convert_numbers, random

from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd
from time import sleep
from lxml import html
from woocommerce import API
from googlesearch import search
from nltk.tokenize import sent_tokenize, word_tokenize




start_row = 2
last_row = 5

class updater:
    SCOPES = None
    creds = None
    sheet_id_target = None
    sheet = None
    wcapi = API(
    url="https://abzarbrand.com",
    consumer_key="ck_bb0f947f73f3d690eb816a960703d84e0ad59723",
    consumer_secret="cs_ad0ce66b5a121e14d7795149425b59f678f4dc98",
    version="wc/v3"
    )

    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        SERVICE_ACCOUNT_FILE = 'endless-fire.json'

        self.creds = None
        self.creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)

        self.sheet_id_target = '1HHGVnpIxfGZz-icG9Uom-iWUsCFUlMMh_Kw5jIIktpw'
        service = build('sheets', 'v4', credentials=self.creds)
        self.sheet = service.spreadsheets()
 
    def torob_data(self, url):
        req = requests.get(url)
#         req = requests.get(url, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'})
        page_info = req.text
        xpath = html.fromstring(page_info)
        # resp = xpath.xpath("//div[@class='jsx-1883554428 purchase-info seller-element']/a/text()")
        prices = xpath.xpath("//a[contains(@class,'price seller-element')]/text()")
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
        price_ls.sort()
        return {'sellers': sellers, 'price list': price_ls}
    
    def final_price(self, buy_price, price_list):
        buy_price = int(buy_price.replace(',',''))
        plc = 0
        if len(price_list) != 0:
            for i in range(len(price_list)):
                if buy_price < price_list[0]:
                    plc = 1
                elif buy_price >= price_list[-1]:
                    plc = len(price_list) + 1
                elif price_list[i] <= buy_price < price_list[i + 1]:
                    plc = i + 2
        else:
            return 0
        if plc <= len(price_list):
            if len(price_list) == 0:
                final_price = buy_price + 150000
            else:
                final_price = price_list[plc - 1] - 1000
        else:
            final_price = buy_price + 150_000
        
        if final_price - buy_price <= 30_000:
            final_price = buy_price + 50_000
        return final_price
    def abzarchi_price(self, url):
        req = requests.get(url)
        page_info = req.text
        xpath = html.fromstring(page_info)
        stock_box = xpath.xpath("//p[@class='stock out-of-stock']/text()")
        if len(stock_box) == 0:
            prices = xpath.xpath("//div[@class='product-page-main']//p[@class='price']/span//text()")
            if len(prices) > 1:
                str_price = prices[0]
                price = str_price.replace(',','')
                return str(price)
            else:
                return ''
        else:
            return ''
    def post_prices_to_google_sheet(self, startRow, lastRow):
        startRow = startRow -2
        print("---------")
        df = self.get_data()
        batch = {'update':[]}
        data = []
        for i in range(startRow, lastRow - 1):
            print(i + 2)
            target_link = df['target link'][i]
            if 'torob.com' in target_link:
                torob_data = self.torob_data(target_link)
                buy_price = df['buy price'][i]
                if len(buy_price) > 0:
                    final_price = self.final_price(buy_price, torob_data['price list'])
                    if final_price != 0:
                        data.append([final_price])
                    elif final_price == 0:
                        data.append([''])
                else:
                    data.append([''])
            elif 'abzarchi.com' in target_link:
                
                price = self.abzarchi_price(target_link)
                print(price, '        ', target_link)
                batch['update'].append(
                    {
                        'id':df['id'][i],
                        'sale_price':'',
                        'regular_price': price,
                        'stock_status': 'instock'
                    }
                )
                data.append([price])
        
        self.sheet.values().update(
        spreadsheetId=self.sheet_id_target,
        range="data!C{}:C{}".format(startRow + 2, lastRow + 2),
        valueInputOption="USER_ENTERED",
        body={'values':data}
        ).execute()                
        print(self.wcapi.post("products/batch", batch).json()) 
        return batch
    def post_prices_to_abzarbrand(self, startRow, lastRow):
        batch = {'update':[]}
        df = self.get_data()
        for i in range(startRow - 2, lastRow - 1):
            price = df['sell price'][i].replace(',','')
            if len(price) > 0:
                batch['update'].append(
                            {
                                'id':df['id'][i],
                                'sale_price':'',
                                'regular_price': price,
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
        print(self.wcapi.post("products/batch", batch).json())  
                
    def post_id(self, startRow, lastRow):
        df = self.get_data()
        data = []
        for i in range(startRow -2, lastRow - 1):
            url = df['abzarbrand link'][i]
            print('url is:  ', url)
            req = requests.get(url)
            page_info = req.text
            xpath = html.fromstring(page_info)
            short_link = xpath.xpath("//link[@rel='shortlink']/@href")
            if len(short_link) > 0:
                id = short_link[0].replace("https://abzarbrand.com/?p=", "")
                data.append([id])
            else:
                id = ''
                data.append([id])
                
        request = self.sheet.values().update(
        spreadsheetId=self.sheet_id_target,
        range="data!D{}:D{}".format(startRow, lastRow),
        valueInputOption="USER_ENTERED",
        body={'values':data}
        ).execute()
    def post_abzarchi_link(self, startRow, lastRow):
        df = self.get_data()
        data = []
        for i in range(startRow -2, lastRow - 1):
            print(i + 2)
            query = df['name'][i] + ' ابزارچی'
            link_list = []
            for j in search(query, tld="co.in", num=10, stop=9, pause=2):
                if 'abzarchi.com/product/' in j:
                    link_list.append(j.strip())
            if len(link_list) > 0:
                data.append([link_list[0]])
            else:
                data.append([''])
        request = self.sheet.values().update(
        spreadsheetId=self.sheet_id_target,
        range="data!E{}:E{}".format(startRow, lastRow),
        valueInputOption="USER_ENTERED",
        body={'values':data}
        ).execute()
    def get_data(self):
        result = self.sheet.values().get(spreadsheetId=self.sheet_id_target, range= "data!A1:F2000").execute()
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
    def model(self, name):
        arabicNumbers = ["۰", "۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹"]
        
        for i in range(10):
            name = name.replace(arabicNumbers[i], str(i))

        model = ''
        words = word_tokenize(name)
        
        ls = []
        for word in words:
            encoded_string = word.encode("ascii", "ignore")
            decode_string = encoded_string.decode()
            if len(decode_string) > 0:
                ls.append(decode_string.strip())
        
        for i in words:
            if i == 'مدل':
                index_of_m = words.index(i)
                index_of_first = ls.index(words[index_of_m + 1])
                for j in range(index_of_first, len(ls)):
                    if ls[j] == "(":
                        break                    
                    model += ls[j] + " "
                return model
        if len(ls) > 0:
            for item in ls:
                if item == "(":
                        break
                if len(item) > 2:
                    model = item
            # model = ls[-1]
        
        units = ['متر', 'میلی', 'وات','اینچ', 'کیلو', 'کیلوگرم', 'میلیمتر', 'سانتی', 'سانتیمتر', 'گرمی', 'اسب', 'سیلندر', 'لیتری', 'کیلویی', 'میلیمتری', 'آمپر', 'بار', '']
        next_word = int()
        if len(model) > 0:
            if model in words:
                length = words.index(model) + 1
                if not length == len(words):
                    next_word = words.index(model) + 1
        if next_word > 0:
            for word in units:
                if word == words[next_word]:
                    model = ''             
        return model
    
    def post_model(self, startRow, lastRow):
        df = self.get_data()
        data = []
        for i in range(startRow -2, lastRow - 1):
            print(i + 2)
            name = df['name'][i]
            data.append([self.model(name).strip()])
        
        self.sheet.values().update(
        spreadsheetId=self.sheet_id_target,
        range="data!I{}:I{}".format(startRow, lastRow),
        valueInputOption="USER_ENTERED",
        body={'values':data}
        ).execute()


updater = updater()
def google_sheet(s, e):
    round = int((e - s) / 20)
    for i in range(round):
        updater.post_prices_to_google_sheet(s + 20*i,s + 20*(i+1))
      
def abzarbrand_price(s, e):
    round = int((e - s) / 10)
    for i in range(round):
        try:
            print('try', i)
            updater.post_prices_to_abzarbrand(s + 10 * i, s + 10 * (i+1))
        except:
            pass

# google_sheet(920, 1210)  

abzarbrand_price(804, 1210)
# print(updater.torob_data("http://torob.com/p/e324ef3e-370d-4cb8-8fbe-d82e4ebae6e0/%D8%AF%D8%B1%DB%8C%D9%84-%D8%A8%D8%AA%D9%86-%DA%A9%D9%86-%D8%B1%D9%88%D9%86%DB%8C%DA%A9%D8%B3-%D9%85%D8%AF%D9%84-2726/"))
# updater.post_price(806 , 850)
# print(updater.post_model(804, 1211))
# print(updater.model("پیچ گوشتی چهارسو RH-2871 رونیکس (125×5)"))



# updater.post_abzarchi_link(66, 79)
