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
    url = 'https://www.soho.id/id/contact'
    driver.get(url)

    contact_object = driver.find_elements(By.CSS_SELECTOR, 'span > strong[data-mce-style]')

    tmp_phone = None
    tmp_address = None
    
    phone_replace = {
        '\n':'',
        '+':'',
        '(':'',
        ')':'',
        '-':''
    }
    address_replace = {
        '\n':''
    }
    for contact in contact_object:

        tmp_contact = contact.get_attribute('innerHTML')
        tmp_contact = tmp_contact.split('<br>')
        print(tmp_contact)

        # tmp_contact = tmp_contact[1]
        # tmp_contact = tmp_contact.split('<br>')
        
        tmp_address = tmp_contact[2]
        tmp_address = replace_multiple_char(tmp_address, char_to_replace=address_replace)
        tmp_address.strip()

        tmp_phone = tmp_contact[3]
        tmp_phone = replace_multiple_char(tmp_phone, char_to_replace=phone_replace)
        tmp_phone = re.sub(r'\s{0,}?','',tmp_phone)
        tmp_phone = tmp_phone.strip()

    print_help(var=tmp_phone, title='PHONE', username='GET CONTACT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
    print_help(var=tmp_address, title='ADDRESS', username='GET CONTACT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)

    return tmp_phone, tmp_address

def get_all_link(driver):
    NAV_LINKS = []
    url = 'https://www.soho.id/'
    driver.get(url)

    try:
        # Get All li with class is__parent
        nav_object = driver.find_elements(By.CSS_SELECTOR, 'span.mobileNavigation-navValueContainerClassName.false')
        
        for nav in nav_object:
            temp_dict = {}

            # Get group link in href in tag <a></a>
            nav_group_object = nav.find_element(By.CSS_SELECTOR, 'a')
            nav_group_link = nav_group_object.get_attribute('href')

            # Get Group Title in innerHTML in <a></a> and Preprocess it
            nav_group_title = nav_group_object.get_attribute('innerHTML')
            nav_group_title = nav_group_title.replace('<!--','').replace('-->','').replace('</i>','').replace('&amp; ','')
            nav_group_title = replace_multiple_tags(nav_group_title,'<','>')
            nav_group_title = nav_group_title.strip()


            print_help(var=nav_group_link, title='NAV GROUP LINK', username='GET ALL LINK',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
            print_help(var=nav_group_title, title='NAV GROUP TITLE', username='GET ALL LINK',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)

            exception_title = ['Promo', 'Hubungi Kami']
            if nav_group_title in exception_title:
                continue

            # Add link and title to dictionary
            temp_dict['link'] = nav_group_link
            temp_dict['title'] = nav_group_title

            NAV_LINKS.append(temp_dict)

        print_help(var=NAV_LINKS, title='ALL NAV LINK AND TITLE', username='GET ALL LINK',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)   
        
        # Save All Links to File
        filename = 'links'
        dirname = os.path.dirname(__file__)
        dest_path = os.path.join(dirname, filename)
        save_to_file(dest_path=dest_path, 
                    filename=filename, 
                    itemList = NAV_LINKS)

    except WebDriverException as e:
        print_help(var=e, title='EXCEPTION', username='GET ALL LINK',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
        print_help(var='ERROR GET ALL LINK', username='GET ALL LINK',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)


def get_every_product(driver, phone, address):
    try:
        # Import Links from Same Folder
        try:
            from .links import links as DATASET
        except ImportError as e:
            print_help(var=e, title='TRY IMPORT ERROR', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
            from links import links as DATASET

        productList = []
        for data in DATASET:
            title = data['title']
            
            driver.get(data['link'])

            SCROLL_PAUSE_TIME = 2
            # Get scroll height
            
            last_height = driver.execute_script("return document.body.scrollHeight")
            new_height = 100
            while True:
                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0," + str(new_height) + ");")

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height += 1050
                last_height = driver.execute_script("return document.body.scrollHeight")
                if new_height >= last_height:
                    break


            # Names and Links are in the same element
            product_links = driver.find_elements(By.CSS_SELECTOR, 'a.products-list__item--link')
            product_names = driver.find_elements(By.CSS_SELECTOR, 'p.products-list__item--label-title')
            product_prices = driver.find_elements(By.CSS_SELECTOR,'p.products-list__item--label-price')
            product_pictures = driver.find_elements(By.CSS_SELECTOR, 'a.products-list__item--link > img.products-list__item--link-image')

            for name, link, price, pic in zip(product_names, product_links, product_prices, product_pictures):
                # Get product name, link , price, and picture
                product_name = name.get_attribute('innerHTML')
                product_name = product_name.encode('ascii', 'ignore').decode()

                product_link = link.get_attribute('href')
                product_picture = pic.get_attribute('src')

                product_price = price.get_attribute('innerHTML')

                char_to_replace = {
                'IDR':'',
                '.00':'',
                ',':'',
                '&nbsp;':'',
                }
                product_price = replace_multiple_char(product_price,char_to_replace)
                product_price = replace_multiple_tags(product_price,'<span class="products-list__item--label-price-sale','</span>', '')
                product_price = replace_multiple_tags(product_price,'<span ','>', '')
                product_price = replace_multiple_tags(product_price,'</','>', '')
                product_price = product_price.strip()
                
                tags = [data['title']]
                furnitureLocation = [ title.lower() ]

                if title.lower() == 'ruang kerja':
                    furnitureLocation = ['ruang kerja','kamar tidur']

                if title.lower() == 'dapur ruang makan':
                    furnitureLocation = ['dapur','ruang makan']

                if title == 'Seri SOHO':
                    tags = ['Seri SOHO',data['title']]
                    furnitureLocation = []

                # Append to productList
                productList.append({'name':product_name, 'pic':product_picture,
                                    'price':product_price,'link':product_link,
                                    'address':address, 'contact_phone':phone,
                                    'tags':tags,'furnitureLocation':furnitureLocation,
                                    'isProduct':1 })

                print_help(var=tags, title='PRODUCT TAGS', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                print_help(var=furnitureLocation, title='PRODUCT FURNITURE LOCATION', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                print_help(var=product_name, title='PRODUCT NAME', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                print_help(var=product_price, title='PRODUCT PRICE', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                print_help(var=product_picture, title='PRODUCT PICTURE', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                print_help(var=product_link, title='PRODUCT LINK', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)

        # Save data to front_page.py
        filename = 'front_page'
        dirname = os.path.dirname(__file__)
        dest_path = os.path.join(dirname, filename)
        save_to_file(dest_path=dest_path, 
                    filename=filename, 
                    itemList = productList)

    except FileExistsError as e:
        print_help(var=e, title='EXCEPTION', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
        print_help(var='FILE DOESNT EXIST', username='GET EVERY PRODUCT',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)


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

                # Get description object
                product_descriptions = driver.find_elements(By.CSS_SELECTOR, 'div.product-detail__content--desc.accordion > div.collapse.show > div')
                
                for desc in product_descriptions:
                    # Get description Text and Preprocess it
                    product_desc = desc.get_attribute('innerHTML')

                    char_to_replace = {
                    '&nbsp;':' ',
                    '\n':' ',
                    '\t':'',
                    ':':'',
                    'cm':'cm ',
                    'kg': 'kg ',
                    '.':'. ',
                    ')':' ',
                    'Bahan':' Bahan',
                    }
                    product_desc = replace_multiple_tags(product_desc,'<','>')
                    product_desc = replace_multiple_char(product_desc,char_to_replace)

                    # Remove Excess Whitespace in the middle of the string
                    product_desc = re.sub('\s{2,}',' ', product_desc)
                    product_desc = product_desc.encode('ascii', 'ignore').decode()
                    product_desc = product_desc.strip()
                    splitted_info = product_desc.split()

                    # Get Material from Description
                    material = ''
                    try:
                        res = re.search(r'\b(?:[dD]ibuat|[bB]ahan)[^.]+\b',product_desc)
                        material = res.group(0)

                        material = material.strip()
                        material = replace_multiple_char(material, SohoID_MATERIAL_REPLACE)

                        material = material.strip()
                        material = replace_multiple_char(material, SohoID_HARD_REMOVE_MATERIAL)

                        material = material.strip()
                        material = re.sub(r'^,\s{0,}?','',material)
                        material = re.sub(r',\s{0,}?$','',material)
                        material = re.sub(r'\s?,\s?',',',material)

                        material = material.strip()
                        material = replace_multiple_char(material, SohoID_HARD_REMOVE_MATERIAL_2)
                        material = material.strip()

                    except AttributeError as ae:
                        print_help(var=ae, title='EXCEPTION REGEX MATERIAL', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var='REGEX MATERIAL #1 FAILED', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)

                    # Get Color from Description
                    colorIndex = -1
                    if 'Warna' in splitted_info:
                        colorIndex = splitted_info.index('Warna')
                    elif 'warna' in splitted_info:
                        colorIndex = splitted_info.index('warna')

                    color = ''
                    if colorIndex > 0:
                        indexCounting = 1
                        if splitted_info[colorIndex + 1].lower() == 'yang':
                            indexCounting = 2

                        while(1):
                            if colorIndex + indexCounting >= len(splitted_info) or \
                                '(' in splitted_info[colorIndex + indexCounting].lower() or \
                                    'bahan' in splitted_info[colorIndex + indexCounting].lower() or \
                                        'yang' in splitted_info[colorIndex + indexCounting].lower():
                                break

                            if '.' in splitted_info[colorIndex + indexCounting]:
                                color += splitted_info[colorIndex + indexCounting] + ' '
                                break

                            color += splitted_info[colorIndex + indexCounting] + ' '
                            indexCounting += 1
                        
                        color = color.lower().replace('-','').replace('top','').replace('  ',' ')
                        color = color.strip()
                        color = re.sub('\s{2,}',' ', color)
                        color = replace_multiple_char(color, char_to_replace = SohoID_COLOR_REPLACE)
                        color = replace_multiple_char(color, char_to_replace = SohoID_COLOR_REPLACE)
                    
                    if color == '':
                        color_contains = ['grey', 'brown', 'pink', 'natural', 'tone', 'cream', 'ivory', 'tosca', 'nature', 'white', 'black', 'green']
                        link = data['link']
                        for c in color_contains:
                            if c in link:
                                color = c
                                break
                            else:
                                color = 'ivory'

                    color = color.replace('.','')

                    # Get Dimension from Description
                    dimension_length = ''
                    dimension_width  = ''
                    dimension_height = ''
                    dimension_unit = 'cm'

                    try:
                        res = re.search(r'\bP(?:anjang)?\s([\d-]+)\s(?:cm|m)?(?:\s)?(?:L|Kedalaman)?\s([\d-]+)\s(?:cm|m)?(?:\s)?T(?:inggi)?\s([\d-]+)\s(?:cm|m)?\b',product_desc)
                        dimension_length = res.group(1)
                        dimension_width = res.group(2)
                        dimension_height = res.group(3)

                        if '-' in dimension_length:
                            tmp_num1 = dimension_length.split('-')[0] if dimension_length.split('-')[0] else 0
                            tmp_num2 = dimension_length.split('-')[1] if dimension_length.split('-')[1] else 0
                            dimension_length = str((float(tmp_num1) + float(tmp_num2)) / 2)

                        if '-' in dimension_width:
                            tmp_num1 = dimension_width.split('-')[0] if dimension_width.split('-')[0] else 0
                            tmp_num2 = dimension_width.split('-')[1] if dimension_width.split('-')[1] else 0
                            dimension_width = str((float(tmp_num1) + float(tmp_num2)) / 2)

                        if '-' in dimension_height:
                            tmp_num1 = dimension_height.split('-')[0] if dimension_height.split('-')[0] else 0
                            tmp_num2 = dimension_height.split('-')[1] if dimension_height.split('-')[1] else 0
                            dimension_height = str((float(tmp_num1) + float(tmp_num2)) / 2)
                    except AttributeError as ae:
                        print_help(var=ae, title='EXCEPTION REGEX DIMENSION', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                        print_help(var='REGEX DIMENSION #1 FAILED', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)

                        try:
                            res = re.search(r'P(?:anjang)?\s([\d-]+)\s(?:cm|m)?(?:\s)?(?:L|Kedalaman)?\s([\d-]+)\s(?:cm|m)?(?:\s)?T(?:inggi)?\s([\d-]+)\s(?:cm|m)?\b',product_desc)
                            dimension_length = res.group(1)
                            dimension_width = res.group(2)
                            dimension_height = res.group(3)

                            if '-' in dimension_length:
                                tmp_num1 = dimension_length.split('-')[0] if dimension_length.split('-')[0] else 0
                                tmp_num2 = dimension_length.split('-')[1] if dimension_length.split('-')[1] else 0
                                dimension_length = str((float(tmp_num1) + float(tmp_num2)) / 2)

                            if '-' in dimension_width:
                                tmp_num1 = dimension_width.split('-')[0] if dimension_width.split('-')[0] else 0
                                tmp_num2 = dimension_width.split('-')[1] if dimension_width.split('-')[1] else 0
                                dimension_width = str((float(tmp_num1) + float(tmp_num2)) / 2)

                            if '-' in dimension_height:
                                tmp_num1 = dimension_height.split('-')[0] if dimension_height.split('-')[0] else 0
                                tmp_num2 = dimension_height.split('-')[1] if dimension_height.split('-')[1] else 0
                                dimension_height = str((float(tmp_num1) + float(tmp_num2)) / 2)
                        
                        except AttributeError as ae:
                            print_help(var=ae, title='EXCEPTION REGEX DIMENSION', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                            print_help(var='REGEX DIMENSION #2 FAILED', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)

                            try:
                                res = re.search(r'P(?:anjang)?\s?([\d,.-]+)\s(?:cm|m)?(?:\s)?(?:L|Kedalaman)?\s?([\d,.-]+)\s?(?:cm|m)?(?:\s)?T(?:inggi)?\s?([\d,.-]+)\s(?:cm|m)?\b',product_desc)
                                dimension_length = res.group(1)
                                dimension_width = res.group(2)
                                dimension_height = res.group(3)
                                char_to_replace = {
                                    ',':'.',
                                }
                                dimension_length = replace_multiple_char(dimension_length, char_to_replace)
                                dimension_width = replace_multiple_char(dimension_width, char_to_replace)
                                dimension_height = replace_multiple_char(dimension_height, char_to_replace)

                                if '-' in dimension_length:
                                    tmp_num1 = dimension_length.split('-')[0] if dimension_length.split('-')[0] else 0
                                    tmp_num2 = dimension_length.split('-')[1] if dimension_length.split('-')[1] else 0
                                    dimension_length = str((float(tmp_num1) + float(tmp_num2)) / 2)

                                if '-' in dimension_width:
                                    tmp_num1 = dimension_width.split('-')[0] if dimension_width.split('-')[0] else 0
                                    tmp_num2 = dimension_width.split('-')[1] if dimension_width.split('-')[1] else 0
                                    dimension_width = str((float(tmp_num1) + float(tmp_num2)) / 2)

                                if '-' in dimension_height:
                                    tmp_num1 = dimension_height.split('-')[0] if dimension_height.split('-')[0] else 0
                                    tmp_num2 = dimension_height.split('-')[1] if dimension_height.split('-')[1] else 0
                                    dimension_height = str((float(tmp_num1) + float(tmp_num2)) / 2)
                            
                            except AttributeError as ae:
                                print_help(var=ae, title='EXCEPTION REGEX DIMENSION', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                                print_help(var='REGEX DIMENSION #3 FAILED', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)

                                try:
                                    res = re.search(r'P(?:anjang)?\s?([\d,.-]+)\s(?:cm|m)?(?:\s)?(?:L|Kedalaman)?\s([\d,.-]+)\s(?:cm|m)?(?:\s)?L(?:inggi)?\s?([\d,.-]+)\s(?:cm|m)?\b',product_desc)
                                    dimension_length = res.group(1)
                                    dimension_width = res.group(2)
                                    dimension_height = res.group(3)
                                    char_to_replace = {
                                        ',':'.',
                                    }
                                    dimension_length = replace_multiple_char(dimension_length, char_to_replace)
                                    dimension_width = replace_multiple_char(dimension_width, char_to_replace)
                                    dimension_height = replace_multiple_char(dimension_height, char_to_replace)

                                    if '-' in dimension_length:
                                        tmp_num1 = dimension_length.split('-')[0] if dimension_length.split('-')[0] else 0
                                        tmp_num2 = dimension_length.split('-')[1] if dimension_length.split('-')[1] else 0
                                        dimension_length = str((float(tmp_num1) + float(tmp_num2)) / 2)

                                    if '-' in dimension_width:
                                        tmp_num1 = dimension_width.split('-')[0] if dimension_width.split('-')[0] else 0
                                        tmp_num2 = dimension_width.split('-')[1] if dimension_width.split('-')[1] else 0
                                        dimension_width = str((float(tmp_num1) + float(tmp_num2)) / 2)

                                    if '-' in dimension_height:
                                        tmp_num1 = dimension_height.split('-')[0] if dimension_height.split('-')[0] else 0
                                        tmp_num2 = dimension_height.split('-')[1] if dimension_height.split('-')[1] else 0
                                        dimension_height = str((float(tmp_num1) + float(tmp_num2)) / 2)
                                
                                except AttributeError as ae:
                                    print_help(var=ae, title='EXCEPTION REGEX DIMENSION', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                                    print_help(var='REGEX DIMENSION #4 FAILED', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)


                    print_help(var=product_desc, title='PRODUCT DESC', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                    print_help(var=material, title='PRODUCT MATERIAL', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                    print_help(var=dimension_length, title='PRODUCT DIMENSION LENGTH', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                    print_help(var=dimension_width, title='PRODUCT DIMENSION WIDTH', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                    print_help(var=dimension_height, title='PRODUCT DIMENSION HEIGHT', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                    print_help(var=dimension_unit, title='DIMENSION UNIT', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                    print_help(var=color, title='PRODUCT COLOR', username='GET EVERY DETAIL',save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
                    
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
                            'additional_desc': '',
                            'color': color,
                            'description': product_desc,
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
    print_help(var='RUNNING SOHO ID WEB SCRAPING....', username='MAIN', save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)

    get_all_link(driver=driver)
    phone, address = get_contact(driver=driver)
    get_every_product(driver=driver, phone=phone, address=address)
    get_every_detail(driver=driver)

    driver.quit()

    print_help(var='FINISHED SOHO ID WEB SCRAPING....', username='MAIN', save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time)))

if __name__ == '__main__':
    main()