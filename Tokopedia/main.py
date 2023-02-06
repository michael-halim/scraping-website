from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

import time
import datetime
import re
import os 
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent_dir = current + os.sep + os.pardir
sys.path.append(parent_dir)

from helper_func.helper import print_help, replace_multiple_char, replace_text_in_between, replace_multiple_tags, save_to_file, get_today 

try: from .dict_clean import *
except ImportError as e: from dict_clean import *

from dotenv import load_dotenv
load_dotenv()

SAVE_LOG_PATH =  os.path.dirname(__file__) + os.sep + 'scraping_logs' + os.sep
LOG_FILENAME = str(get_today()) + '.txt'

def get_every_product(driver):
        try:
            PAGES = 4
            productList = []
            for i in range(PAGES):
                url = f'https://www.tokopedia.com/find/custom-furniture/c/surabaya?page={i}&pmin=100000'
                driver.get(url)

                SCROLL_PAUSE_TIME = 0.5
                # Get scroll height
                last_height = driver.execute_script("return document.body.scrollHeight")
                new_height = 100
                while True:
                    # Scroll down to bottom
                    driver.execute_script("window.scrollTo(0," + str(new_height) + ");")

                    # Wait to load page
                    time.sleep(SCROLL_PAUSE_TIME)

                    # Calculate new scroll height and compare with last scroll height
                    new_height += 250
                    if new_height >= last_height:
                        break
                

                # Get Product Names, Prices, Pictures, and Links
                product_names = driver.find_elements(By.CSS_SELECTOR, 'div.prd_link-product-name')
                product_prices = driver.find_elements(By.CSS_SELECTOR,'div.prd_link-product-price')
                
                product_links = driver.find_elements(By.CSS_SELECTOR,'div.pcv3__container > div:nth-child(2) > a:first-child')
                product_pictures = driver.find_elements(By.CSS_SELECTOR, '[data-testid=imgProduct]')
                product_addresses = driver.find_elements(By.CSS_SELECTOR, 'span[data-testid="lblShopLocation"]')
                count_item = 0
                for name, price, links, pic, address in zip(product_names, product_prices, product_links, product_pictures, product_addresses):
                    product_name = name.get_attribute('innerHTML')
                    product_name = product_name.encode('ascii', 'ignore').decode()

                    
                    product_price = price.get_attribute('innerHTML')
                    char_to_replace = {
                        '<!--':'',
                        '-->':'',
                        ',':'',
                        ' ':'',
                        '.':'',
                        'Rp':'',
                        'rp':'',
                    }
                    product_price = replace_multiple_char(product_price, char_to_replace)

                    product_picture = pic.get_attribute('src')
                    product_link = links.get_attribute('href')
                    product_address = address.get_attribute('innerHTML')
                    product_address = product_address.replace('Kab.','')
                    product_address = product_address.strip()

                    count_item += 1

                    print_help(var=product_name, title='PRODUCT NAME', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                    print_help(var=product_price, title='PRODUCT PRICE', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                    print_help(var=product_picture, title='PRODUCT PICTURE', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                    print_help(var=product_link, title='PRODUCT LINK', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)

                    productList.append({'name':product_name, 'pic':product_picture,
                                        'price':product_price,'link':product_link,
                                        'address':product_address,
                                        'isProduct':0 })
            
            print('TOTAL ITEM')
            print(count_item)

            # Save data to front_page.py
            filename = 'front_page'
            dirname = os.path.dirname(__file__)
            dest_path = os.path.join(dirname, filename)
            save_to_file(dest_path=dest_path, 
                        filename=filename, 
                        itemList = productList)

        except WebDriverException as e:
            print_help(var=e, title='EXCEPTION', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
            print_help(var='SCRAPING FAILED', title='GET EVERY PRODUCT', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
        

def get_every_detail(driver):
    try:
        try:
            from .front_page import front_page as DATASET
        except ImportError as e:
            print_help(var=e, title='TRY IMPORT ERROR', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
            from front_page import front_page as DATASET

        dataset_copy = []
        count_item = 0
        jenis_kategori = []
        count_ta_tokped = 0
        for data in DATASET:
            
            try:
                driver.get(data['link'])
                link = data['link']
                if link.count('ta.tokopedia') > 0:
                    count_ta_tokped += 1
                else:
                    # Get Description and Additional Description object
                    product_descriptions = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="lblPDPDescriptionProduk"]')
                    additional_descs_object = driver.find_elements(By.CSS_SELECTOR, 'ul[data-testid="lblPDPInfoProduk"] > li')
                    
                    for desc in product_descriptions:
                        
                        # Get Product Description and Preprocess it
                        product_desc = desc.get_attribute('innerHTML')
                        product_desc = product_desc.encode('ascii', 'ignore').decode()
                        char_to_replace = {
                            '&lt;br&gt;':'',
                            'br&gt;':'',
                            '&lt&gt;':'',
                            '&lt;':'',
                            '</td>':'\n\n'
                        }
                        product_desc = replace_multiple_char(product_desc, char_to_replace)
                        product_desc = replace_multiple_tags(product_desc,'<span','>')
                        product_desc = re.sub(r'\s{2,}',' ',product_desc)

                        # Get Additional Description and Preprocess it
                        additional_description = ''
                        furniture_location = []
                        product_color = 'custom'
                        material = 'custom'
                        tags = ''
                        dimension_length = ''  
                        dimension_width = ''
                        dimension_height = ''
                        dimension_unit = 'cm'
                        weight = ''
                        contact_phone = ''
                        weight_unit = 'kg'

                        for count, add_desc in enumerate(additional_descs_object):
                            tmp = add_desc.get_attribute('innerHTML')

                            print('===========================')
                            print(tmp)
                            print('===========================')
                            
                            tmp = replace_multiple_tags(tmp, '<','>')
                            tmp = tmp.replace('<!--','').replace('-->','')
                            
                            tmp_text = tmp.lower()
                            print('===========================')
                            print('TMP TEXT')
                            print(tmp_text)
                            print('===========================')

                            tmp_etalase = tmp_text.count('etalase')
                            print('===========================')
                            print('TMP ETALASE')
                            print(tmp_etalase)
                            print('===========================')
                            tmp_category = tmp_text.count('kategori')
                            print('===========================')
                            print('TMP CATEGORY')
                            print(tmp_category)
                            print('===========================')

                            if tmp_etalase <= 0:
                                additional_description += tmp + '<br>'

                            if tmp_text.count('berat satuan') > 0:
                                tmp_weight = re.search(r'(\d+)\s?(g|kg)',tmp_text)
                                tmp_weight = tmp_weight.group(0)
                                tmp_weight = tmp_weight.split()

                                print('===========================')
                                print('TMP WEIGHT')
                                print(tmp_weight)
                                print(tmp_weight[0])
                                print(tmp_weight[1])
                                print('===========================')

                                weight = tmp_weight[1]
                                if tmp_weight[1] == 'g':
                                    weight = float(tmp_weight[0]) / 1000

                            if tmp_category > 0:
                                tmp_text = tmp_text.lower()
                                tmp_text = tmp_text.replace('kategori:','')
                                tmp_text = tmp_text.strip()

                                if tmp_text == 'kasur' or tmp_text == 'lemari pakaian' or tmp_text == 'rak' \
                                    or tmp_text.count('cermin') > 0 or tmp_text.count('tidur') > 0:

                                    furniture_location += ['kamar tidur']
                                
                                elif tmp_text == 'meja makan' or tmp_text == 'meja bar':
                                    furniture_location += ['ruang makan']

                                elif tmp_text.count('hiasan') > 0 or tmp_text == 'meja tv':
                                    furniture_location += ['ruang tamu','kamar tidur']

                                elif tmp_text.count('custom') > 0:
                                    furniture_location += ['kamar mandi', 'kamar tidur', 'ruang makan', 'dapur', 'ruang keluarga', 'ruang tamu']

                                else:
                                    furniture_location += ['ruang tamu']

                                jenis_kategori.append(tmp_text)

                        print_help(var=data['link'], title='ORIGINAL LINK', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=product_desc, title='PRODUCT DESC', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=additional_description, title='ADDITIONAL DESC', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=product_color, title='PRODUCT COLOR', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=material, title='PRODUCT MATERIAL', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=dimension_length, title='PRODUCT DIMENSION LENGTH', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=dimension_width, title='PRODUCT DIMENSION WIDTH', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=dimension_height, title='PRODUCT DIMENSION HEIGHT', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=dimension_unit, title='DIMENSION UNIT', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=weight, title='PRODUCT WEIGHT', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=weight_unit, title='WEIGHT UNIT', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=furniture_location, title='FURNITURE LOCATION', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)

                        dataset_object = {
                                'name': data['name'],
                                'pic': data['pic'],
                                'price': data['price'],
                                'link': data['link'], 
                                'address': data['address'], 
                                'contact_phone':  contact_phone,
                                'tags': tags,
                                'furnitureLocation': furniture_location,
                                'isProduct': data['isProduct'],
                                'material': material,
                                'weight':weight,
                                'weight_unit':weight_unit,
                                'dimension_length': dimension_length,
                                'dimension_width': dimension_width,
                                'dimension_height': dimension_height,
                                'dimension_unit': dimension_unit,
                                'description': product_desc,
                                'additional_desc': additional_description,
                                'color': product_color
                        }

                        dataset_copy.append(dataset_object)
                count_item += 1
            except WebDriverException as e:
                print_help(var=e, title='EXCEPTION', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                print_help(var='ERROR IN FOR DATASET', title='GET EVERY DETAIL', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
        
        
        print_help(var=jenis_kategori, title='JENIS KATEGORI', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)

        print_help(var=count_ta_tokped, title='COUNT TA TOKPED', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)

        # Check Any Duplicate Name Because in The Database, Every Item is store with Slug
        non_duplicate = {}

        for data in dataset_copy:
            non_duplicate[data['name']] = data

        print_help(var=count_item, title='TOTAL ITEM SCRAPED', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
        dataset_copy = []
        for data in non_duplicate:
            dataset_copy.append(non_duplicate[data])

        # Save Complete Dataset to all_data.py
        filename = 'all_data'
        dirname = os.path.dirname(__file__)
        dest_path = os.path.join(dirname, filename)
        save_to_file(dest_path=dest_path, 
                    filename=filename, 
                    itemList = dataset_copy)

    except FileExistsError as e:
        print_help(var=e, title='EXCEPTION', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
        print_help(var='FILE FRONT PAGE DOESNT EXIST', title='GET EVERY DETAIL', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)


def main():
    # https://chromedriver.storage.googleapis.com/index.html
    s = Service(os.environ.get('CHROMEDRIVER_PATH_DEVELOPMENT'))
    if os.environ.get('DEVELOPMENT_MODE') == 'False':
        s = Service(os.environ.get('CHROMEDRIVER_PATH_PRODUCTION'))

    options = Options()

    if os.environ.get('DEVELOPMENT_MODE') == 'False':
        options.add_argument("--headless")
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument('user-agent={0}'.format(user_agent))

    driver = webdriver.Chrome(service=s, options=options)
    driver.implicitly_wait(15)

    start_time = time.perf_counter()
    print_help(var='RUNNING TOKOPEDIA WEB SCRAPING....', title='TOKOPEDIA WEB SCRAPING', username='MAIN', save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)

    get_every_product(driver=driver)
    get_every_detail(driver=driver)

    driver.quit()
    
    print_help(var='FINISHED TOKOPEDIA WEB SCRAPING....', title='TOKOPEDIA WEB SCRAPING', username='MAIN', save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time)))

if __name__ == '__main__':
    main()