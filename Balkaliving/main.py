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

s = Service('C:/SeleniumDrivers/chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.implicitly_wait(15)

ADDRESS = 'Jl. Vini Vidi Vici No. 40, Ciracas, Jakarta Timur, 13730, Indonesia'
PHONE = '6287875475391'

def get_all_product():
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
                                    'address':ADDRESS, 'contact_phone':PHONE})
                
            print('PRODUCT LIST')
            print(productList)

        except WebDriverException as e: 
            print(e)   

    # Save file to front_page.py
    save_to_file('front_page',productList)
    

def get_every_detail():
    try:
        # Import front_page from front_page
        from .front_page import front_page as DATASET
    
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
                material = material.split(',')
                
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
                color_replace = {
                    'abu-abu':'grey',
                    'adam motif natural black':'black',
                    'all black':'black',
                    'all natural':'natural',
                    'all white':'white',
                    'amber black gold':'amber',
                    'amber natural':'amber',
                    'anodized':'chrome',
                    'antique':'antique',
                    'antique brown':'brown',
                    'antique copper':'copper',
                    'antique gold':'gold',
                    'antique grey':'grey',
                    'antique silver':'silver',
                    'antique white':'white',
                    'ash grey':'grey',
                    'bark grey antique gold leg':'grey',
                    'beige antique silver':'beige',
                    'bisa sesuai keinginan':'custom',
                    'black antique choco':'black',
                    'black antique copper':'black',
                    'black antique gold':'black',
                    'black black':'black',
                    'black blue':'black',
                    'black brown':'black',
                    'black dark grey':'black',
                    'black distressed':'black',
                    'black distressed black leg':'black',
                    'black eccletic':'black',
                    'black frame':'black',
                    'black gold':'black',
                    'black grey seating antique gold leg':'black',
                    'black greyish':'black',
                    'black maroon burnt':'black',
                    'black matte':'black',
                    'black natural':'black',
                    'black natural willow':'black',
                    'black oreo':'black',
                    'black red':'black',
                    'black solid':'black',
                    'black two tone':'black',
                    'black white':'black',
                    'black white natural':'black',
                    'black white weaving light suar frame':'black',
                    'blue mix':'blue',
                    'blue orange':'blue',
                    'brass gold':'brass',
                    'brown black':'brown',
                    'brown burnt':'brown',
                    'brown leather seating antique gold leg':'brown',
                    'brown metal':'brown',
                    'brown natural':'brown',
                    'brown ornamental':'brown',
                    'brown seating black leg':'brown',
                    'brown top grey leg':'brown',
                    'brown wash':'brown',
                    'brown wash black':'brown',
                    'brown white':'brown',
                    'brushed copper':'copper',
                    'brushed gold':'gold',
                    'brushed ss':'stainless steel',
                    'celadon blue':'blue',
                    'cerah':'bright',
                    'ch,agne':'chagne',
                    'choco natural pala':'brown',
                    'chrome bronze':'chrome',
                    'chrome grey':'chrome',
                    'coffee cream black':'brown',
                    'concrete grey':'grey',
                    'dark brown':'brown',
                    'dark brown gold':'brown',
                    'dark brown light grey':'brown',
                    'dark ch,agne':'chagne',
                    'dark choco':'brown',
                    'dark green':'green',
                    'dark green antique gold leg':'green',
                    'dark silver':'silver',
                    'dusty mint':'green',
                    'flint grey':'grey',
                    'full ivory':'ivory',
                    'glazed brown':'brown',
                    'gliss brown':'brown',
                    'gold metal':'gold',
                    'gold metal'
                    'green mix':'green',
                    'green natural':'green',
                    'green taupe seating antique gold leg':'green',
                    'grey black':'grey',
                    'grey brown':'grey',
                    'grey burnt':'grey',
                    'grey gold':'grey',
                    'grey kobu':'grey',
                    'grey natural':'grey',
                    'grey seating antique brass leg':'grey',
                    'grey seating black leg':'grey',
                    'grey white wash':'grey',
                    'gunmetal':'grey',
                    'heather':'grey',
                    'honey black':'honey',
                    'honey brown wash':'honey',
                    'honey brown wash black leg':'honey',
                    'honey grey':'honey',
                    'honey white':'honey',
                    'ivory brown':'ivory',
                    'jok':'brown',
                    'kain asli mungkin berbeda dengan':'custom',
                    'kobu grey black leg':'grey',
                    'krem':'cream',
                    'light brown':'brown',
                    'light brown natural':'brown',
                    'light grey':'grey',
                    'light grey black':'grey',
                    'light star':'brown',
                    'light suar':'brown',
                    'lime green gold':'green',
                    'marble white':'white',
                    'maroon':'brown',
                    'maroon black':'brown',
                    'matcha green':'green',
                    'matte black':'black',
                    'matte grey':'grey',
                    'matte white':'white',
                    'medium grey':'grey',
                    'mint green':'green',
                    'morocco brown':'brown',
                    'morocco brown black leg':'brown',
                    'multi colour':'mixed',
                    'natural antique':'natural',
                    'natural baby blue':'blue',
                    'natural black':'black',
                    'natural black leg':'black',
                    'natural black white':'black',
                    'natural brown':'brown',
                    'natural coffee brown':'brown',
                    'natural dark brown':'brown',
                    'natural dark choco':'brown',
                    'natural green':'green',
                    'natural grey':'grey',
                    'natural honey':'honey',
                    'natural inca':'brown',
                    'natural jute':'brown',
                    'natural light grey':'grey',
                    'natural matcha green':'green',
                    'natural pala':'brown',
                    'natural pale':'brown',
                    'natural peanut':'brown',
                    'natural pewter':'brown',
                    'natural soft white':'white',
                    'natural strong blue':'blue',
                    'natural tiffany blue':'blue',
                    'natural top black leg':'black',
                    'natural top pewter leg':'brown',
                    'natural verdant green':'green',
                    'natural walnut':'walnut',
                    'natural waterhyacynth black leg':'brown',
                    'natural white':'white',
                    'natural white black':'white',
                    'natural white grey':'white',
                    'natural willow':'brown',
                    'natural willow black':'brown',
                    'natural willow white':'brown',
                    'ocean':'blue',
                    'onyx natural':'brown',
                    'oranye':'orange',
                    'oyster':'white',
                    'pala black':'brown',
                    'pastel blue green':'blue',
                    'petrol':'white',
                    'pine frame':'brown',
                    'powder':'mixed',
                    'purple mix':'purple',
                    'putih gading':'ivory',
                    'red green burnt':'red',
                    'red white':'red',
                    'rose gold':'gold',
                    'sakura pink':'pink',
                    'shaded brown':'brown',
                    'silver aluminium':'silver',
                    'silver black':'silver',
                    'silver white':'silver',
                    'silver wood':'silver',
                    'slate':'white',
                    'soft gold':'gold',
                    'soft white':'white',
                    'solid black':'black',
                    'star motif natural black':'black',
                    'steel':'white',
                    'stone':'grey',
                    'tan brown':'brown',
                    'taupe':'white',
                    'teakwood frame':'brown',
                    'terracotta':'red',
                    'terracotta red':'red',
                    'terracotta red black':'red',
                    'vase':'black',
                    'vintage brown':'brown',
                    'walnut natural':'walnut',
                    'walnut.':'walnut',
                    'warm grey':'grey',
                    'washed grey':'grey',
                    'white black':'white',
                    'white blue':'white',
                    'white brown':'white',
                    'white glossyproduk ini sudah termasuk ongkos kirim dan pemasangan untuk daerah bandung.':'white',
                    'white gold':'white',
                    'white grey':'white',
                    'white grey black':'white',
                    'white kobu':'white',
                    'white natural':'white',
                    'yellow lemon antique gold leg':'yellow',
                    'yellow orange':'yellow',
                    'yellow seating black leg':'yellow',
                }
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
                        data['color'] = [ replace_multiple_char(x.lower().replace(',',''), char_to_replace=color_replace) for x in string ]

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
        save_to_file('all_data',dataset_copy)

    except WebDriverException as e:
        print('ERROR IN SECOND HALF')
        print(e)

def main():
    import time
    start_time = time.perf_counter()

    get_all_product()
    get_every_detail()
    
    import datetime
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time)))

if __name__ == '__main__':
    import time
    start_time = time.perf_counter()

    get_all_product()
    get_every_detail()
    
    import datetime
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time)))