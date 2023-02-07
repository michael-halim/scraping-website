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

def get_contact(driver):
    url = 'https://atesonhome.com/locations/'
    driver.get(url)

    phones = driver.find_elements(By.CSS_SELECTOR, 'div.elementor-element.elementor-element-27c7bd6.elementor-widget.elementor-widget-text-editor > div.elementor-widget-container > div.elementor-text-editor.elementor-clearfix > div:nth-child(3)')
    addresses = driver.find_elements(By.CSS_SELECTOR, 'div.elementor-element.elementor-element-27c7bd6.elementor-widget.elementor-widget-text-editor > div.elementor-widget-container > div.elementor-text-editor.elementor-clearfix > div:nth-child(2)')

    tmp_phone = None
    tmp_address = None
    
    phone_replace = {
        '+':'',
        '(':'',
        ')':'',
        '-':''
    }
    for phone, address in zip(phones, addresses):
        tmp_phone = phone.get_attribute('innerHTML')
        tmp_phone = replace_multiple_char(tmp_phone, char_to_replace=phone_replace)
        tmp_phone = re.sub(r'\s{0,}?','',tmp_phone)
        tmp_phone = tmp_phone.strip()

        tmp_address = address.get_attribute('innerHTML')
        tmp_address = tmp_address.strip()
    
    print_help(var=tmp_phone, title='PHONE', username='GET CONTACT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
    print_help(var=tmp_address, title='ADDRESS', username='GET CONTACT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)

    return tmp_phone, tmp_address

def get_category_and_links(driver):
    url = 'https://atesonhome.com/'
    driver.get(url)

    try:
        # Get Nav Object
        nav_object = driver.find_elements(By.CSS_SELECTOR, 'li#mega-menu-item-text-24 > div.textwidget > p > a')
        tmp_data = {}
        for nav in nav_object:
            location = []
            nav_title = nav.get_attribute('innerHTML')
            nav_link = nav.get_attribute('href')

            if 'kitchen' in nav_title.lower():
                location.append('dapur')
                location.append('ruang makan')
            else:
                location.append('kamar mandi')

            # Remove Duplicate
            tmp_data[nav_title] = {
                'title':nav_title,
                'link':nav_link,
                'category':location,
            }

        collections = []
        for data in tmp_data:
            print_help(var=tmp_data[data]['title'], title='LINK NAME', username='GET CATEGORY AND LINKS',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
            print_help(var=tmp_data[data]['link'], title='LINK URL', username='GET CATEGORY AND LINKS',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
            print_help(var=tmp_data[data]['category'], title='LINK CATEGORY', username='GET CATEGORY AND LINKS',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
            
            collections.append({
                'title':tmp_data[data]['title'],
                'link':tmp_data[data]['link'],
                'category':tmp_data[data]['category'],
            })
        
        # Save Links to File
        filename = 'links'
        dirname = os.path.dirname(__file__)
        dest_path = os.path.join(dirname, filename)
        save_to_file(dest_path=dest_path, 
                    filename=filename, 
                    itemList = collections)

    except WebDriverException as e:
        print_help(var=e, title='EXCEPTION', username='GET CATEGORY AND LINKS',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
        print_help(var='WEB DRIVER FAILED', username='GET CATEGORY AND LINKS',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)


def get_every_product(driver, phone, address):
        try:

            try:
                from .links import links as DATASET
            except ImportError as e:
                print_help(var=e, title='TRY IMPORT ERROR', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                from links import links as DATASET

            productList = []
            for data in DATASET:
                PAGE = 1
                is_not_found = False
                # Find All Pages until Not Found
                while(1):
                    url = f'{data["link"]}page/{PAGE}/'
                    driver.get(url)
                    
                    # If Page is Not Found
                    try:
                        is_not_found_object = driver.find_element(By.CSS_SELECTOR, 'div.rt-entry-content > h2')
                        if is_not_found_object.get_attribute('innerHTML') == 'Unfortunately, the page you requested could not be found.':
                            is_not_found = True

                    except WebDriverException as e:
                        print_help(var=e, title='WEB DRIVER EXCEPTION', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var='PAGE STILL FOUND NEXT PAGE', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                    
                    if is_not_found:
                        break

                    # Get Product Names, Prices, Pictures, and Links
                    product_names_links = driver.find_elements(By.CSS_SELECTOR, 'h3.rt-product__title > a')
                    product_prices = driver.find_elements(By.CSS_SELECTOR,'span.woocommerce-Price-amount.amount > bdi')
                    product_pictures = driver.find_elements(By.CSS_SELECTOR,'div.rt-product__thumbnail > a:nth-child(2) > img')
                    
                    for name_link, price, pic in zip(product_names_links,product_prices, product_pictures):
                        char_to_replace = {
                            '&amp;':'and',
                            '.':'',
                            'Rp':''
                        }
                        # Get Product Name, Price, Picture, Link and Preprocess it
                        product_name = name_link.get_attribute('innerHTML')
                        product_name = product_name.encode('ascii', 'ignore').decode()
                        product_name = replace_multiple_char(product_name,char_to_replace)
                        product_name = re.sub('\s{2,}',' ',product_name)
                        product_name = product_name.strip()

                        product_price = price.get_attribute('innerHTML')
                        product_price = replace_multiple_tags(product_price,'<span','</span>')
                        product_price = replace_multiple_char(product_price,char_to_replace)
                        product_price = product_price.strip()

                        product_picture = pic.get_attribute('src')
                        product_link = name_link.get_attribute('href')
                        
                        print_help(var=data['category'], title='PRODUCT CATEGORY', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=product_name, title='PRODUCT NAME', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=product_price, title='PRODUCT PRICE', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=product_picture, title='PRODUCT PICTURE', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=product_link, title='PRODUCT LINK', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        
                        productList.append({ 'name':product_name, 'pic':product_picture,
                                            'price':product_price, 'link': product_link,
                                            'address':address, 'contact_phone':phone,
                                            'tags':data['category'], 'furnitureLocation':data['category'],
                                            'isProduct':1 })
                    PAGE += 1

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

                # Get Description and Additional Description Object
                product_descriptions = driver.find_elements(By.CSS_SELECTOR, 'div#tab-description')
                additional_desc_title = driver.find_elements(By.CSS_SELECTOR, 'th.woocommerce-product-attributes-item__label')
                additional_desc_value = driver.find_elements(By.CSS_SELECTOR, 'td.woocommerce-product-attributes-item__value')
                is_available_object = driver.find_element(By.CSS_SELECTOR, 'p.stock')
                
                for desc in product_descriptions:

                    # If Object is Not Available Don't Preprocess it
                    is_available = is_available_object.get_attribute('innerHTML')
                    if is_available.lower() != 'out of stock':
                        
                        # Get Product Description and Preprocess it
                        product_desc = desc.get_attribute('innerHTML')

                        char_to_replace = {
                        '\n':'<br>',
                        '<p>':'',
                        '</p>':'',
                        '&amp;':' dan',
                        }

                        product_desc = replace_multiple_char(product_desc,char_to_replace)
                        product_desc = product_desc.encode('ascii', 'ignore').decode()

                        # Remove Excess Whitespace in the middle of the string
                        product_desc = re.sub('\s{2,}',' ', product_desc)
                        product_desc = product_desc.strip()

                        additional_desc = ''
                        product_color = ''
                        material = ''
                        weight = ''
                        weight_unit = ''
                        dimension_length = ''
                        dimension_width = ''
                        dimension_height = ''
                        dimension_unit = ''

                        for title,value in zip(additional_desc_title,additional_desc_value):
                            
                            tmp_title = title.get_attribute('innerHTML')
                            tmp_value = value.get_attribute('innerHTML')
                            tmp_value = tmp_value.encode('ascii', 'ignore').decode()

                            tmp_title = re.sub('\s{2,}',' ', tmp_title)
                            tmp_value = re.sub('\s{2,}',' ', tmp_value)

                            tmp_title = replace_multiple_char(tmp_title,char_to_replace)
                            tmp_value = replace_multiple_char(tmp_value,char_to_replace)

                            additional_desc += tmp_title + ': ' + tmp_value + '<br>'

                            if tmp_title.lower() == 'colour':
                                product_color = tmp_value.lower()
                                product_color = product_color.replace('<br>','')
                                product_color = replace_multiple_char(product_color, char_to_replace = AtesonHome_COLOR_REPLACE)
                                hard_to_remove_word = {
                                    'stainless white':'silver',
                                }
                                product_color = replace_multiple_char(product_color, char_to_replace=hard_to_remove_word)

                            elif tmp_title.lower() == 'material':
                                material = tmp_value.lower()
                                material = material.replace('<br>','')
                                material = replace_multiple_char(material, char_to_replace = AtesonHome_COLOR_REPLACE)
                                material = material.strip()
                                material = replace_multiple_char(material, char_to_replace= AtesonHome_MATERIAL_REPLACE)
                                material = material.strip()
                                material = replace_multiple_char(material, AtesonHome_HARD_REMOVE_MATERIAL)
                                material = material.strip()
                                material = re.sub(r'^,\s{0,}?','',material)
                                material = re.sub(r',\s{0,}?$','',material)
                                material = re.sub(r'\s?,\s?',',',material)
                                material = material.strip()
                                
                            elif tmp_title.lower() == 'weight':
                                res = re.search(r'(\d+)\s?([a-z]+)',tmp_value)
                                weight = res.group(1)
                                weight_unit = res.group(2)
                                if weight_unit == 'g':
                                    weight_unit = 'kg'
                                    weight = int(weight) / 1000

                            elif tmp_title.lower() == 'dimension' or tmp_title.lower() == 'dimensions':
                                res = re.search(r'(\d+)\s?(\d+)\s?(\d+)\s?([a-z]+)',tmp_value)
                                dimension_length = res.group(1)
                                dimension_width = res.group(2)
                                dimension_height = res.group(3)
                                dimension_unit = res.group(4)

                        additional_desc = re.sub('(\\n){2,}','<br>', additional_desc)
                        additional_desc = additional_desc.rstrip('\n')


                        print_help(var=product_desc, title='PRODUCT DESC', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=additional_desc, title='ADDITIONAL DESC', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=product_color, title='PRODUCT COLOR', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=material, title='PRODUCT MATERIAL', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=dimension_length, title='PRODUCT DIMENSION LENGTH', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=dimension_width, title='PRODUCT DIMENSION WIDTH', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=dimension_height, title='PRODUCT DIMENSION HEIGHT', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=dimension_unit, title='DIMENSION UNIT', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=weight, title='PRODUCT WEIGHT', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=weight_unit, title='WEIGHT UNIT', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var=is_available_object.get_attribute('innerHTML'), title='IS AVAILABLE', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)

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
                            'additional_desc': additional_desc,
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
    print_help(var='RUNNING ATESON HOME WEB SCRAPING....', username='MAIN', save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)

    get_category_and_links(driver=driver)
    phone, address = get_contact(driver=driver)
    get_every_product(driver=driver, phone=phone, address=address)
    get_every_detail(driver=driver)
    
    driver.quit()
    
    print_help(var='FNISIHED ATESON HOME WEB SCRAPING....', username='MAIN', save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time)))

if __name__ == '__main__':
    main()