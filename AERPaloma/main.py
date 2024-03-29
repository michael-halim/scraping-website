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

SAVE_LOG_PATH =  os.path.join(os.path.dirname(__file__), 'scraping_logs' + os.sep)
LOG_FILENAME = str(get_today()) + '.txt'

def get_contact(driver):
    url = 'https://dekoruma.freshdesk.com/support/solutions/articles/17000117057-hubungi-dekoruma'
    driver.get(url)

    phones = driver.find_elements(By.CSS_SELECTOR, 'td > a[href*="konsultasi"]')
    addresses = driver.find_elements(By.CSS_SELECTOR, 'ul[data-identifyelement="650"] > li[dir="ltr"]')

    tmp_phone = None
    tmp_address = None
    for phone, address in zip(phones, addresses):
        tmp_phone = phone.get_attribute('innerHTML')
        tmp_phone = tmp_phone.replace('(', '').replace(')', '').replace('-', '')
        tmp_phone = tmp_phone.strip()
        
        tmp_address = address.get_attribute('innerHTML')
        tmp_address = replace_multiple_tags(tmp_address, '<br', '>', '')
    
    print_help(var=tmp_phone, title='PHONE', username='GET CONTACT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
    print_help(var=tmp_address, title='ADDRESS', username='GET CONTACT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)

    return tmp_phone, tmp_address

def get_every_product(driver, phone, address):
        try:
            PAGES = 15
            productList = []

            for i in range(1, PAGES+1):
                
                url = f'https://www.dekoruma.com/brands/PALOMA?page={i}'
                driver.get(url)

                # Get Product Names, Prices, Pictures, and Links
                product_names = driver.find_elements(By.CSS_SELECTOR, 'div.gdqlKPEW0WGrWRPRMEEBv')
                product_prices = driver.find_elements(By.CSS_SELECTOR,'span[role=price]')
                
                product_links = driver.find_elements(By.CSS_SELECTOR,'div.Dm8LhUyOXIORVM0BUITws > a[product]:first-child')
                product_pictures = driver.find_elements(By.CSS_SELECTOR, 'img._25riT2FvUgRdndrlHTuo-w')
                
                for name,price,links,pic in zip(product_names,product_prices,product_links,product_pictures):
                    product_name = name.get_attribute('innerHTML')
                    product_name = product_name.encode('ascii', 'ignore').decode()

                    
                    product_price = price.get_attribute('innerHTML')
                    product_price = replace_multiple_tags(product_price,'<strike','</strike>')
                    char_to_replace = {
                        '<!--':'',
                        '-->':'',
                        ',':'',
                        ' ':''
                    }
                    product_price = replace_multiple_char(product_price, char_to_replace)

                    product_picture = pic.get_attribute('src')
                    product_link = links.get_attribute('href')

                    tags = ['kamar tidur','ruang tamu','ruang keluarga']
                    location = ['kamar tidur','ruang tamu','ruang keluarga']

                    if 'mandi' or 'shampoo' or 'sabun' in product_name.lower():
                        tags = ['kamar mandi']
                        location = ['kamar mandi']

                    print_help(var=product_name, title='PRODUCT NAME', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                    print_help(var=product_price, title='PRODUCT PRICE', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                    print_help(var=product_picture, title='PRODUCT PICTURE', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                    print_help(var=product_link, title='PRODUCT LINK', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)

                    productList.append({'name':product_name, 'pic':product_picture,
                                        'price':product_price,'link':product_link,
                                        'address':address, 'contact_phone':phone,
                                        'tags':tags,'furnitureLocation':location,
                                        'isProduct':1 })

            # Save data to front_page.py
            filename = 'front_page'
            dirname = os.path.dirname(__file__)
            dest_path = os.path.join(dirname, filename)
            save_to_file(dest_path=dest_path, 
                        filename=filename, 
                        itemList = productList)

        except WebDriverException as e:
            print_help(var=e, title='EXCEPTION', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
            print_help(var='SCRAPING FAILED', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
        

def get_every_detail(driver):
    try:
        try:
            from .front_page import front_page as DATASET
        except ImportError as e:
            print_help(var=e, title='TRY IMPORT ERROR', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
            from front_page import front_page as DATASET

        dataset_copy = []
        for data in DATASET:

            try:
                driver.get(data['link'])

                # Check if Stock is Available
                is_available_object = driver.find_element(By.CSS_SELECTOR, 'div.t--body.phl > div:first-child > div:first-child')
                is_available = is_available_object.get_attribute('innerHTML')
                is_available = is_available.strip().lower()

                # Don't Take All The Detail if Stock is not Available   
                if is_available != 'stok habis':
                
                    # Get Description and Additional Description object
                    product_descriptions = driver.find_elements(By.CSS_SELECTOR, 'div._3dq5UjErSm8nLRgMyvQbYA + p')
                    additional_descs_object = driver.find_elements(By.CSS_SELECTOR, 'td.pvs')
                    
                    for desc,add_desc in zip(product_descriptions,additional_descs_object):
                        
                        # Get Product Description and Preprocess it
                        product_desc = desc.get_attribute('innerHTML')
                        product_desc = product_desc.encode('ascii', 'ignore').decode()
                        char_to_replace = {
                            '&lt;br&gt;':'',
                            'br&gt;':'',
                            '&lt&gt;':'',
                            '&lt;':'',
                            '</td>':'\n\n',
                            '&amp;':'and',
                        }
                        product_desc = replace_multiple_char(product_desc, char_to_replace)
                        product_desc = replace_multiple_tags(product_desc,'<','>')
                        product_desc = re.sub(r'\s{2,}',' ',product_desc)

                        # Get Additional Description and Preprocess it
                        additional_description = ''
                        isNext = [None,None]
                        product_color = ''
                        material = ''
                        dimension_length = ''  
                        dimension_width = ''
                        dimension_height = ''
                        dimension_unit = 'cm'
                        weight = ''
                        weight_unit = 'kg'
                        for count, add_desc in enumerate(additional_descs_object):
                            tmp_additional_description = add_desc.get_attribute('innerHTML')
                            tmp_additional_description = tmp_additional_description.encode('ascii', 'ignore').decode()
                            tmp_additional_description = replace_multiple_tags(tmp_additional_description,'<','>') 

                            if isNext[0] and isNext[1] == 'warna':
                                product_color = tmp_additional_description.lower()
                                product_color = replace_multiple_char(product_color, AERPaloma_CHAR_TO_REPLACE)

                            elif isNext[0] and isNext[1] == 'material':
                                material = tmp_additional_description.lower()
                                material = replace_multiple_char(material, AERPaloma_CHAR_TO_REPLACE)
                                material = material.strip()
                                material = replace_multiple_char(material, AERPaloma_MATERIAL_REPLACE)
                                material = material.strip()
                                material = replace_multiple_char(material, AERPaloma_HARD_REMOVE_MATERIAL)
                                material = material.strip()
                                material = re.sub(r'^,\s{0,}?','',material)
                                material = re.sub(r',\s{0,}?$','',material)
                                material = re.sub(r'\s?,\s?',',',material)
                                material = material.strip()


                            elif isNext[0] and isNext[1] == 'ukuran barang':
                                res = re.search(r'([\d.,]+)\s?(cm|m)?\s?[xX]?\s?([\d.,]+)\s?(cm|m)?\s?[xX]?\s?([\d.,]+)\s?(cm|m)',tmp_additional_description)
                                dimension_length = res.group(1)
                                dimension_width = res.group(3)
                                dimension_height = res.group(5)

                                dimension_length = dimension_length.replace(',','.')
                                dimension_width = dimension_width.replace(',','.')
                                dimension_height = dimension_height.replace(',','.')

                                if res.group(2) == res.group(4) == res.group(6):
                                    dimension_unit = res.group(2)

                            elif isNext[0] and isNext[1] == 'berat':
                                res = re.search(r'([\d.,]+)\s?(?:kg|g)',tmp_additional_description)
                                weight = res.group(1)
                                weight = weight.replace(',','.')

                            if isNext[0]:
                                isNext[0] = False
                                isNext[1] = None

                            if tmp_additional_description.lower() == 'warna' or \
                                tmp_additional_description.lower() == 'material' or \
                                    tmp_additional_description.lower() == 'ukuran barang' or \
                                        tmp_additional_description.lower() == 'berat':
                                isNext[0] = True
                                isNext[1] = tmp_additional_description.lower()

                            # Because data is in table tr td, if it's a new td add \n
                            if count % 2 == 0 and count != 0 :
                                additional_description += '<br>'
                            else:
                                tmp_additional_description = replace_multiple_char(tmp_additional_description, AERPaloma_CHAR_TO_REPLACE)

                            additional_description += tmp_additional_description + ' '

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

                        dataset_object = {
                            'name': data['name'],
                            'pic': data['pic'],
                            'price': data['price'],
                            'link': data['link'], 
                            'address': data['address'], 
                            'contact_phone':  data['contact_phone'],
                            'tags': data['tags'],
                            'furnitureLocation': data['furnitureLocation'],
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

            except WebDriverException as e:
                print_help(var=e, title='EXCEPTION', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                print_help(var='ERROR IN FOR DATASET', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
        
        # Check Any Duplicate Name Because in The Database, Every Item is store with Slug
        non_duplicate = {}

        for data in dataset_copy:
            non_duplicate[data['name']] = data

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
        print_help(var='FILE FRONT PAGE DOESNT EXIST', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)

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
    
    print_help(var='RUNNING AER PALOMA WEB SCRAPING....', username='MAIN', save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
    
    phone, address = get_contact(driver=driver)
    get_every_product(driver=driver, phone=phone, address=address)
    get_every_detail(driver)

    driver.quit()
    
    print_help(var='FINISHED AER PALOMA WEB SCRAPING....', username='MAIN', save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time)))

if __name__ == '__main__':
    main()