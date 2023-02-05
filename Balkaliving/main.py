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
    url = 'https://www.balkaliving.com/about-us/'
    
    driver.get(url)
    contact_object = driver.find_elements(By.CSS_SELECTOR, 'aside#text-4 > h3 + div.textwidget')
    
    tmp_phone = None
    tmp_address = None
    
    phone_replace = {
        '+':'',
        '(':'',
        ')':'',
        '-':''
    }
    address_replace = {
        'WORKSHOP':''
    }
    for contact in contact_object:
        tmp_contact = contact.get_attribute('innerHTML')
        tmp_contact = tmp_contact.split('Phone')

        tmp_address = tmp_contact[0]
        tmp_phone = tmp_contact[1]

        tmp_phone = replace_multiple_tags(tmp_phone, 'E-Mail', '.com', '')
        tmp_phone = replace_multiple_tags(tmp_phone, '<br', '>', '')
        tmp_phone = replace_multiple_char(tmp_phone, char_to_replace=phone_replace)
        tmp_phone = tmp_phone.strip()

        tmp_address = replace_multiple_char(tmp_address, char_to_replace=address_replace)
        tmp_address = replace_multiple_tags(tmp_address, '<br', '>', '')
        tmp_address = tmp_address.strip()
    
    print(tmp_phone)
    print(tmp_address)

    return tmp_phone, tmp_address

def get_every_product(driver, phone, address):
    PAGES = 10
    productList = []
    for page in range(1, PAGES + 1):
        url = f'https://www.balkaliving.com/product-category/furniture/page/{page}/'
        driver.get(url)

        try:
            # Get Product Names, Pictures, Prices, Links object
            product_names = driver.find_elements(By.CSS_SELECTOR, 'div.product-caption > h3')
            product_pictures = driver.find_elements(By.CSS_SELECTOR, 'div.product-type-simple > a > img')
            product_prices = driver.find_elements(By.CSS_SELECTOR, 'div.product-caption > span.price > span.amount')
            product_links = driver.find_elements(By.CSS_SELECTOR,'div.product-type-simple > a[title]')

            for name, pics, price, links in zip(product_names,product_pictures,product_prices,product_links):
                # Get Product name and preprocess it
                product_name = name.get_attribute('innerHTML')
                product_name = product_name.encode('ascii', 'ignore').decode()
                product_name = product_name.title()

                # Get Product picture, price, and link and preprocess it
                product_picture = pics.get_attribute('src')
                product_price = price.get_attribute('innerHTML').replace('IDR&nbsp;','').replace('.','')
                product_link = links.get_attribute('href')
                
                # Print to CLI
                print('==================')
                print(product_name)
                print(product_picture)
                print(product_price)
                print(product_link)
                print('==================')
                # Append each attribute to dict
                productList.append({'name':product_name,'pic':product_picture,
                                    'price' :product_price, 'link' :product_link,
                                    'address':address, 'contact_phone':phone})
                
            print('PRODUCT LIST')
            print(productList)

        except WebDriverException as e: 
            print(e)   

    # Save file to front_page.py
    filename = 'front_page'
    dirname = os.path.dirname(__file__)
    dest_path = os.path.join(dirname, filename)
    save_to_file(dest_path=dest_path, 
                filename=filename, 
                itemList = productList)
    

def get_every_detail(driver):
    try:
        # Import front_page from front_page
        try:
            from .front_page import front_page as DATASET
        except ImportError as e:
            print(e)
            from front_page import front_page as DATASET

        dataset_copy = DATASET
        for data in dataset_copy:
            # Get a link of each dataset
            driver.get(data['link'])
            driver.implicitly_wait(5)

            try:
                # Get Product Descriptions and Cleaned It
                product_descriptions = driver.find_element(By.CSS_SELECTOR, 'div[itemprop="description"]')
                product_descriptions = product_descriptions.get_attribute('innerHTML')

                # A Dict of Chars and what to replace
                char_to_replace = {
                    '<p>':'',
                    '</p>':'',
                    '&nbsp;':' ',
                    '</span>':'',
                    '\n':' ',
                    '\t':''
                }
                
                # Get product descriptions and preprocess it
                product_descriptions = product_descriptions.strip()
                product_descriptions = replace_multiple_char(product_descriptions,char_to_replace)
                product_descriptions = replace_multiple_tags(product_descriptions, '<', '>')
                product_descriptions = product_descriptions.encode('ascii', 'ignore').decode()
                
                # Get Product Tags and preprocess it
                product_tags = driver.find_elements(By.CSS_SELECTOR, 'ul.inline-tags > li > a')
                
                tagsList = []
                for tag in product_tags:
                    product_tag = tag.get_attribute('innerHTML')
                    product_tag = product_tag.replace('#','')
                    tagsList.append(product_tag)

                product_additional_descriptions = driver.find_element(By.CSS_SELECTOR, 'div#tab-description')
                product_additional_descriptions = product_additional_descriptions.get_attribute('innerHTML')
                product_additional_descriptions = product_additional_descriptions.replace('Product Description','')
                product_additional_descriptions = re.sub(r'\n\s*\n', '\n\n', product_additional_descriptions)
                product_additional_descriptions = re.sub('\s{2,}',' ',product_additional_descriptions)
                
                product_additional_descriptions = replace_multiple_char(product_additional_descriptions,char_to_replace)
                product_additional_descriptions = product_additional_descriptions.strip()
                product_additional_descriptions = replace_multiple_tags(product_additional_descriptions, '<', '>')
                product_additional_descriptions = product_additional_descriptions.encode('ascii', 'ignore').decode()
                
                # Get "Material" from description by splitting it to words
                splitted_desc = product_additional_descriptions.split()
                material = ''
                for index,desc in enumerate(splitted_desc):
                    if desc.lower() == 'bahan' or desc.lower() == 'material':
                        count = 1
                        while(1):
                            if index + count < len(splitted_desc) and \
                            (splitted_desc[index+count] != ',' and \
                            splitted_desc[index+count] != 'Dimensi' and splitted_desc[index+count] != 'Dimension'):
                                material += splitted_desc[index+count] + ' '
                            else:
                                break
                            count += 1

                material = material.lower().strip()
                material = replace_multiple_char(material, char_to_replace = Balkaliving_MATERIAL_REPLACE)
                material = material.strip()
                material = replace_multiple_char(material, Balkaliving_HARD_REMOVE_MATERIAL)
                material = material.strip()
                material = re.sub(r'^,\s{0,}?','',material)
                material = re.sub(r',\s{0,}?$','',material)
                material = re.sub(r'\s?,\s?',',',material)
                material = material.strip()
                
                # Get Product Dimension object
                product_additional_information = driver.find_element(By.CSS_SELECTOR, 'div#tab-additional_information')
                product_additional_information = product_additional_information.get_attribute('innerHTML')
                product_additional_information = product_additional_information.replace('Additional Information','')

                product_additional_information = replace_multiple_char(product_additional_information,char_to_replace)
                product_additional_information = replace_multiple_tags(product_additional_information, '<', '>')
                product_additional_information = product_additional_information.encode('ascii', 'ignore').decode()
                product_additional_information = re.sub('\s{2,}',' ',product_additional_information)
                product_additional_information = product_additional_information.strip()

                
                # Get dimension and weight from additional information 
                splitted_info = product_additional_information.split()
                data['dimension_length'] = ''
                data['dimension_width'] = ''
                data['dimension_height'] = ''
                data['dimension_unit'] = ''
                data['weight'] = ''
                data['weight_unit'] = ''
                data['color'] = ''
                for index,info in enumerate(splitted_info):
                    if info.lower() == 'weight':
                        data['weight'] = str(splitted_info[index+1])
                        data['weight_unit'] = str(splitted_info[index+2])

                    elif info.lower() == 'dimensions' or info.lower() == 'dimension':
                        data['dimension_length'] = str(splitted_info[index + 1])
                        data['dimension_width'] = str(splitted_info[index + 3])

                        if index + 5 < len(splitted_info):
                            data['dimension_height'] = str(splitted_info[index + 5])
                            data['dimension_unit'] = str(splitted_info[index+6])

                        elif splitted_info[index + 4] == 'cm' or splitted_info[index + 4] == 'm':
                                data['dimension_unit'] = str(splitted_info[index + 4])

                        
                    elif info.lower() == 'color':
                        string = splitted_info[index+1:]
                        string = "".join(string)
                        string = string.strip()
                        string = string.lower().replace(',','')
                        data['color'] = replace_multiple_char(string,char_to_replace=Balkaliving_COLOR_REPLACE)

                location = []
                if 'tidur' in product_descriptions:
                    location.append('kamar tidur')
                else:
                    location.append('ruang keluarga')
                    location.append('ruang tamu')

                data['isProduct'] = 1
                data['furnitureLocation'] = location
                data['description'] = product_descriptions
                data['tags'] = tagsList
                data['material'] = material
                data['additional_desc'] = product_additional_descriptions
                
                print('================')
                print(product_descriptions)
                print('ADDITIONAL DESC')
                print(product_additional_information)
                print('MATERIAL', material)
                print('DIMENSION LENGTH', data['dimension_length'])
                print('DIMENSION WIDTH', data['dimension_width'])
                print('DIMENSION HEIGHT', data['dimension_height'])
                print('DIMENSION UNIT', data['dimension_unit'])
                print('COLOR ',data['color'])
                print('WEIGHT ',data['weight'])
                print('WEIGHT UNIT',data['weight_unit'])
                print('================')

                print("COMPLETE DATA")
                print(data)
            except WebDriverException as e:
                print('INSIDE EVERY PRODUCT')
                print(e)

         # Check Any Duplicate Name Because in The Database, Every Item is store with Slug
        non_duplicate = {}

        for data in dataset_copy:
            non_duplicate[data['name']] = data

        dataset_copy = []
        for data in non_duplicate:
            dataset_copy.append(non_duplicate[data])
            
        # Save file to all_data.py
        filename = 'all_data'
        dirname = os.path.dirname(__file__)
        dest_path = os.path.join(dirname, filename)
        save_to_file(dest_path=dest_path, 
                        filename=filename, 
                        itemList = dataset_copy)

    except WebDriverException as e:
        print('ERROR IN SECOND HALF')
        print(e)

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

    print('RUNNING BALKALIVING WEB SCRAPING....')

    phone, address = get_contact(driver=driver)
    get_every_product(driver=driver, phone=phone, address=address)
    get_every_detail(driver=driver)
    
    driver.quit()

    print('FINISHED BALKALIVING WEB SCRAPING....')
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time)))

if __name__ == '__main__':
    main()