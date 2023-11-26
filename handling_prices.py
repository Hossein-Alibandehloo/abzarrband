from __future__ import print_function
import requests,convert_numbers, random, re
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd
from time import sleep
from lxml import html
from woocommerce import API
from googlesearch import search
from nltk.tokenize import sent_tokenize, word_tokenize
import ast, datetime




start_row = 2
last_row = 5

class Updater:
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
        http_proxy = "halibandehloo_gmail_com:Hg6670hg6670@la.residential.rayobyte.com:8000"
        https_proxy = "halibandehloo_gmail_com:Hg6670hg6670@la.residential.rayobyte.com:8000"
        # http_proxy = ""
        # https_proxy = ""

        self.proxyDict = {
            "http": http_proxy,
            "https": https_proxy,
        }
        
    def request_header(self):
        user_agent_list = [
            "Windows 10/ Edge browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
            "Windows 7/ Chrome browser: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
            "Mac OS X10/Safari browser: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
            "Linux PC/Firefox browser: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
            "Chrome OS/Chrome browser: Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
            ]
        user_agent = random.choice(user_agent_list)
        headers = {
            'User-Agent':user_agent
        }
        return headers
    def torob_data(self, url):
        try:
            req = requests.get(url, headers=self.request_header(), proxies=self.proxyDict)
#         req = requests.get(url, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'})
        except: 
            {'sellers': [], 'price list': []}
            print("error: ", url)
            
        page_info = req.text
        xpath = html.fromstring(page_info)
        # resp = xpath.xpath("//div[@class='jsx-1883554428 purchase-info seller-element']/a/text()")
            # json_data = xpath.xpath("//script[@type='application/ld+json']/text()")
            # sellers_data = ast.literal_eval(str(json_data[0]).replace('"بناباز"', ''))['offers']['offers']
            # sellers_data = sellers_data.sort(key = lambda x: x['price'])
            # print(sellers_data[0])
            # abzarbrand_rank = 0
            # sellers_data2 = sellers_data
            # for i, seller_data in enumerate(sellers_data):
            #     # print(seller_data)
            #     if seller_data['name'] == "ابزاربرند":
            #         abzarbrand_rank = i + 1
            #         sellers_data2.pop(i)
            
            # price_ls = [(int(data['price']) / 10) for data in sellers_data2 if data['@type'] == "Offer"]
            # sellers = [data['name'] for data in sellers_data2 if data['@type'] == "Offer"]
            # return {'sellers': sellers, 'price list': price_ls, 'abzarbrand rank': abzarbrand_rank}
                
        # except: return "N/A"
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
        if 'ابزاربرند' in sellers and len(sellers) != 1:
            ind = sellers.index('ابزاربرند')
            if len(price_ls) > ind:
                del price_ls[ind]
            del sellers[ind]
        price_ls.sort()
        return {'sellers': sellers, 'price list': price_ls}    
    def final_price(self, buy_price, price_list, seller_list):
        buy_price = int(buy_price.replace(',',''))
        plc = 0
        print('price list: ',price_list)
        print('seller list: ',seller_list)
        if len(price_list) == 1 and seller_list[0] == 'ابزاربرند':
            return price_list[0]

        elif len(price_list) >= 1:
            for i in range(len(price_list)):
                if buy_price < price_list[0]:
                    plc = 1
                elif buy_price >= price_list[-1]:
                    plc = len(price_list) + 1
                elif price_list[i] <= buy_price < price_list[i + 1]:
                    plc = i + 2
            
        else:
            return int(buy_price * 1.1 + 100000)
            
        
        if plc <= len(price_list):
            if len(price_list) == 0:
                final_price = buy_price * 1.1
            else:
                final_price = price_list[plc - 1] - 2000
        else:
            final_price = buy_price + 150_000
        
        if final_price - buy_price <= 50_000:
            final_price = buy_price + 200_000
        return final_price

    def abzarchi_price(self, url):
        req = requests.get(url)
        page_info = req.text
        xpath = html.fromstring(page_info)
        price_list = xpath.xpath("//div[@class='product-page-main']//span[@class='woocommerce-Price-amount amount']//text()")
        if len(price_list) != 0:
            return str(price_list[0].replace(",",'')).strip()
        else:
            return ''

    def post_prices_to_google_sheet(self,df, startRow, lastRow):
        
        batch = {'update':[]}
        data = []
        for i in range(startRow, lastRow + 1):
            buy_price = df['buy price'][i]
            print(i)
            target_link = df['target link'][i]
            if 'torob.com' in target_link:
                torob_data = self.torob_data(target_link)
                print('torob data is: ', torob_data)
                if len(buy_price) > 0:
                    final_price = self.final_price(buy_price, torob_data['price list'], torob_data['sellers'])
                                        
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
            else:
                if len(buy_price) > 0:
                    data.append([int(int(buy_price.replace(",", '')) * 1.1)])
                else:
                    data.append([''])

        print(data)
        self.sheet.values().update(
        spreadsheetId=self.sheet_id_target,
        range="data!C{}:C{}".format(startRow, lastRow + 1),
        valueInputOption="USER_ENTERED",
        body={'values':data}
        ).execute()
        # print(self.wcapi.post("products/batch", batch).json()) 
        # return batch
    def post_prices_to_abzarbrand(self, df, startRow, lastRow):
        batch = {'update':[]}
        for i in range(startRow, lastRow + 1):

            price = df['sell price'][i].replace(',','')
            
            if len(price) > 0:
                batch['update'].append(
                            {
                                'id':df['id'][i],
                                'sale_price':price,
                                # 'date_on_sale_from':datetime.datetime.now(),
                                # 'date_on_sale_to':datetime.datetime.now() + datetime.timedelta(days=2),
                                'regular_price': str(int(price) + 100000 + 0.1 * int(price)),
                                'stock_status': 'instock',
                                # 'on_sale': 1,
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
    def post_id(self, df, startRow, lastRow):
        data = []
        for i in range(startRow, lastRow + 1):
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
                
        self.sheet.values().update(
        spreadsheetId=self.sheet_id_target,
        range="data!D{}:D{}".format(startRow, lastRow + 1),
        valueInputOption="USER_ENTERED",
        body={'values':data}
        ).execute()
    def check_model_in_name(self, word, full_text):
        if re.search(r'\b{}\b'.format(word), full_text):
            return 1
        else:
            return 0
    def post_abzarchi_link(self, df, startRow, lastRow):
        data = []
        for i in range(startRow, lastRow + 1):
            print(i)
            product_model = self.model(df.loc[i, 'name'])
            print(product_model)
            query = df.loc[i, 'Brand'] + " " +  product_model + ' ابزارچی'
            google_search_results = search(query, tld="co.in", num=10, stop=9, pause=2)
            link_list = []
            for result in google_search_results:
                if 'abzarchi.com/product/' in result:
                    response = requests.get(result)
                    xpath = html.fromstring(response.text)
                    abzarchi_product_name = xpath.xpath("//h1/text()")[0]
                    if self.check_model_in_name(product_model, abzarchi_product_name):                
                        link_list.append(result.strip())
            if len(link_list) > 0:
                data.append([link_list[0]])
            else:
                data.append([''])
        self.sheet.values().update(
        spreadsheetId=self.sheet_id_target,
        range="data!E{}:E{}".format(startRow, lastRow),
        valueInputOption="USER_ENTERED",
        body={'values':data}
        ).execute()
    def get_data(self, sheet_name):
        result = self.sheet.values().get(spreadsheetId=self.sheet_id_target, range= f"{sheet_name}!A1:N5000").execute()
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
        df.index = range(2, len(df) + 2)
        return df
    def model(self, name):
        arabicNumbers = ["۰", "۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹"]
        
        for i in range(10):
            name = name.replace(arabicNumbers[i], str(i))

        model = ''
        words = word_tokenize(name)
        
        ls, ls2 = [], []
        for word in words:
            encoded_string = word.encode("ascii", "ignore")
            decode_string = encoded_string.decode()
            if len(decode_string) > 0:
                ls.append(decode_string.strip())
        if len(ls) > 0:
            for item in ls:
                if item != "(" and item != ")":
                    ls2.append(item)
        for i in words:
            if i == 'مدل' or i == 'کد':             
                index_of_m = words.index(i)
                try:
                    index_of_first = ls2.index(words[index_of_m + 1])
                    model = ls2[index_of_first]
                    # for j in range(index_of_first, len(ls)):
                    #     if ls[j] == "(":
                    #         break                    
                    #     model += ls[j] + " "
                    return model
                except:
                    pass
        if len(ls2) > 0:
            for item in ls2:
                if len(item) > 3:
                    model = item
    
            # model = ls[-1]
        units = ['متر', 'میلی', 'وات','اینچ', 'کیلو', 'کیلوگرم', 'میلیمتر', 'سانتی', 'سانتیمتر', 'گرمی', 'اسب', 'سیلندر', 'لیتری', 'کیلویی', 'میلیمتری', 'آمپر', 'بار', '', 'سایز']
        next_word = int()
        if len(model) > 0:
            if model in words:

                index_of_model = words.index(model) + 1
                if not index_of_model == len(words):
                    next_word = words.index(model) + 1

        # if next_word > 0:
        #     for unit_name in units:
        #         if unit_name == words[next_word]:
        #             model = ''
                                       
        return model
    def post_model(self, df, startRow, lastRow):   
        data = []
        for i in range(startRow, lastRow + 1):
            print(i)
            name = df['name'][i]
            data.append([self.model(name).strip()])
        
        self.sheet.values().update(
        spreadsheetId=self.sheet_id_target,
        range="data!I{}:I{}".format(startRow, lastRow + 1),
        valueInputOption="USER_ENTERED",
        body={'values':data}
        ).execute()
    def bulk_post_prices_to_abzarbrand(self, df, s, e):
        round = int((e - s) / 5)
        print(round)
        for i in range(round):
            try:
                print('try', i)
                self.post_prices_to_abzarbrand(df, s + 5 * i, s + 5 * (i+1))
            except:
                pass        
    def get_rank_of_abzarbrand(self, torob_link):
        req = requests.get(torob_link, headers=self.request_header()
                           ,proxies=self.proxyDict
                           )
#         req = requests.get(url, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'})
        page_info = req.text
        xpath = html.fromstring(page_info)
        # resp = xpath.xpath("//div[@class='jsx-1883554428 purchase-info seller-element']/a/text()")
        json_data = xpath.xpath("//script[@type='application/ld+json']/text()")
        sellers_data = ast.literal_eval(str(json_data[0]).replace('"بناباز"', ''))['offers']['offers']
        sellers_data.sort(key = lambda x: int(x['price']))     
        sellers_data2 = [data for data in sellers_data if data['price'] != '0']
        abzarbrand_rank = 0
        for i, seller_data in enumerate(sellers_data2):
            if seller_data['name'] == "ابزاربرند":
                abzarbrand_rank = i + 1
        if abzarbrand_rank == 0:
            return "Not in List",int(int(sellers_data2[0]['price'])/10), len(sellers_data2)
        else:
            return abzarbrand_rank, int(int(sellers_data2[0]['price'])/10), len(sellers_data2)   
    def post_rank_of_abzarbrand_to_googlesheet(self, df, startRow, lastRow):
        list_of_ranks = []
        torob_links = df.loc[startRow:lastRow, 'Torob Link']
        for i, link in enumerate(torob_links):
            print(i + startRow)
            # try:    
            rank_output = self.get_rank_of_abzarbrand(link)
            list_of_ranks.append([rank_output[0],rank_output[1], rank_output[2]])
            # except: list_of_ranks.append(['', '', ''])
        
        self.sheet.values().update(
        spreadsheetId=self.sheet_id_target,
        range="data!G{}:I{}".format(startRow, lastRow + 1),
        valueInputOption="USER_ENTERED",
        body={'values':list_of_ranks}
        ).execute()
        
updater = Updater()

df = updater.get_data('data')
updater.post_prices_to_google_sheet(df, 2, 285)
# updater.bulk_post_prices_to_abzarbrand(df, 2, 285)
