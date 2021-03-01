import time
import re
import pandas as pd
import requests
import logging
from bs4 import BeautifulSoup
import openpyxl

formatter = '%(levelname)s : %(filename)s : %(asctime)s : %(message)s'
logging.basicConfig(level=logging.INFO, format=formatter)


from constants import Consts
from utils import get_shopname_shop_url

class ScrapedData(object):

    def __init__(self, target_url):
        self.target_url = target_url
        self.html = requests.get(self.target_url).text
        self.doc = BeautifulSoup(self.html, 'html.parser')

    def get_search_list(self):
        return self.doc.select('li.searchListCassette')

    def get_phone_url(self):
        phone_number_url = self.doc.select_one('td.w618 > a').get('href')

        return phone_number_url

    def get_phone_number(self):
        phone_number = self.doc.select_one('td.fs16').text

        return phone_number

    def get_page_number(self):
        current_page_element = self.doc.select_one('p.pa').text.split('/')[0]
        page_number = re.sub("[^0-9]", "", current_page_element)
        page_number = int(page_number)

        return page_number



if __name__ == '__main__':
    i = 1
    dict = {'美容院': [], 'URL': [], '電話番号': []}
    while True:

        # ページ一枚分のデータを取る
        crawling_URL = Consts.TARGET_URL.format(i)
        data = ScrapedData(crawling_URL)
        list_shop_data = data.get_search_list()
        logging.info('%s', 'Scraping {}'.format(crawling_URL))

        # 一番最後のページに到達したらスクリプトを止める
        if i > data.get_page_number():
            logging.warning('%s', 'Reached the End of Search. Stopping it at Page {}'.format(data.get_page_number()))
            break

        for item in list_shop_data:
            # お店の名前とURLを抽出
            shop_name, shop_url = get_shopname_shop_url(item)
            # お店の電話番号を抽出
            shop_data = ScrapedData(shop_url)
            phone_url = shop_data.get_phone_url()
            phone_data = ScrapedData(phone_url)
            phone_number = phone_data.get_phone_number()

            #とった情報を格納
            dict['美容院'].append(shop_name)
            dict['URL'].append(shop_url)
            dict['電話番号'].append(phone_number)

        logging.info('%s', 'Finished Page {}'.format(i))
        i += 1


    # 辞書型に入れていたデータをデータフレームに変換
    dict_final = {}

    for k, v in dict.items():
        dict_final[k] = pd.Series(v)

    df = pd.DataFrame(dict_final)
    logging.info('%s', 'Exporting Excel File')

    # CSVにエクスポート
    df.to_csv('hotpepper.csv')
    logging.info('%s', 'Successfully Exported!')






