from itertools import product
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


ADDRESS = 'Jl. Jalur 20 No.9, RT.9/RW.10, Meruya Utara, Kec. Kembangan, Kota Jakarta Barat, Daerah Khusus Ibukota Jakarta 11650'
PHONE = '6281299069458'

s = Service('C:/SeleniumDrivers/chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.implicitly_wait(15)

def get_category_and_links():
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
        save_to_file('links',categoryList)

    except WebDriverException as e:
        print(e)
        print('WEB DRIVER FAILED')

def get_every_product():
        try:
            from .links import links as DATASET

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
                                        'address':ADDRESS, 'contact_phone':PHONE,
                                        'tags':data['category'], 'furnitureLocation':data['category'],
                                        'isProduct':1 })

            # Save data to front_page.py
            save_to_file('front_page',productList)

        except WebDriverException as e:
            print(e)
            print('SCRAPING FAILED')
        

def get_every_detail():
    try:
        from .front_page import front_page as DATASET

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

                            material = material.split(',')
                            material = [x.strip() for x in material if x.strip()]

                            tmp_material = material

                            for count,data_material in enumerate(tmp_material):
                                if data_material == 'rotan':
                                    material[count] = 'rattan'
                                if data_material == 'besi':
                                    material[count] = 'iron'
                                if data_material == 'jati':
                                    material[count] = 'teakwood'

                        except AttributeError as ae:
                            print('REGEX MATERIAL #1 FAILED')
                            print(ae)
                        

                        # Get Color from Detail Page with Regex
                        product_color = color.get_attribute('innerHTML')
                        product_color = product_color.lower()
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
                        try:
                            char_to_replace = {
                            '&amp;':',',
                            'amp':',',
                            '&amp':',',
                            'amp;':',',
                            'and':','
                            }
                            product_color = replace_multiple_char(product_color,char_to_replace)
                            product_color = re.sub(r'[^a-z,\s]*', '', product_color)
                            product_color = re.sub(r'\s[xX]\s', ',', product_color)
                            product_color = re.sub('\s{2,}', ' ', product_color)
                            product_color = product_color.split(',')
                            product_color = [ replace_multiple_char(x.strip(),char_to_replace=color_replace) for x in product_color if x.strip() ]

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
        save_to_file('all_data',dataset_copy)

    except FileExistsError as e:
        print(e)
        print('FILE FRONT PAGE DOESNT EXIST')

def main():
    import time
    start_time = time.perf_counter()
    get_category_and_links()
    get_every_product()
    get_every_detail()
    import datetime
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time)))

if __name__ == '__main__':
    import time
    start_time = time.perf_counter()
    get_category_and_links()
    get_every_product()
    get_every_detail()
    import datetime
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time)))