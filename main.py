import psycopg2
import psycopg2.extras
import os
from slugify import slugify

# Import All Data from each module
def get_all_data():
    try:
        from AERDekoruma import all_data as AER_Dekoruma_All_Data
        AER_Dekoruma_All_Data = AER_Dekoruma_All_Data.all_data

    except ImportError as e:
        print('=========================================')
        print('## Error While Importing AER Dekoruma ##')
        print('=========================================')
        print(e)
        print('=========================================')

######################################################################        
    
    try:
        from AtesonHome import all_data as Ateson_Home_All_Data
        Ateson_Home_All_Data = Ateson_Home_All_Data.all_data

    except ImportError as e:
        print('=========================================')
        print('## Error While Importing Ateson Home ##')
        print('=========================================')
        print(e)
        print('=========================================')

######################################################################        

    try:
        from Balkaliving import all_data as Balkaliving_All_Data
        Balkaliving_All_Data = Balkaliving_All_Data.all_data

    except ImportError as e:
        print('=========================================')
        print('## Error While Importing Balkaliving ##')
        print('=========================================')
        print(e)
        print('=========================================')

######################################################################        

    try:
        from Nagarey import all_data as Nagarey_All_Data
        Nagarey_All_Data = Nagarey_All_Data.all_data

    except ImportError as e:
        print('=========================================')
        print('## Error While Importing Nagarey ##')
        print('=========================================')
        print(e)
        print('=========================================')

######################################################################        

    try:
        from SohoID import all_data as SohoID_All_Data
        SohoID_All_Data = SohoID_All_Data.all_data

    except ImportError as e:
        print('=========================================')
        print('## Error While Importing Soho ID ##')
        print('=========================================')
        print(e)
        print('=========================================')

######################################################################        

    try:
        from AERTEKA import all_data as AER_TEKA_All_Data
        AER_TEKA_All_Data = AER_TEKA_All_Data.all_data

    except ImportError as e:
        print('=========================================')
        print('## Error While Importing AER TEKA ##')
        print('=========================================')
        print(e)
        print('=========================================')

######################################################################        

    try:
        from AERDobidos import all_data as AER_Dobidos_All_Data
        AER_Dobidos_All_Data = AER_Dobidos_All_Data.all_data

    except ImportError as e:
        print('=========================================')
        print('## Error While Importing AER Dobidos ##')
        print('=========================================')
        print(e)
        print('=========================================')

######################################################################        

    try:
        from AERDobidos import all_data as AER_Dobidos_All_Data
        AER_Dobidos_All_Data = AER_Dobidos_All_Data.all_data

    except ImportError as e:
        print('=========================================')
        print('## Error While Importing AER Dobidos ##')
        print('=========================================')
        print(e)
        print('=========================================')

######################################################################        

    try:
        from AERGree import all_data as AER_Gree_All_Data
        AER_Gree_All_Data = AER_Gree_All_Data.all_data


    except ImportError as e:
        print('=========================================')
        print('## Error While Importing AER Gree ##')
        print('=========================================')
        print(e)
        print('=========================================')

######################################################################        

    try:
        from AERSharp import all_data as AER_Sharp_All_Data
        AER_Sharp_All_Data = AER_Sharp_All_Data.all_data

    except ImportError as e:
        print('=========================================')
        print('## Error While Importing AER SHARP ##')
        print('=========================================')
        print(e)
        print('=========================================')

######################################################################        

    try:
        from AERPaloma import all_data as AER_Paloma_All_Data
        AER_Paloma_All_Data = AER_Paloma_All_Data.all_data

    except ImportError as e:
        print('=========================================')
        print('## Error While Importing AER PALOMA ##')
        print('=========================================')
        print(e)
        print('=========================================')

######################################################################        

    return [(AER_Dekoruma_All_Data, 'AER DEKORUMA'), 
            (Ateson_Home_All_Data, 'ATESON HOME'), 
            (Balkaliving_All_Data,'BALKALIVING'), 
            (Nagarey_All_Data,'NAGAREY'), 
            (SohoID_All_Data,'SOHO ID'),
            (AER_TEKA_All_Data,'AER TEKA'),
            (AER_Dobidos_All_Data,'AER DOBIDOS'),
            (AER_Gree_All_Data,'AER GREE'),
            (AER_Sharp_All_Data,'AER SHARP'),
            (AER_Paloma_All_Data,'AER PALOMA'),
            ]

def run_all_web_scraper():
    import time

    start_time_parent = time.perf_counter()

    # Import All Main Function
    from AERDekoruma import main as MAIN_AER_DEKORUMA
    MAIN_AER_DEKORUMA.main()

    from AtesonHome import main as MAIN_ATESONHOME
    MAIN_ATESONHOME.main()

    from Balkaliving import main as MAIN_BALKALIVING
    MAIN_BALKALIVING.main()

    from Nagarey import main as MAIN_NAGAREY
    MAIN_NAGAREY.main()

    from SohoID import main as MAIN_SOHO_ID
    MAIN_SOHO_ID.main()

    from AERTEKA import main as MAIN_AER_TEKA
    MAIN_AER_TEKA.main()

    from AERDobidos import main as MAIN_AER_DOBIDOS
    MAIN_AER_DOBIDOS.main()

    from AERGree import main as MAIN_AER_GREE
    MAIN_AER_GREE.main()

    from AERSharp import main as MAIN_AER_SHARP
    MAIN_AER_SHARP.main()
    
    from AERPaloma import main as MAIN_AER_PALOMA
    MAIN_AER_PALOMA.main()

    import datetime
    print('ALL SCRAPING RUNTIME')
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time_parent)))

def transfer_data_to_database():
    try:
        with psycopg2.connect(
                    host = os.environ.get('host'),
                    dbname = os.environ.get('database'),
                    user = os.environ.get('username'),
                    password = os.environ.get('pwd'),
                    port = os.environ.get('port_id')) as conn:

            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

                insert_script  = '''INSERT INTO public.main_app_item( 
                                    name, 
                                    slug,
                                    pic, 
                                    address, 
                                    phone, 
                                    price, 
                                    original_link, 
                                    description, 
                                    additional_desc, 
                                    material,
                                    weight, 
                                    weight_unit, 
                                    color, 
                                    dimension_length, 
                                    dimension_width, 
                                    dimension_height, 
                                    dimension_unit, 
                                    "isProduct", 
                                    furniture_location)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

                all_records = get_all_data()
                                
                print('=========================================')
                for record in all_records:
                    for data in record[0]:
                        weight =  float(data['weight']) if data['weight'] else 0
                        dimension_length =  float(data['dimension_length']) if data['dimension_length'] else 0
                        dimension_width =  float(data['dimension_width']) if data['dimension_width'] else 0
                        dimension_height =  float(data['dimension_height']) if data['dimension_height'] else 0
                        isProduct = True if data['isProduct'] == 1 else False
                        slug = slugify(data['name'])

                        if len(str(dimension_length)) > 5:
                            dimension_length =  float(str(dimension_length)[:3] + '.00')

                        tmp_data = (data['name'], 
                                    slug,
                                    data['pic'],
                                    data['address'],
                                    data['contact_phone'],
                                    data['price'],
                                    data['link'],
                                    data['description'],
                                    data['additional_desc'],
                                    ','.join(data['material']),
                                    weight,
                                    data['weight_unit'],
                                    ','.join(data['color']),
                                    dimension_length,
                                    dimension_width,
                                    dimension_height,
                                    data['dimension_unit'], 
                                    isProduct,
                                    ','.join(data['furnitureLocation']))
                        cur.execute(insert_script, tmp_data)
                    print(record[1] + ' DATA INSERTED SUCCESSFULY')
                print('=========================================')
                
                # for record in insert_values:
                #     cur.execute(insert_script, record)

                # update_script = 'UPDATE employee SET salary = salary + (salary * 0.5)'
                # cur.execute(update_script)

                # delete_script = 'DELETE FROM skripsi WHERE 1'
                # delete_record = ('James',)
                # cur.execute(delete_script, delete_record)

                # cur.execute('SELECT * FROM EMPLOYEE')
                # for record in cur.fetchall():
                #     print(record['name'], record['salary'])

    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


RUN_SCRAPING = False
RUN_TRANSFER_DATA = True

if __name__ == '__main__':
    if RUN_SCRAPING:
        run_all_web_scraper()

    if RUN_TRANSFER_DATA:
        transfer_data_to_database()