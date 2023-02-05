from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

import datetime
import time
import re
import random
import os 
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent_dir = current + os.sep + os.pardir
sys.path.append(parent_dir)

from helper_func.helper import *
from dict_clean import *

from dotenv import load_dotenv
load_dotenv()

def get_every_product(driver):
        try:
            links = ['https://www.olx.co.id/surabaya-kota_g4000216/q-custom-furniture',
                    'https://www.olx.co.id/surabaya-kota_g4000216/q-jasa-custom-furniture',
                    'https://www.olx.co.id/surabaya-kota_g4000216/q-jasa-interior-design',
                    'https://www.olx.co.id/surabaya-kota_g4000216/q-custom-interior']
            # links = ['https://www.olx.co.id/surabaya-kota_g4000216/q-custom-interior']
            productList = []
            count_item = 0

            for link in links:
                driver.get(link)

                if len(driver.find_elements(By.CSS_SELECTOR, 'h3._3lWQO > span')) > 0:
                    print('PAGE NOT FOUND, CONTINUE NEXT LINK')
                    continue

                print('===========================')
                print('BTN LOAD MORE LEN')
                print(len(driver.find_elements(By.CSS_SELECTOR, 'button[data-aut-id="btnLoadMore"]')))
                print('===========================')
                if len(driver.find_elements(By.CSS_SELECTOR, 'button[data-aut-id="btnLoadMore"]')) > 0:
                    load_more_button = driver.find_element(By.CSS_SELECTOR, 'button[data-aut-id="btnLoadMore"]')
                    load_more_button.click()

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
                
                    # driver.execute_script("""document.querySelector('button[data-aut-id="btnLoadMore"]').click()""")

                # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li[data-aut-id="itemBox"] > a > div > span[data-aut-id="itemTitle"]')))
                time.sleep(3)

                # Get Product Names, Prices, Pictures, and Links
                product_names = driver.find_elements(By.CSS_SELECTOR, 'li[data-aut-id="itemBox"] > a > div > span[data-aut-id="itemTitle"]')
                product_prices = driver.find_elements(By.CSS_SELECTOR,'li[data-aut-id="itemBox"] > a > div > span[data-aut-id="itemPrice"]')
                
                product_links = driver.find_elements(By.CSS_SELECTOR,'li[data-aut-id="itemBox"] > a')
                product_pictures = driver.find_elements(By.CSS_SELECTOR, 'li[data-aut-id="itemBox"] > a > figure[data-aut-id="itemImage"] > img')
                product_addresses = driver.find_elements(By.CSS_SELECTOR, 'li[data-aut-id="itemBox"] > a > div > div > span[data-aut-id="item-location"]')
                for name, price, links, pic, address in zip(product_names, product_prices, product_links, product_pictures, product_addresses):

                    product_name = name.get_attribute('innerHTML')
                    product_name = product_name.encode('ascii', 'ignore').decode()
                    product_name = product_name.replace('&amp;','dan')

                    product_price = price.get_attribute('innerHTML')
                    char_to_replace = {
                        '<!--':'',
                        '-->':'',
                        ',':'',
                        '&amp;':'dan',
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
                    furniture_location = []
                    tmp_product_name = product_name.lower()
                    if tmp_product_name.count('lemari'):
                        furniture_location += ['kamar tidur','ruang keluarga']
                    elif tmp_product_name.count('dipan'):
                        furniture_location += ['kamar tidur']
                    elif tmp_product_name.count('kitchen'):
                        furniture_location += ['dapur']
                    else:
                        furniture_location += ['kamar tidur', 'kamar mandi', 'ruang makan', 'dapur', 'ruang keluarga', 'ruang tamu']

                    print('=============')
                    print(product_name)
                    print(product_price)
                    print(product_picture)
                    print(product_link)
                    print('=============')
                    productList.append({'name':product_name, 'pic':product_picture,
                                        'price':product_price,'link':product_link,
                                        'address':product_address, 'furnitureLocation': furniture_location,
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
            print(e)
            print('SCRAPING FAILED')
        

def get_every_detail(driver):
    # Try Login to get Phone Number
    try:
        email = os.environ.get('EMAIL_OLX')
        password = os.environ.get('PASSWORD_OLX')
        driver.get('http://olx.co.id')

        print('WAIT VISIBILITY LOGIN BUTTON ELEMENT')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'button[data-aut-id="btnLogin"]')
                )
            )
        print('GET LOGIN BUTTON ELEMENT')

        login_button = driver.find_element(By.CSS_SELECTOR,'button[data-aut-id="btnLogin"]')
        login_button.click()

        print('GET EMAIL BUTTON ELEMENT')
        WebDriverWait(driver, 10).until(
            EC.visibility_of_any_elements_located(
                (By.CSS_SELECTOR, 'button[data-aut-id="emailLogin"]')
                )
            )
        email_login = driver.find_element(By.CSS_SELECTOR,'button[data-aut-id="emailLogin"]')
        email_login.click()
        

        print('WAIT VISIBILITY INPUT EMAIL ELEMENTS')
        WebDriverWait(driver, 10).until(
            EC.visibility_of_any_elements_located(
                (By.CSS_SELECTOR, 'input#email_input_field')
                )
            )

        time.sleep(3)
        print('INSERT EMAIL INPUT')
        email_input = driver.find_element(By.CSS_SELECTOR,'input#email_input_field')
        email_input.clear()
        for letter in email:
            email_input.send_keys(letter)
            time.sleep(random.random())
        
        
        print('SUBMIT EMAIL INPUT')
        submit_button = driver.find_element(By.CSS_SELECTOR,'button.rui-39-wj.rui-3mpqt.rui-1JPTg._2sWUW')
        print('DID IT FOUND THE ELEMENT ',submit_button)
        time.sleep(3)
        submit_button.click()

        time.sleep(3)
        print('WAIT VISIBILITY INPUT PASSWORD ELEMENTS')
        WebDriverWait(driver, 10).until(
            EC.visibility_of_any_elements_located(
                (By.CSS_SELECTOR, 'input#password')
                )
        )

        time.sleep(3)
        print('INSERT PASSWORD INPUT')
        password_input = driver.find_element(By.CSS_SELECTOR,'input#password')
        password_input.send_keys(password)

        print('SUBMIT PASSWORD')
        submit_login = driver.find_element(By.CSS_SELECTOR,'button[data-aut-id="login-form-submit"]')
        time.sleep(3)
        submit_login.click()

        time.sleep(5)

    except WebDriverException as e:
        print(e)
        print('NOT LOGGED IN')

    # Try to get information after logged in
    try:
        # Try saved dataset
        try:
            from .front_page import front_page as DATASET
        except ImportError as e:
            print(e)
            from front_page import front_page as DATASET

        dataset_copy = []
        count_item = 0
       
        for data in DATASET:
            try:
                driver.get(data['link'])
                # Get Description and Additional Description object
                product_descriptions = driver.find_elements(By.CSS_SELECTOR, 'div[data-aut-id="itemDescriptionContent"]')
                additional_descs_object = driver.find_elements(By.CSS_SELECTOR, 'div[data-aut-id="itemParams"] > div > div > div')
                
                show_contact_button = driver.find_element(By.CSS_SELECTOR,'button[data-aut-id="btnChat"] + div > div + div')
                show_contact_button.click()

                WebDriverWait(driver, 15).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, 'button[data-aut-id="btnChat"] + div > div')
                        )
                )
                contact_phone = driver.find_element(By.CSS_SELECTOR, 'button[data-aut-id="btnChat"] + div > div')
                contact_phone = contact_phone.get_attribute('innerHTML')
                contact_phone = contact_phone.replace('+','')
                
                print('===========================')
                print('CONTACT PHONE')
                print(contact_phone)
                print('===========================')

                for desc in product_descriptions:
                    # Get Product Description and Preprocess it
                    product_desc = desc.get_attribute('innerHTML')
                    product_desc = product_desc.encode('ascii', 'ignore').decode()
                    char_to_replace = {
                        '&amp;':'dan',
                        '&lt;br&gt;':'',
                        'br&gt;':'',
                        '&lt&gt;':'',
                        '&lt;':'',
                        '</td>':'\n\n',
                        '</p>':'%^&br%^&'
                    }
                    product_desc = replace_multiple_char(product_desc, char_to_replace)
                    product_desc = replace_multiple_tags(product_desc,'<p','>')
                    char_to_replace = {
                        '%^&br%^&':'<br>'
                    }
                    product_desc = replace_multiple_char(product_desc, char_to_replace)

                    product_desc = re.sub(r'\s{2,}',' ',product_desc)

                    # Get Additional Description and Preprocess it
                    additional_description = ''
                    product_color = 'custom'
                    material = 'custom'
                    tags = ''
                    dimension_length = ''  
                    dimension_width = ''
                    dimension_height = ''
                    dimension_unit = 'cm'
                    weight = ''
                    weight_unit = 'kg'
                    
                    for count, add_desc in enumerate(additional_descs_object):
                        tmp = add_desc.get_attribute('innerHTML')

                        print('===========================')
                        print(tmp)
                        print('===========================')
                        char_to_replace = {
                            '&amp;':'dan',
                            '<!--':'',
                            '-->':'',
                            'Tipe':'Tipe: ',
                            'tipe':'Tipe: ',
                            'Kondisi':'Kondisi: ',
                            'kondisi':'Kondisi: '
                        }
                        tmp = replace_multiple_char(tmp, char_to_replace)
                        tmp = replace_multiple_tags(tmp, '<','>')
                        
                        additional_description += tmp
                        if count % 2 == 0:
                            additional_description += '<br>'

                    print('==================')
                    print('ORIGINAL LINK')
                    print(data['link'])

                    print(product_desc)
                    print('ADDITIONAL DESCRIPTION')
                    print(additional_description)

                    print('COLOR',product_color)
                    print('MATERIAL',material)
                    print('DIMENSION LENGTH',dimension_length)
                    print('DIMENSION WIDTH',dimension_width)
                    print('DIMENSION HEIGHT',dimension_height)
                    print('DIMENSION UNIT',dimension_unit)
                    print('WEIGHT',weight)
                    print('WEIGHT UNIT',weight_unit)
                    print('FURNITURE LOCATION', data['furnitureLocation'])
                    print('CONTACT PHONE', contact_phone)
                    print('==================')
                    
                    dataset_object = {
                            'name': data['name'],
                            'pic': data['pic'],
                            'price': data['price'],
                            'link': data['link'], 
                            'address': data['address'], 
                            'contact_phone':  contact_phone,
                            'tags': tags,
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
                count_item += 1
            except WebDriverException as e:
                print(e)
                print('ERROR IN FOR DATASET')
        
        # Check Any Duplicate Name Because in The Database, Every Item is store with Slug
        non_duplicate = {}

        for data in dataset_copy:
            non_duplicate[data['name']] = data

        print('TOTAL ITEM SCRAPED')
        print(count_item)
        
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

    driver.implicitly_wait(30)
    driver.delete_all_cookies()
    start_time = time.perf_counter()
    
    print('RUNNING OLX WEB SCRAPING....')

    get_every_product(driver=driver)
    get_every_detail(driver=driver)

    driver.quit()

    print('FINSIHED OLX WEB SCRAPING....')
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time)))

if __name__ == '__main__':
    main()