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


ADDRESS = 'Jl. Panglima Polim No.86, RT.2/RW.5, Pulo, Kec. Kby. Baru, Kota Jakarta Selatan, Daerah Khusus Ibukota Jakarta 12160'
PHONE = '02129236727'

s = Service('C:/SeleniumDrivers/chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.implicitly_wait(15)

def get_every_product():
        try:
            PAGES = 1
            productList = []

            for i in range(1, PAGES+1):
                
                url = f'https://www.dekoruma.com/brands/Dobidos?page={i}'
                driver.get(url)

                # Get Product Names, Prices, Pictures, and Links
                product_names = driver.find_elements(By.CSS_SELECTOR, 'div.gdqlKPEW0WGrWRPRMEEBv')
                product_prices = driver.find_elements(By.CSS_SELECTOR,'span[role=price]')
                
                product_links = driver.find_elements(By.CSS_SELECTOR,'div.Dm8LhUyOXIORVM0BUITws > a[product]:first-child')
                product_pictures = driver.find_elements(By.CSS_SELECTOR, 'img._25riT2FvUgRdndrlHTuo-w')
                
                for name,price,links,pic in zip(product_names,product_prices,product_links,product_pictures):
                    product_name = name.get_attribute('innerHTML')
                    product_name = product_name.encode('ascii', 'ignore').decode()

                    
                    product_price = price.get_attribute('innerHTML')
                    product_price = replace_multiple_tags(product_price,'<strike','</strike>')
                    char_to_replace = {
                        '<!--':'',
                        '-->':'',
                        ',':'',
                        ' ':''
                    }
                    product_price = replace_multiple_char(product_price, char_to_replace)

                    product_picture = pic.get_attribute('src')
                    product_link = links.get_attribute('href')
                    
                    print('=============')
                    print(product_name)
                    print(product_price)
                    print(product_picture)
                    print(product_link)
                    print('=============')
                    productList.append({'name':product_name, 'pic':product_picture,
                                        'price':product_price,'link':product_link,
                                        'address':ADDRESS, 'contact_phone':PHONE,
                                        'tags':['kamar mandi'],'furnitureLocation':['kamar mandi'],
                                        'isProduct':1 })

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
        for data in DATASET:

            try:
                driver.get(data['link'])

                # Check if Stock is Available
                is_available_object = driver.find_element(By.CSS_SELECTOR, 'div.t--body.phl > div:first-child > div:first-child')
                is_available = is_available_object.get_attribute('innerHTML')
                is_available = is_available.strip().lower()

                # Don't Take All The Detail if Stock is not Available   
                if is_available != 'stok habis':
                
                    # Get Description and Additional Description object
                    product_descriptions = driver.find_elements(By.CSS_SELECTOR, 'div._3dq5UjErSm8nLRgMyvQbYA + p')
                    additional_descs_object = driver.find_elements(By.CSS_SELECTOR, 'td.pvs')
                    
                    for desc,add_desc in zip(product_descriptions,additional_descs_object):
                        
                        # Get Product Description and Preprocess it
                        product_desc = desc.get_attribute('innerHTML')
                        product_desc = product_desc.encode('ascii', 'ignore').decode()
                        char_to_replace = {
                            '&lt;br&gt;':'',
                            'br&gt;':'',
                            '&lt&gt;':'',
                            '&lt;':'',
                            '</td>':'\n\n',
                            '&amp;':'and',
                        }
                        product_desc = replace_multiple_char(product_desc, char_to_replace)
                        product_desc = replace_multiple_tags(product_desc,'<','>')
                        product_desc = re.sub(r'\s{2,}',' ',product_desc)

                        char_to_replace = {
                            '&amp;':'',
                            'kaca':'glass',
                            'hitam':'black',
                            'metalik':'metalic',
                            'keramik':'ceramic',
                            'kuningan':'brass',
                            'berlapis chrome berkualitas':',chrome',
                            'berlapis chrome':',chrome',
                            'chrome dengan fiinishing chrome':',chrome',
                            'mengkilap':'',
                            'dilapisi':',',
                            'berkualitas':'',
                            'putih':'white',
                            'emas':'gold',
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
                            'beige silver':'beige',
                            'beige,gold leg':'beige',
                            'black , dark grey leg':'black',
                            'black , white speckled':'black',
                            'black black leg':'black',
                            'black copper':'black',
                            'black grey seating gold leg':'black',
                            'black leather , grey':'black',
                            'black leg':'black',
                            'black weaving brown frame':'black',
                            'black willow':'black',
                            'black,gold leg':'black',
                            'black,grey cushion':'black',
                            'blue,gold leg':'blue',
                            'bright, laci penyimpanan ini akan memberikan kehangatan ke rumah anda.':'bright',
                            'brown , grey leg':'brown',
                            'brown , grey,gold leg':'brown',
                            'brown , white':'brown',
                            'brown , white speckled':'brown',
                            'brown antique seating, black leg':'brown',
                            'brown bone,black':'brown',
                            'brown gold':'brown',
                            'brown grey':'brown',
                            'brown leather , grey':'brown',
                            'brown leather seating gold leg':'brown',
                            'brown leather,gold leg':'brown',
                            'brown leg':'brown',
                            'brown top,black leg':'brown',
                            'brown top,brown leg':'brown',
                            'brown white':'brown',
                            'brown,black leg':'brown',
                            'copper , black tripod':'copper',
                            'cream, abu, biru, tosca, merah':'cream',
                            'dark champagne':'champagne',
                            'flamingo pink':'pink',
                            'gold black':'gold',
                            'gold top, black leg':'gold',
                            'golden brown,white':'brown',
                            'green gold leg':'green',
                            'green mix':'green',
                            'green olive':'green',
                            'green white seating gold leg':'green',
                            'green white seating, gold leg':'green',
                            'green,gold leg':'green',
                            'grey marble,gold':'grey',
                            'honey brown':'honey',
                            'honey brown , brown leg':'honey',
                            'honey brown black leg':'honey',
                            'honey brown seating, black leg':'honey',
                            'honey top,white leg':'honey',
                            'ivory brown':'ivory',
                            'ivory dan natural kayu, akan memberikan kesan':'ivory',
                            'ivory grey':'ivory',
                            'kobu grey leg':'grey',
                            'leg black, loom seating':'black',
                            'leg natural sr, loom seating':'natural',
                            'leg natural sr, seating natural weaving':'natural',
                            'm,arin yellow gold leg':'yellow',
                            'natural , white':'white',
                            'natural back , seating brown arm , leg':'natural',
                            'natural base,black leg':'natural',
                            'natural frame white':'natural',
                            'natural seat,black leg':'natural',
                            'natural seating, black leg':'natural',
                            'natural shelf,black':'natural',
                            'natural top gun metal leg':'metalic',
                            'natural top, black leg':'natural',
                            'natural top,black leg':'natural',
                            'natural,black leg':'natural',
                            'natural,red red leg':'red',
                            'red red':'red',
                            'red red black':'red',
                            'redturquoisewhite':'red',
                            'redwhite':'red',
                            'smoke grey arm, seating natural':'grey',
                            'stainless white':'white',
                            'star motif black':'black',
                            'white , natural':'white',
                            'white frame':'white',
                            'white,cobblegrey':'white',
                            'yellow lemon gold leg':'yellow',
                            'natural,white':'white',
                            'naturalwalnut':'walnut',
                            'naturalwalnutandwhite':'walnut',
                            'naturalwalnutwhite':'walnut',
                            'natural baby blue':'blue',
                            'babybluenatural':'blue',
                            'antique teak finish , gold':'gold',
                            'bark grey leg':'grey',
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
                            'tebal':'',
                            'terbuat dari':',',
                            'plastik abs':'plastic abs',
                            'hand shower':'',
                            'wall shower':'',
                            'stainless steel 304':'stainless steel',
                            'granit':'granite',
                            'berwarna':'',
                            'campuran':'',
                            'finishing':'',
                            'dan':',',
                        }
                        material_replace = {
                            ',,':'',
                            'lcmudag':'',
                            'frame long associated with purity and beauty, our lotus blossom cradles votives or tealights in capiz petals, finished in matte metal finish for timeless look group them to create a peaceful oasis of soft light or a compelling table centerpiece makes a memorable hostess gift':'',
                            'lcmdwc':'',
                            'mdlggl':'',
                            'updated kilim style airs out traditional complex patterning with a hand weaved motif that creates a new look for a classic style firm cotton yarns are hand tufted by skilled artisans crafted of pure cotton, this rug will occasionally shed, especially during the first few months, which is easily managed with regular vacuuming a':'',
                            'updated kilim style airs out traditional complex patterning with a hand weaved motif that creates a new look for a classic style firm cotton yarns are hand tufted by skilled artisans crafted of pure cotton, this rug will occasionally shed, especially during the first few months, which is easily managed with regular vacuuming jc':'',
                            'unattended laundries disrupts our room harmony keep them out of our sight by putting it into handwoven laundry hamper spacious interior to keep your space neat, and handwoven pandan with checkered pattern to make your room give your room more classy look plplntbl':'',
                            'unattended laundries disrupts our room harmony keep them out of our sight by putting it into handwoven laundry hamper spacious interior to keep your space neat, and handwoven pan, with checkered pattern to make your room give your room more classy look plpmntbl':'',
                            'inspired from japanese countryside pottery, karatsu rustic vase will be a lovely additional for your home stony textured and concrete grey colour drops in the rustic vibe suitable for interior and exterior spaces narfccgr':'',
                            'dan , abs':'abs',
                            'dari tempered glass yang tidak mudah pecah':'tempered glass',
                            'dasar kayu solid dan cat duco':'solid wood,duco paint',
                            'jati belanda dan roda karet':'dutch teak,rubber wheel',
                            'jati belanda ukuran panjang 120cm x lebar 40cm x tinggi 70cm berat volume 84kg':'dutch teak',
                            'jati belanda, besi behel 10mm':'dutch teak,steel',
                            'jati belanda, hollow 22':'dutch teak,steel',
                            'jati belanda, kaki besi hollow 33':'dutch teak,steel',

                            'jati belanda, roda karet':'dutch teak,rubber wheel',
                            'jati belanda, roda karet dengan rem':'dutch teak,rubber wheel',
                            'jati belanda, roda karet, tegel':'dutch teak,ceramic',
                            'Jok kain, plastik':'cloth seat, plastic',
                            'Jok kulit sintesis dan plastik':'synthetic leather,plastic',
                            'kayu jati belanda, besi wire mesh':'dutch teak,steel wire mesh',
                            'kayu jati belanda':'dutch teak',
                            'jati belanda':'dutch teak',
                            'kayu mahoni dan mdf':'mahogany,mdf',
                            'kayu mahoni, mdf dan finishing cat duco':'mahogany,mdf,duco paint',
                            'kayu mahoni, mdf, cat duco':'mahogany,mdf,duco paint',
                            'kayu mahoni, mdf, gantungan pipa besi, finishing cat duco':'mahogany,mdf,steel, duco paint',
                            'kayu mahoni, papan mdf, cat duco':'mahogany,mdf,duco paint',
                            'Kayu mahoni, papan MDF, laci kayu, dan finishing cat duco':'mahogany,mdf,duco paint',
                            'Kayu Mindi Moku Dining Chair Panjang 46 cm Kedalaman 53 cm Tinggi 84 cm Material Kayu Mindi, Kain 100% Polyester':'mindy wood,polyester',
                            'Kayu Mindi Produk ini adalah meja makan saja, belum termasuk kursi':'mindy wood',
                            'kayu pinus ukuran panjang 30cm x lebar 30cm x tinggi 62cm berat volume 14kg':'pine wood',
                            'kayu pinus, cermin 5mm':'pine wood',
                            'kayu soid, laci kayu, mdf, cat duco Warna Ivory (putih gading':'solid wood,mdf,duco paint',
                            'kayu solid, laci kayu, mdf, cat duco Warna Ivory (putih gading':'solid wood,mdf,duco paint',
                            'kayu solid, laci kayu, mdf, cat ducoWarna Ivory (putih gading':'solid wood,mdf,duco paint',
                            'kayu solid, mdf, cat duco':'solid wood,mdf,duco paint',
                            'kayu solid, mdf, cat ducoDrawerP 60 cm L 45 cm T 56,5 cm kayu solid, mdf, cat ducoSaat digabung panjang maksimal 160~170 cm':'solid wood,mdf,duco paint',
                            'kayu solid, mdf, laci kayu':'solid wood,mdf',
                            'kayu solid, top mdf, laci kayu':'solid wood,mdf',
                            'kayu sungkai':'sungkai wood',
                            'kertas, kayu pinus, kaca':'paper,pine wood,glass',
                            'kulit rusa kutub kulit rusa kami tanpa lubang, tidak akan menggulung setiap kulit rusa adalah bagian yang unik dan meskipun kulitnya bisa sangat mirip, tidak ada dua kulit yang persis sama kulit rusa kutub utara kami akan menambah karakter dan tampilan pelengkap ruang anda arhlb':'reindeer hide',
                            'mdf, cat melamin':'mdf,melamine paint',
                            'mdf, kayu solid, cat duco Warna Ivory (putih gading':'mdf,solid wood,duco paint',
                            'mdf, laci kayu sengon, cat melamin':'mdf,sengon wood,melamine paint',
                            'menggunakan rangka kayu mahoni, papan mdf dan finishing cat duco berkualitas':'mahogany,mdf,duco paint',
                            'menggunakan rel besi yang mudah dibuka dan tahan lama':'steel',
                            'multipleks lapis kayu sungkai, kaki besi hollow 22':'multiplex,sungkai wood',
                            'multipleks sungkai, besi galvanis 2x2cm': 'multiplex,sungkai wood,galvanized iron',
                            'multipleks, jati belanda':'multiplex,dutch teak',
                            'particle board, lapisan paper pvc':'particle board,pvc paper',
                            'particle board, mdf dan finishing pvc white glossyUntuk finishing pvc lebih tahan lembab':'particle board,mdf,pvc',
                            'particle board, mdf dan lapisan PVC':'particle board,mdf,pvc',
                            'partikel board, mdf, finishing pvc vacuum (lebih tahan terhadap lembab , handle aluminiumProduk ini free rakit untuk daerah Bandung':'particle board,mdf,pvc',
                            'pintu kayu jati belanda, badan multipleks':'dutch teak,multiplex',
                            'plywood lapis veneer sungkai':'sungkai wood,plywood,veneer',
                            'rangka kayu mahoni, lemari ini didukung konstruksi yang sangat kokoh':'mahogany',
                            'rangka kayu mahoni, mdf, cat duco':'mahogany,mdf,duco paint',
                            'rangka kayu mahoni, papan mdf dan finishing cat duco':'mahogany,mdf,duco paint',
                            'rangka kayu mahoni, papan mdf dan finishing cat duco berkualitas':'mahogany,mdf,duco paint',
                            'rangka kayu mahoni, papan mdf, finishing cat duco':'mahogany,mdf,duco paint',
                            'rangka kayu mahoni, papan mdf, kaca, cat duco':'mahogany,mdf,duco paint',
                            'Rangka kayu mahoni,papan mdf dan finishing menggunakan cat duco':'mahogany,mdf,duco paint',
                            'rangka kayu pinus, busa rebounded, kain':'pine wood,rebounded foam,fabric',
                            'rangka kayu solid mahoni':'mahogany',
                            'rangka kayu solid mahoni, papan mdf dan finishing cat duco':'mahogany,mdf,duco paint',
                            'rangka kayu solid mahoni, papan mdf dan finishing cat duco, rak ini kuat dan tahan lama':'mahogany,mdf,duco paint',
                            'rangka kayu solid yang kokoh':'solid wood',
                            'rangka sofa: jati belanda. dudukan dan sandaran: busa kombinasi dakron, sarung kanvas':'dutch teak,dakron combination foam,canvas cover',
                            'rattan sintetis':'synthetic rattan',
                            'rattan, cermin asahi merefleksikan estetika tahun an, semburan kelopak bunga di sekelilingnya melambangkan bunga matahari yang cerah rattan yang anggun menghasilkan bayangan yang menarik di dinding lfmrnt':'rattan,asahi glass',
                            'rattan, metal not suitable for outdoor except sheltered no water exposure or direct sunlight':'rattan,metal',
                            'rel besi yang mudah dibuka dan tahan lama':'steel',
                            'rel besi, sehingga mudah dibuka dan tahan lama':'steel',
                            'stainless white, plastik':'stainless,plastic',
                            'suarwood tremiron':'suar wood',
                            'suar wood tremiron':'suar wood',
                            'synthetic weaving, mindi wood':'synthetic weaving,mindy wood',
                            'teakwood, metal brimming with rustic charm, edizio side table , rack will instantly elevate visual appeal of your living space showcasing the best quality of teakwood as racks, and sturdy metal to hold the teakwood together, this chic piece will be an excellent choice for your home or office tier racks means more storage space to stage your beloved collectibles and magazines, or to simply store light snacks to accompany your relaxing time yogntbl':'teakwood,metal',
                            'teakwood, sisipan bambu':'teakwood,bamboo weaving',
                            'terracota':'terracotta',
                            'untuk kenyamanan Anda sandaran melengkung dan sarung kain di bagian dudukan':'mindy wood,fabric,polyester',
                            'waterhyacinth':'water hyacinth',
                            'waterhyacynth, vinyl':'water hyacinth,vinyl',
                            'cooper solid':'copper',
                            'teak':'teakwood',
                            'tremiron':'',                        
                            ', kaki iron hollow 22':'',
                            'multipleks':'multiplex',
                            'tegel':'ceramic',
                            'kain':'fabric',
                            'katun':'cotton',
                            'ceramic':'ceramic',
                            'rotan':'rattan',
                            'besi':'iron',
                            'teak wood':'teakwood',
                            'jati' : 'teakwood',
                            'abaca banana hemp':'abaca',
                            ' , ':', ',
                            ' ,':', ',
                            'berdasarkan pesanan':'custom',
                            'dan':',',
                            'brass ,chromebrass ,chromebrass ,chromebrass ,chromebrass ,chromebrass ,chromebrass ,chromebrass ,chrome':'brass,chrome',

                        }
                        hard_to_remove_material_word = {
                            'Dibuat dengan rangka kayu mahoni, lemari ini didukung dengan konstruksi yang sangat kokoh':'mahogany',
                            'brass, chromebrass, chromebrass, chromebrass, chromebrass, chromebrass, chromebrass, chromebrass, chrome':'brass,chrome',
                            'Bahan solid wood, mdf, duco paintDrawerP 60 cm L 45 cm T 56,5 cm Bahan solid wood, mdf, duco paintSaat digabung panjang maksimal 160~170 cm':'solid wood,mdf,duco paint',
                            'Dibuat untuk kenyamanan Anda dengan sandaran melengkung , sarung fabric di bagian dudukan':'mindy wood,fabric,polyester',
                            'multiplex lapis sungkai wood, kaki iron hollow 22':'multiplex,sungkai wood,iron',
                            'unattended laundries disrupts our room harmony keep them out of our sight by putting it into handwoven laundry hamper spacious interior to keep your space neat, and handwoven pan, with checkered pattern to make your room give your room more classy look plpmntbl':'',
                            'when it comes to relaxing lounge chair in linear modern style, our comfortable gonzalo lounge chair knows the ropes affordable, laidback chair is handwoven of synthetic resin rope, a resilient new design thats colorfast and uvresistant lfyogbw':'',
                            'bras, stainless steel 304':'brass,stainless steel 304',
                            'kayu pinus':'pine wood',
                            'sofa: dutch teakwood. dudukan , sandaran: busa kombinasi dakron, sarung kanvas':'dutch teak,dakron combination foam,canvas cover',
                            'teakwood, synthetic a smooth finished combination of teakwood twig and compact natural faux rattan could be a great option for decorating your living space could be placed on living room or matching coffee table, look nice, comfy, and bring up ructic vibes nfrnt':'teakwood',
                            'DrawerP 60 cm L 45 cm T 56,5 cm solid wood,mdf,duco paintSaat digabung panjang maksimal 160~170 cm':'',
                            'dibuat dengan standar ekspor':'export standard',
                            'Bahan':'',
                            'pintu':'',
                            'bahan':'',
                            'dibuat dengan':'',
                            'Dibuat dengan':'',
                            'dibuat':'',
                            'Dibuat':'',
                            'glass stainless':'glass,stainless steel',
                            'stainless white':'glass,stainless steel',
                            'stainless white 304':'stainless steel 304',
                            'stainless white stainless steel 304':'stainless steel 304',
                            'syntethic':'synthetic',
                            'syntetic':'synthetic',
                            'sintetis':'synthetic',

                            'alluminium':'aluminium',
                            'taekwood':'teakwood',
                            'teakwood teakwood':'teakwood',
                            'vicose':'viscose',
                            'plastik':'plastic',
                            'poliester':'polyester',
                            'finishing cat duco':'duco paint',
                            'teakwoodwood':'teakwood',
                            'suar wood':'suarwood',
                            'mindiwood':'mindy wood',
                            'mindi wood':'mindy wood',
                            'rangka':'',
                            'dengan rem':'',
                            'polyestercotton':'polyester,cotton',
                            'berkualitas':'',
                            ', rak ini kuat , tahan lama':'',
                            ',,':',',
                            'rangka sofa: dutch teakwood. dudukan , sandaran: busa kombinasi dakron, sarung kanvas':'dutch teak,dakron combination foam,canvas cover',
                            'cermin asahi merefleksikan estetika tahun an, semburan kelopak bunga di sekelilingnya melambangkan bunga matahari yang cerah rattan yang anggun menghasilkan bayangan yang menarik di dinding lfmrnt':'asahi glass',
                            'DrawerP 60 cm L 45 cm T 56,5 cm solid wood, mdf, duco paintSaat digabung panjang maksimal 160~170 cm':'',
                            'tremiron':'',
                            'sisipan bambu':'bamboo weaving',
                            'untuk kenyamanan Anda sandaran melengkung , sarung fabric di bagian dudukan':'mindy wood,fabric,polyester',
                            'brasss':'brass',

                        }
                        # Get Additional Description and Preprocess it
                        additional_description = ''
                        isNext = [None,None]
                        product_color = ''
                        material = ''
                        dimension_length = ''  
                        dimension_width = ''
                        dimension_height = ''
                        dimension_unit = 'cm'
                        weight = ''
                        weight_unit = 'kg'
                        for count, add_desc in enumerate(additional_descs_object):
                            tmp_additional_description = add_desc.get_attribute('innerHTML')
                            tmp_additional_description = tmp_additional_description.encode('ascii', 'ignore').decode()
                            tmp_additional_description = replace_multiple_tags(tmp_additional_description,'<','>') 

                            if isNext[0] and isNext[1] == 'warna':
                                product_color = tmp_additional_description.lower()
                                product_color = replace_multiple_char(product_color,char_to_replace)

                            elif isNext[0] and isNext[1] == 'material':
                                material = tmp_additional_description.lower()
                                material = replace_multiple_char(material,char_to_replace)
                                material = material.strip()
                                material = replace_multiple_char(material,material_replace)
                                material = material.strip()
                                material = replace_multiple_char(material,hard_to_remove_material_word)
                                material = material.strip()
                                material = re.sub(r'^,\s{0,}?','',material)
                                material = re.sub(r',\s{0,}?$','',material)
                                material = re.sub(r'\s?,\s?',',',material)
                                material = material.strip()

                            elif isNext[0] and isNext[1] == 'ukuran barang':
                                res = re.search(r'([\d.,]+)\s?(cm|m)?\s?[xX]?\s?([\d.,]+)\s?(cm|m)?\s?[xX]?\s?([\d.,]+)\s?(cm|m)',tmp_additional_description)
                                dimension_length = res.group(1)
                                dimension_width = res.group(3)
                                dimension_height = res.group(5)

                                dimension_length = dimension_length.replace(',','.')
                                dimension_width = dimension_width.replace(',','.')
                                dimension_height = dimension_height.replace(',','.')

                                if res.group(2) == res.group(4) == res.group(6):
                                    dimension_unit = res.group(2)

                            elif isNext[0] and isNext[1] == 'berat':
                                res = re.search(r'([\d.,]+)\s?(?:kg|g)',tmp_additional_description)
                                weight = res.group(1)
                                weight = weight.replace(',','.')

                            if isNext[0]:
                                isNext[0] = False
                                isNext[1] = None

                            if tmp_additional_description.lower() == 'warna' or \
                                tmp_additional_description.lower() == 'material' or \
                                    tmp_additional_description.lower() == 'ukuran barang' or \
                                        tmp_additional_description.lower() == 'berat':
                                isNext[0] = True
                                isNext[1] = tmp_additional_description.lower()

                            # Because data is in table tr td, if it's a new td add \n
                            if count % 2 == 0 and count != 0 :
                                additional_description += '<br>'
                            else:
                                tmp_additional_description = replace_multiple_char(tmp_additional_description,char_to_replace)

                            additional_description += tmp_additional_description + ' '


                        print('==================')
                        print(product_desc)
                        print('ADDITIONAL DESCRIPTION')
                        print(additional_description)

                        print('COLOR',product_color)
                        print('MATERIAL',material)
                        print('DIMENSION LENGTH',dimension_length)
                        print('DIMENSION WIDTH',dimension_height)
                        print('DIMENSION HEIGHT',dimension_height)
                        print('DIMENSION UNIT',dimension_unit)
                        print('WEIGHT',weight)
                        print('WEIGHT UNIT',weight_unit)
                        print('==================')

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

    get_every_product()
    get_every_detail()

    import datetime
    print('Program Runtime')
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time)))

if __name__ == '__main__':
    import time
    start_time = time.perf_counter()

    get_every_product()
    get_every_detail()

    import datetime
    print('Program Runtime')
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time)))