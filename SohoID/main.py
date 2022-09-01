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


ADDRESS = 'Jl. Ibrahim Adjie no. 423 Kiaracondong, Bandung'
PHONE = '022-732 80 790'

s = Service('C:/SeleniumDrivers/chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.implicitly_wait(15)


def get_all_link():
    NAV_LINKS = []
    url = 'https://www.soho.id/'
    driver.get(url)

    try:
        # Get All li with class is__parent
        nav_object = driver.find_elements(By.CSS_SELECTOR, 'li.is__parent')
        
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

            print('===============')
            print('NAV GROUP LINK')
            print(nav_group_link)
            print('NAV GROUP TITLE')
            print(nav_group_title)
            print('===============')
            
            # Add link and title to dictionary
            temp_dict['link'] = nav_group_link
            temp_dict['title'] = nav_group_title
            
            # Get children object
            nav_children_object = nav.find_elements(By.CSS_SELECTOR, 'ul.is__dropdown > li > a')
            childList = []
            for nav_child in nav_children_object:
                # Get Child Link in href in <a></a>
                nav_child_link = nav_child.get_attribute('href')

                # Get Child Title in innerHTML in <a></a>
                nav_child_title = nav_child.get_attribute('innerHTML')
                nav_child_title = nav_child_title.title().strip().lower()

                print('===============')
                print('NAV CHILD LINK')
                print(nav_child_link)
                print('NAV CHILD TITLE')
                print(nav_child_title)
                print('===============')

                # Add Child Link and Title to Dictionary
                childList.append({'link':nav_child_link, 'title':nav_child_title})

            temp_dict['child'] = childList

            NAV_LINKS.append(temp_dict)
            
        print('ALL NAV LINK AND TITLE')
        print(NAV_LINKS)
        
        # Save All Links to File
        save_to_file('links',NAV_LINKS)

    except WebDriverException as e:
        print('ERROR GET ALL LINK')
        print(e)

def get_every_product():
    try:
        # Import Links from 
        from links import links as DATASET
        
        productList = []
        for data in DATASET:
            title = data['title']

            # Loop each child
            for child in data['child']:
                driver.get(child['link'])

                # Names and Links are in the same element
                product_names_and_links = driver.find_elements(By.CSS_SELECTOR, 'a.product__name')
                product_prices = driver.find_elements(By.CSS_SELECTOR,'div.product__price > span:first-child')
                product_pictures = driver.find_elements(By.CSS_SELECTOR, 'a.thumbnail > img')

                for name_link, price,pic in zip(product_names_and_links,product_prices,product_pictures):
                    # Get product name, link , price, and picture
                    product_name = name_link.get_attribute('innerHTML')
                    product_name = product_name.encode('ascii', 'ignore').decode()

                    product_link = name_link.get_attribute('href')
                    product_picture = pic.get_attribute('src')

                    product_price = price.get_attribute('innerHTML')

                    char_to_replace = {
                    'IDR':'',
                    '.00':'',
                    ',':'',
                    }
                    product_price = replace_multiple_char(product_price,char_to_replace)
                    product_price = product_price.strip()
                   
                    tags = [child['title']]
                    furnitureLocation = [ title.lower() ]

                    if title.lower() == 'ruang kerja':
                        furnitureLocation = ['ruang kerja','kamar tidur']

                    if title.lower() == 'dapur ruang makan':
                        furnitureLocation = ['dapur','ruang makan']

                    if title == 'Seri SOHO':
                        tags = ['Seri SOHO',child['title']]
                        furnitureLocation = []

                    # Append to productList
                    productList.append({'name':product_name, 'pic':product_picture,
                                        'price':product_price,'link':product_link,
                                        'address':ADDRESS, 'contact_phone':PHONE,
                                        'tags':tags,'furnitureLocation':furnitureLocation,
                                        'isProduct':1 })

                    print('=================')
                    print(tags)
                    print(furnitureLocation)
                    print(product_name)
                    print(product_link)
                    print(product_picture)
                    print(product_price)
                    print('=================')
        
        # Save data to front_page.py
        save_to_file('front_page',productList)

    except FileExistsError as e:
        print('FILE DOESNT EXIST')
        print(e)

def get_every_detail():
    try:
        from front_page import front_page as DATASET
        dataset_copy = []
        for data in DATASET:
            try:
                driver.get(data['link'])

                # Get description object
                product_descriptions = driver.find_elements(By.CSS_SELECTOR, 'div.spesification')
                
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
                        char_to_replace = {
                        'dibuat':'',
                        'Dibuat':'',
                        'bahan':'',
                        'Bahan':'',
                        'dengan':'',
                        }
                        material = replace_multiple_char(material,char_to_replace)
                        material = material.strip()
                    except AttributeError as ae:
                        print('REGEX MATERIAL FAILED')
                        print(ae)
                    finally:
                        material = material.split(',')
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
                        print('REGEX DIMENSION FAILED')
                        print(ae)
                        

                    print('================')
                    print(product_desc)
                    print(splitted_info)
                    print('MATERIAL', material)
                    print('DIMENSION LENGTH', dimension_length)
                    print('DIMENSION WIDTH', dimension_width)
                    print('DIMENSION HEIGHT', dimension_height)
                    print('DIMENSION UNIT', dimension_unit)
                    print('COLOR ',color)
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
                            'additional_desc': '',
                            'color': color.split(','),
                            'description': product_desc,
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
    get_all_link()
    get_every_product()
    get_every_detail()
    import datetime
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time)))