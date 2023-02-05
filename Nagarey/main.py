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

from helper_func.helper import *
from dict_clean import *

from dotenv import load_dotenv
load_dotenv()

def get_contact(driver):
    url = 'https://nagarey.com/about'
    driver.get(url)

    phones = driver.find_elements(By.CSS_SELECTOR, 'p.phone-no')

    tmp_phone = None
    tmp_address = Nagarey_Address
    
    phone_replace = {
        '+':'',
        '(':'',
        ')':'',
        '-':''
    }
    for phone in phones:
        tmp_phone = phone.get_attribute('innerHTML')
        tmp_phone = replace_multiple_tags(tmp_phone, '<i ', '</i>', '')
        tmp_phone = replace_multiple_char(tmp_phone, char_to_replace=phone_replace)
        tmp_phone = re.sub(r'\s{0,}?','',tmp_phone)
        tmp_phone = tmp_phone.strip()

    print(tmp_phone)
    print(tmp_address)

    return tmp_phone, tmp_address

def get_category_and_links(driver):
    url = 'https://nagarey.com/home'
    driver.get(url)

    try:
        nav_object = driver.find_elements(By.CSS_SELECTOR, 'div.inner-ctr > div.nav.navbar-nav > li > a')
        
        collections = []
        for nav in nav_object:
            category_title = nav.get_attribute('innerHTML')

            if not (category_title.lower() == 'new' or category_title.lower() == 'sale'):
                category_link = nav.get_attribute('href')
                print('===============')
                print(category_link)
                print(category_title)
                print('===============')
                collections.append({'title':category_title, 'link':category_link})

        categoryList = []
        for data in collections:
            if data['title'].lower() != 'lighting':

                # Get URL                
                driver.get(data['link'])

                # Get Category Object
                category_object = driver.find_elements(By.CSS_SELECTOR,'p.shop-cover-title > a')

                for category in category_object:
                    location = []
                    category_link = category.get_attribute('href')
                    category_title = category.get_attribute('innerHTML')
                    category_title = category_title.replace('&amp;','and')
                    category_title = re.sub('\s{2,}',' ',category_title)
                    category_title = category_title.lower()

                    for word in category_title.split():
                        if word == 'dine' or word == 'dining' :
                            location.append('ruang makan')
                            break
                        elif word == 'bed':
                            location.append('kamar tidur')
                            break

                        elif word == 'kitchen':
                            location.append('dapur')
                            break

                        elif word == 'art' or word == 'vase' or word == 'decoration' or word == 'pet':
                            location.append('ruang keluarga')
                            location.append('ruang tamu')
                            location.append('kamar tidur')
                            break

                        else:
                            location.append('ruang keluarga')
                            location.append('ruang tamu')
                            break

                    print('===============')
                    print(category_link)
                    print(category_title)
                    print(location)
                    print('===============')
                    categoryList.append({'title':category_title, 'link': category_link, 'category':location})
            else:
                print('LIGHTING')
                categoryList.append({'title':data['title'], 'link': data['link'], 
                                    'category':['ruang keluarga', 'ruang tamu','kamar tidur']})
        
        print('CATEGORY LIST')
        print(categoryList)

        # Save Links to File
        filename = 'links'
        dirname = os.path.dirname(__file__)
        dest_path = os.path.join(dirname, filename)
        save_to_file(dest_path=dest_path, 
                    filename=filename, 
                    itemList = categoryList)

    except WebDriverException as e:
        print(e)
        print('WEB DRIVER FAILED')

def get_every_product(driver, phone, address):
        try:

            try:
                from .links import links as DATASET
            except ImportError as e:
                print(e)
                from links import links as DATASET


            productList = []
            for data in DATASET:
                
                print(data['link'])
                
                driver.get(data['link'])

                # Get Product Names, Prices, Pictures, and Links
                product_names = driver.find_elements(By.CSS_SELECTOR, 'div.info > div.title')
                product_prices = driver.find_elements(By.CSS_SELECTOR,'span.price.normal-price')
                product_pictures = driver.find_elements(By.CSS_SELECTOR,'img.img-responsive')
                product_links = driver.find_elements(By.CSS_SELECTOR, 'div.thumb.col-xs-6.col-sm-4.col-lg-3 > a.transition')
                
                for name, price, pic, link in zip(product_names,product_prices, product_pictures,product_links):
                    char_to_replace = {
                        '&amp;':'and',
                        '.':'',
                        'Rp':''
                    }
                    # Get Product Name, Price, Picture, Link and Preprocess it
                    product_name = name.get_attribute('innerHTML')
                    product_name = product_name.encode('ascii', 'ignore').decode()
                    product_name = replace_multiple_char(product_name,char_to_replace)
                    product_name = re.sub('\s{2,}',' ',product_name)
                    product_name = product_name.strip()

                    product_price = price.get_attribute('innerHTML')
                    product_price = replace_multiple_char(product_price,char_to_replace)
                    product_price = product_price.strip()

                    product_picture = pic.get_attribute('src')
                    product_link = link.get_attribute('href')

                    print('================')
                    print(data['category'])
                    print(product_name)
                    print(product_price)
                    print(product_picture)
                    print(product_link)
                    print('================')
                    productList.append({ 'name':product_name, 'pic':product_picture,
                                        'price':product_price, 'link': product_link,
                                        'address':address, 'contact_phone':phone,
                                        'tags':data['category'], 'furnitureLocation':data['category'],
                                        'isProduct':1 })

            # Save data to front_page.py
            filename = 'front_page'
            dirname = os.path.dirname(__file__)
            dest_path = os.path.join(dirname, filename)
            save_to_file(dest_path=dest_path, 
                        filename=filename, 
                        itemList = productList)

        except WebDriverException as e:
            print(e)
            print('SCRAPING FAILED')
        

def get_every_detail(driver):
    try:

        try:
            from .front_page import front_page as DATASET
        except ImportError as e:
            print(e)
            from front_page import front_page as DATASET

        dataset_copy = []
        for data in DATASET:
            try:
                driver.get(data['link'])

                # Get description object
                product_descriptions = driver.find_elements(By.CSS_SELECTOR, 'div.prod-desc.custom-scroll > h3.hidden + p')
                additional_desc = driver.find_elements(By.CSS_SELECTOR, 'div.prod-desc.custom-scroll > p.help-block + div.row')
                product_colors = driver.find_elements(By.CSS_SELECTOR,'select#id_option_type > option[selected="selected"]')
                isAvailableObject = driver.find_elements(By.CSS_SELECTOR,'div#id-label-type > div > p.control-value')

                for desc,color,isAvailable,add_desc in zip(product_descriptions, product_colors, isAvailableObject, additional_desc):
                    product_is_available = isAvailable.get_attribute('innerHTML')
                    product_is_available = product_is_available.lower()

                    # Check If the Stock is Available or Not
                    if product_is_available == 'stock available':

                        # Get description Text and Preprocess it
                        product_desc = desc.get_attribute('innerHTML')

                        char_to_replace = {
                        '&nbsp;':' ',
                        '\n\n':'\n',
                        '\t':'',
                        ':':'',
                        'Dimesnions': 'Dimensions',
                        '&amp;':'and',
                        '\n-\n':'\n',
                        '-\n':'',
                        '- ':'',
                        'Materials\n':'Materials ',
                        'Bahan\n':'Bahan ',
                        '(cm)\n':'(cm)',
                        'Dimensions\n':'Dimension ',
                        'Ukuran\n':'Ukuran '
                        }

                        # Get Product Description and Preprocess it
                        product_desc = replace_multiple_tags(product_desc,'<','>')
                        product_desc = replace_multiple_char(product_desc,char_to_replace)
                        product_desc = product_desc.replace('(cm)','')
                        product_desc = product_desc.encode('ascii', 'ignore').decode()

                        # Remove Excess Whitespace in the middle of the string
                        product_desc = re.sub('\s{2,}',' ', product_desc)
                        product_desc = product_desc.strip()

                        # Get Dimension from Description with Regex
                        dimension_length = ''
                        dimension_width = ''
                        dimension_height = ''
                        dimension_unit = 'cm'

                        try:
                            res = re.search(r'\b(?:[dD]ime....ns?|Ukuran)\s?([\d.,]+)\s?[Xx]\s?([\d.,]+)\s?[Xx]\s?([\d.,]+).+\b',product_desc)
                            dimension_length = res.group(1)
                            dimension_width = res.group(2)
                            dimension_height = res.group(3)
                        except AttributeError as ae:
                            print('REGEX DIMENSION #1 FAILED')
                            print(ae)
                            try:
                                res = re.search(r'\b(?:[dD]ime....ns?|Ukuran)?\s?[A-Z]?([\d.,]+)\s?(?:cm)?\s?[xX]\s?[A-Z]?\s?([\d.,]+)\s?(?:cm)?\s?[xX]\s?[A-Z]?\s?([\d.,]+)\b',product_desc)
                                dimension_length = res.group(1)
                                dimension_width = res.group(2)
                                dimension_height = res.group(3)
                            except AttributeError as ae:
                                print('REGEX DIMENSION #2 FAILED')
                                print(ae)
                                try:
                                    res = re.search(r'\b(?:[dD]ime....ns?|Ukuran)?(?:DIA)?[A-Z]?\s?([\d,.-]+)\s?(?:cm)?\s?[Xx]?\s?[A-Z]?\s?([\d,.-]+)\b',product_desc)
                                    dimension_length = res.group(1)
                                    dimension_width = res.group(2)
                                    print(dimension_length)
                                    print(dimension_width)
                                    if '-' in dimension_length:
                                        tmp_num1 = dimension_length.split('-')[0] if dimension_length.split('-')[0] else 0
                                        tmp_num2 = dimension_length.split('-')[1] if dimension_length.split('-')[1] else 0
                                        dimension_length = str((float(tmp_num1) + float(tmp_num2)) / 2)

                                    if '-' in dimension_width:
                                        tmp_num1 = dimension_width.split('-')[0] if dimension_width.split('-')[0] else 0
                                        tmp_num2 = dimension_width.split('-')[1] if dimension_width.split('-')[1] else 0
                                        dimension_width = str((float(tmp_num1) + float(tmp_num2)) / 2)

                                    dimension_height = '2'
                                except AttributeError as ae:
                                    print('REGEX DIMENSION #3 FAILED')
                                    print(ae)

                        finally:
                            dimension_length = dimension_length.replace(',','.')
                            dimension_width = dimension_width.replace(',','.')
                            dimension_height = dimension_height.replace(',','.')


                        # Get Material from Description with Regex
                        material = ''
                        try:
                            res = re.search(r'\b(?:[bB]ahan|[Mm]at....ls?)\s[^\n]+\b',product_desc)
                            material = res.group(0)
                            material = material.lower()
                            char_to_replace = {
                                'bahan':'',
                                'materials':'',
                                'material':'',
                                '/':',',

                            }
                            material = replace_multiple_char(material,char_to_replace)
                            material = re.sub(r'[^a-z(),\s]*','',material)
                            material = re.sub(r'(?:\(|\)|\(\)|\(\w+\)|\(\w+|\w+\))','',material)
                            material = re.sub('\s{2,}',' ',material)

                            material = material.strip()
                            material = replace_multiple_char(material, Nagaret_MATERIAL_REPLACE)
                            material = material.strip()
                            material = replace_multiple_char(material, Nagarey_HARD_REMOVE_MATERIAL)
                            material = material.strip()
                            material = re.sub(r'^,\s{0,}?','',material)
                            material = re.sub(r',\s{0,}?$','',material)
                            material = re.sub(r'\s?,\s?',',',material)
                            material = material.strip()
                            material = replace_multiple_char(material, Nagarey_HARD_REMOVE_MATERIAL)

                        except AttributeError as ae:
                            print('REGEX MATERIAL #1 FAILED')
                            print(ae)
                        

                        # Get Color from Detail Page with Regex
                        product_color = color.get_attribute('innerHTML')
                        product_color = product_color.lower()

                        try:
                            char_to_replace = {
                            '&amp;':',',
                            '&amp':',',
                            'amp;':',',
                            'and':','
                            }
                            product_color = replace_multiple_char(product_color,char_to_replace)
                            product_color = re.sub(r'[^a-z,\s]*', '', product_color)
                            product_color = re.sub(r'\s[xX]\s', ',', product_color)
                            product_color = re.sub('\s{2,}', ' ', product_color)
                            product_color = product_color.strip()
                            product_color = replace_multiple_char(product_color,char_to_replace=Nagarey_COLOR_REPLACE)
                            product_color = replace_multiple_char(product_color,char_to_replace=Nagarey_COLOR_REPLACE)
                            product_color = replace_multiple_char(product_color,char_to_replace=Nagarey_HARD_REMOVE_COLOR)
                        except AttributeError as ae:
                            print('REGEX COLOR #1 FAILED')
                            print(ae)

                        # Get Additional Description from Detail Page with Regex
                        additional_description = add_desc.get_attribute('innerHTML')
                        additional_description = replace_multiple_tags(additional_description,'<','>')
                        char_to_replace = {
                        '&nbsp;':' ',
                        '\n':'',
                        '\t':'',
                        'Days':'Days\n',
                        '&amp;':'and',
                        ' **':'\n**'
                        }
                        additional_description = replace_multiple_char(additional_description,char_to_replace)
                        additional_description = additional_description.encode('ascii', 'ignore').decode()
                        additional_description = additional_description.strip()

                        print('================')
                        print(product_desc)
                        print('MATERIAL', material)
                        print('DIMENSION LENGTH', dimension_length)
                        print('DIMENSION WIDTH', dimension_width)
                        print('DIMENSION HEIGHT', dimension_height)
                        print('DIMENSION UNIT', dimension_unit)
                        print('COLOR ',product_color)
                        print('IS AVAILABLE',product_is_available)
                        print('================')
                        
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
                            'weight':'',
                            'weight_unit':'',
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
                print(e)
                print('ERROR IN FOR DATASET')

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
        print(e)
        print('FILE FRONT PAGE DOESNT EXIST')

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

    print('RUNNING NAGAREY WEB SCRAPING....')

    get_category_and_links(driver=driver)
    phone, address = get_contact(driver=driver)
    get_every_product(driver=driver, phone=phone, address=address)
    get_every_detail(driver=driver)

    driver.quit()

    print('FINISHED NAGAREY WEB SCRAPING....')
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time)))

if __name__ == '__main__':
    main()