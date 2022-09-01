import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException,WebDriverException

import re
# from selenium.webdriver.common.keys import Keys

def replace_text_in_between(text,start,end,replace_with=''):
    idx_start = text.index(start) if start in text else None
    idx_end = text.index(end) + len(end) if end in text else None
    
    if idx_start == None or idx_end == None:
        return text
    return str(text[0:idx_start]) + replace_with + str(text[idx_end:])

def replace_multiple_char(text, char_to_replace):
    for key, value in char_to_replace.items():
        text = text.replace(key, value)

    return text

def replace_multiple_tags(text, start, end, replace_with=''):
    occurences = text.count(start)

    for _ in range(occurences):
        text = replace_text_in_between(text,start,end,replace_with)
    return text

def save_to_file(filename, itemList, automatic_overwrite = True):
    dirname = os.path.dirname(__file__)
    dest_path = os.path.join(dirname, filename)
    with open(dest_path + '.txt','w') as file:
        file.write(filename + ' = [')
        for count,product in enumerate(itemList):
            file.write(str(product))

            if count == len(itemList):
                file.write('\n')
            else:
                file.write(',\n')

        file.write(']')
    file.close()


    FILE_NAME = dest_path
    try:
        os.rename(FILE_NAME + '.txt', FILE_NAME + '.py')

    except FileExistsError:
        chc = '1'
        if not automatic_overwrite:
            chc = input('{0}.py Already Exist. Do You Want to Overwrite ? (0/1)'.format(FILE_NAME))
        
        if chc == '1':
            os.remove(FILE_NAME + '.py')
            os.rename(FILE_NAME + '.txt',FILE_NAME + '.py')

    finally:
        print('Saving File Finished\n\n')
        if automatic_overwrite:
            print('File Overwrite Automatically')


ADDRESS = 'Jl Stasiun Timur No 40, Bandung 40111'
PHONE = '6281284801166'

s = Service('C:/SeleniumDrivers/chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.implicitly_wait(15)

def get_category_and_links():
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
            print('======================')
            print(tmp_data[data]['title'])
            print(tmp_data[data]['link'])
            print(tmp_data[data]['category'])
            print('======================')
            collections.append({
                'title':tmp_data[data]['title'],
                'link':tmp_data[data]['link'],
                'category':tmp_data[data]['category'],
            })
        
        # Save Links to File
        save_to_file('links',collections)

    except WebDriverException as e:
        print(e)
        print('WEB DRIVER FAILED')

def get_every_product():
        try:
            from links import links as DATASET

            productList = []
            for data in DATASET:
                PAGE = 1
                is_not_found = False
                # Find All Pages until Not Found
                while(1):
                    url = f'{data["link"]}page/{PAGE}/'
                    print(url)
                    driver.get(url)
                    
                    # If Page is Not Found
                    try:
                        is_not_found_object = driver.find_element(By.CSS_SELECTOR, 'div.rt-entry-content > h2')
                        if is_not_found_object.get_attribute('innerHTML') == 'Unfortunately, the page you requested could not be found.':
                            is_not_found = True

                    except WebDriverException as e:
                        print(e)
                        print('PAGE STILL FIND NEXT PAGE')
                    
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

                        print('================')
                        print(data['category'])
                        print(product_name)
                        print(product_price)
                        print(product_picture)
                        print(product_link)
                        print('================')
                        productList.append({ 'name':product_name, 'pic':product_picture,
                                            'price':product_price, 'link': product_link,
                                            'address':ADDRESS, 'contact_phone':PHONE,
                                            'tags':data['category'], 'furnitureLocation':data['category'],
                                            'isProduct':1 })
                    PAGE += 1

            # Save data to front_page.py
            save_to_file('front_page',productList)

        except WebDriverException as e:
            print(e)
            print('SCRAPING FAILED')
        
def get_every_detail():
    try:
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
                                product_color = product_color.split(',')
                                product_color = [ x.strip() for x in product_color if x.strip() and x.strip() != ',' and x.strip() != '.' ]

                            elif tmp_title.lower() == 'material':
                                material = tmp_value.lower()
                                material = material.replace('<br>','')
                                material = material.split(',')
                                material = [ x.strip() for x in material if x.strip() and x.strip() != ',' and x.strip() != '.' ]

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

                        print('================')
                        print(product_desc)
                        print('ADDITIONAL DESC')
                        print(additional_desc)
                        print('MATERIAL', material)
                        print('DIMENSION LENGTH', dimension_length)
                        print('DIMENSION WIDTH', dimension_width)
                        print('DIMENSION HEIGHT', dimension_height)
                        print('DIMENSION UNIT', dimension_unit)
                        print('COLOR ',product_color)
                        print('WEIGHT ',weight)
                        print('WEIGHT UNIT',weight_unit)
                        print('IS AVAILABLE',is_available_object.get_attribute('innerHTML'))
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
        save_to_file('all_data',dataset_copy)

    except FileExistsError as e:
        print(e)
        print('FILE FRONT PAGE DOESNT EXIST')

if __name__ == '__main__':
    import time
    start_time = time.perf_counter()
    get_category_and_links()
    get_every_product()
    get_every_detail()
    import datetime
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time)))