import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException,WebDriverException
from selenium.webdriver.chrome.options import Options
import time
import re
import requests
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

ADDRESS = 'NOT YET'
PHONE = '022-732 80 790'

# https://chromedriver.storage.googleapis.com/index.html
s = Service('C:/SeleniumDrivers/chromedriver.exe')


# driver = webdriver.Chrome(service=s,options=options)
# ==== 
options = Options()
# options.add_argument("--headless")
# options.add_argument('--disable-gpu')
# options.add_argument('--no-sandbox')
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options.add_argument('user-agent={0}'.format(user_agent))

driver = webdriver.Chrome(service=s, options=options)
driver.implicitly_wait(15)


def get_every_product():
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
                    print('=============')
                    print(product_name)
                    print(product_price)
                    print(product_picture)
                    print(product_link)
                    print('=============')
                    productList.append({'name':product_name, 'pic':product_picture,
                                        'price':product_price,'link':product_link,
                                        'address':product_address,
                                        'isProduct':0 })
            
            print('TOTAL ITEM')
            print(count_item)

            # Save data to front_page.py
            save_to_file('front_page',productList)

        except WebDriverException as e:
            print(e)
            print('SCRAPING FAILED')
        

def get_every_detail():
    try:
        try:
            from .front_page import front_page as DATASET
        except ImportError as e:
            print(e)
            from front_page import front_page as DATASET

        dataset_copy = []
        count_item = 0
        jenis_kategori = []
        count_ta_tokped = 0
        for data in DATASET:
            
            try:
                # request_session = requests.Session()
                # # Set correct user agent
                # selenium_user_agent = driver.execute_script("return navigator.userAgent;")
                # request_session.headers.update({"user-agent": selenium_user_agent})
                # print(driver.get_cookies())
                
                # for cookie in driver.get_cookies():
                #     print('COOKIE NAME')
                #     print(cookie['name'])
                #     print('COOKIE VALUE')
                #     print(cookie['value'])
                #     print('COOKIE DOMAIN')
                #     print(cookie['domain'])

                #     request_session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])

                # response = request_session.get(data['link'])
                # print(response)
                # driver.get(request_session.get(data['link']))
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
                        print('FURNITURE LOCATION', furniture_location)
                        print('==================')

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
                print(e)
                print('ERROR IN FOR DATASET')
        
        print('==================')
        print('JENIS KATEGORI')
        print(jenis_kategori)
        print('==================')

        print('==================')
        print('COUNT TA TOKPED')
        print(count_ta_tokped)
        print('==================')

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
        save_to_file('all_data',dataset_copy)

    except FileExistsError as e:
        print(e)
        print('FILE FRONT PAGE DOESNT EXIST')

def main():
    import time
    start_time = time.perf_counter()
    get_every_product()
    get_every_detail()
    import datetime
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time)))

if __name__ == '__main__':
    import time
    start_time = time.perf_counter()
    get_every_product()
    get_every_detail()
    import datetime
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time)))