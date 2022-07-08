import requests
from lxml import html
wcapi = API(
    url="https://abzarbrand.com",
    consumer_key="ck_bb0f947f73f3d690eb816a960703d84e0ad59723",
    consumer_secret="cs_ad0ce66b5a121e14d7795149425b59f678f4dc98",
    version="wc/v3"
)
class updater:
    
    # def __init__(self, x):
    #     self.x = x        
    def torob_data(self, url):
      
        req = requests.get(url)
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
