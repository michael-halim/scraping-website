import psycopg2
import psycopg2.extras
import os
from slugify import slugify
from ml_helper import *

import numpy as np
import time 
import datetime
from zoneinfo import ZoneInfo

LOCAL_TZ = ZoneInfo('Asia/Bangkok')

def start_timer():
    return time.perf_counter()

def end_timer(start_time, time_log=[], add_time_log=False, message=''):
    total_time = datetime.timedelta(seconds = time.perf_counter() - start_time)
    bracket = '********************************************'
    print(bracket)
    print(message)
    print('--- %s ---' % (total_time))
    print(bracket)

    if add_time_log:
        time_log += [ (message, str(total_time)) ]
        return time_log

    return None
def get_today():
    """Get Today's Date with `YYYY-MM-DD` Format"""
    today = datetime.datetime.now(LOCAL_TZ)
    return datetime.date(today.year, today.month, today.day)

def print_help(var, title='', username='', show_list_more=False):
    """Log to CLI and Save to File \n
    `============================================`\n
    `2023-01-06 14:15:01.963270`\n
    `USERNAME:  TRAIN APRIORI MODEL`\n
    `APRIORI MODEL`\n
    `============================================`
    
    `============================================`\n
    `2023-01-06 14:15:01.923290`\n
    `USERNAME:  TRAIN WEIGHTED MATRIX`\n
    `CBF LOWEST ITEM LIST`\n
    `[ [841, 2.82], [840, 2.95], [2237, 3.03], [834, 3.2], [224, 3.23] ]`\n
    `LENGTH : 5`\n
    `============================================`
    """
    logs = []
    bracket = '============================================'
    time_now = datetime.datetime.now(LOCAL_TZ)
    print(bracket)
    print(time_now)
    print('USERNAME: ', username)

    logs += [bracket, str(time_now), f'USERNAME: {str(username)}']
    
    if isinstance(var, str) and title == '':
        print(var)
        print(bracket)
        logs += [str(var), bracket]
    else:
        print(title)
        modified_var = var
        if not show_list_more and isinstance(var, list):
            modified_var = modified_var[:5] if len(modified_var) > 5 else modified_var

        print(modified_var)
        logs += [str(title), str(modified_var)]

        try:
            print(f'ORIGINAL LENGTH : {len(var)}')
            print(bracket)
            logs += [f'ORIGINAL LENGTH : {str(len(var))}', bracket]
        except TypeError as e:
            print(bracket)
            logs += [bracket]

    logs = '\n'.join(logs)

    if os.environ.get('DEVELOPMENT_MODE') == 'False':
        save_log(logs)

def save_log(logs):
    dirname = os.path.dirname(__file__)
    up_one_levels = 'scraping_logs' + os.sep
    filename = str(get_today()) + '.txt'
    dest_path = os.path.join(dirname, up_one_levels, filename)

    with open(dest_path, 'a') as file:
        file.write(logs)

    file.close()
    
# Import All Data from each module
def show_error_message(err, module_name = ''):
    print('=========================================')
    print(f'## Error While Importing {module_name} ##')
    print('=========================================')
    print(err)
    print('=========================================')

def get_all_data():
    try:
        from AERDekoruma import all_data as AER_Dekoruma_All_Data
        AER_Dekoruma_All_Data = AER_Dekoruma_All_Data.all_data

    except ImportError as e:
        show_error_message(e, 'AER DEKORUMA')

######################################################################
    
    try:
        from AtesonHome import all_data as Ateson_Home_All_Data
        Ateson_Home_All_Data = Ateson_Home_All_Data.all_data

    except ImportError as e:
        show_error_message(e, 'Ateson Home')

######################################################################

    try:
        from Balkaliving import all_data as Balkaliving_All_Data
        Balkaliving_All_Data = Balkaliving_All_Data.all_data

    except ImportError as e:
        show_error_message(e, 'Balkaliving')

######################################################################

    try:
        from Nagarey import all_data as Nagarey_All_Data
        Nagarey_All_Data = Nagarey_All_Data.all_data

    except ImportError as e:
        show_error_message(e, 'Nagarey')

######################################################################

    try:
        from SohoID import all_data as SohoID_All_Data
        SohoID_All_Data = SohoID_All_Data.all_data

    except ImportError as e:
        show_error_message(e, 'Soho ID')

######################################################################

    try:
        from AERTEKA import all_data as AER_TEKA_All_Data
        AER_TEKA_All_Data = AER_TEKA_All_Data.all_data

    except ImportError as e:
        show_error_message(e, 'AER TEKA')

######################################################################

    try:
        from AERDobidos import all_data as AER_Dobidos_All_Data
        AER_Dobidos_All_Data = AER_Dobidos_All_Data.all_data

    except ImportError as e:
        show_error_message(e, 'AER Dobidos')

######################################################################

    try:
        from AERGree import all_data as AER_Gree_All_Data
        AER_Gree_All_Data = AER_Gree_All_Data.all_data


    except ImportError as e:
        show_error_message(e, 'AER Gree')

######################################################################

    try:
        from AERSharp import all_data as AER_Sharp_All_Data
        AER_Sharp_All_Data = AER_Sharp_All_Data.all_data

    except ImportError as e:
        show_error_message(e, 'AER Sharp')

######################################################################

    try:
        from AERPaloma import all_data as AER_Paloma_All_Data
        AER_Paloma_All_Data = AER_Paloma_All_Data.all_data

    except ImportError as e:
        show_error_message(e, 'AER Paloma')

######################################################################

    try:
        from Tokopedia import all_data as Tokopedia_All_Data
        Tokopedia_All_Data = Tokopedia_All_Data.all_data

    except ImportError as e:
        show_error_message(e, 'Tokopedia')

######################################################################

    try:
        from OLX import all_data as OLX_All_Data
        OLX_All_Data = OLX_All_Data.all_data

    except ImportError as e:
        show_error_message(e, 'OLX')

######################################################################

    return [(AER_Dekoruma_All_Data, 'AER DEKORUMA'), 
            (AER_Dobidos_All_Data,'AER DOBIDOS'),
            (AER_Gree_All_Data,'AER GREE'),
            (AER_Paloma_All_Data,'AER PALOMA'),
            (AER_Sharp_All_Data,'AER SHARP'),
            (AER_TEKA_All_Data,'AER TEKA'),
            (Ateson_Home_All_Data, 'ATESON HOME'), 
            (Balkaliving_All_Data,'BALKALIVING'), 
            (Nagarey_All_Data,'NAGAREY'), 
            (SohoID_All_Data,'SOHO ID'),
            (Tokopedia_All_Data,'TOKOPEDIA'),
            (OLX_All_Data, 'OLX'),
            ]

def run_all_web_scraper():
    import time

    start_time_parent = time.perf_counter()

    # Import All Main Function
    from AERDekoruma import main as MAIN_AER_DEKORUMA
    MAIN_AER_DEKORUMA.main()

    from AERDobidos import main as MAIN_AER_DOBIDOS
    MAIN_AER_DOBIDOS.main()

    from AERGree import main as MAIN_AER_GREE
    MAIN_AER_GREE.main()

    from AERPaloma import main as MAIN_AER_PALOMA
    MAIN_AER_PALOMA.main()

    from AERSharp import main as MAIN_AER_SHARP
    MAIN_AER_SHARP.main()

    from AERTEKA import main as MAIN_AER_TEKA
    MAIN_AER_TEKA.main()

    from AtesonHome import main as MAIN_ATESONHOME
    MAIN_ATESONHOME.main()

    from Balkaliving import main as MAIN_BALKALIVING
    MAIN_BALKALIVING.main()

    from Nagarey import main as MAIN_NAGAREY
    MAIN_NAGAREY.main()

    from SohoID import main as MAIN_SOHO_ID
    MAIN_SOHO_ID.main()
    
    from Tokopedia import main as MAIN_TOKOPEDIA
    MAIN_TOKOPEDIA.main()

    from OLX import main as MAIN_OLX
    MAIN_OLX.main()

    print('ALL SCRAPING RUNTIME')
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time_parent)))


def process_data_item():
    all_records = get_all_data()
    data_insert_check_time, tmp_data_insert = [], []
    
    for record in all_records:
        for data in record[0]:
            weight =  float(data['weight']) if data['weight'] and not str(data['weight']).isalpha() else 0
            dimension_length =  float(data['dimension_length']) if data['dimension_length'] and not str(data['dimension_length']).isalpha() else 0
            dimension_width =  float(data['dimension_width']) if data['dimension_width'] and not str(data['dimension_width']).isalpha() else 0
            dimension_height =  float(data['dimension_height']) if data['dimension_height'] and not str(data['dimension_height']).isalpha() else 0

            isProduct = True if data['isProduct'] == 1 else False
            slug = slugify(data['name'])
            if len(str(dimension_length)) > 5:
                dimension_length =  float(str(dimension_length)[:3] + '.00')
            
            modified_color = data['color']
            if isinstance(data['color'], list):
                modified_color = ''.join(data['color'])

            modified_material = data['material']
            if isinstance(data['material'], list):
                modified_material = ','.join(data['material'])
            
            tmp_data_insert.append(
                (
                    data['name'], 
                    slug,
                    data['pic'],
                    data['address'],
                    data['contact_phone'],
                    data['price'],
                    data['link'],
                    data['description'],
                    data['additional_desc'],
                    modified_material,
                    weight,
                    data['weight_unit'],
                    modified_color,
                    dimension_length,
                    dimension_width,
                    dimension_height,
                    data['dimension_unit'], 
                    isProduct,
                    ','.join(data['furnitureLocation']),
                    datetime.datetime.now(LOCAL_TZ)
                )
            )
            data_insert_check_time.append( 
                (
                    data['name'], 
                    slug,
                    data['pic'],
                    data['address'],
                    data['contact_phone'],
                    data['price'],
                    data['link'],
                    data['description'],
                    data['additional_desc'],
                    modified_material,
                    weight,
                    data['weight_unit'],
                    modified_color,
                    dimension_length,
                    dimension_width,
                    dimension_height,
                    data['dimension_unit'], 
                    isProduct,
                    ','.join(data['furnitureLocation']),
                    datetime.datetime.now(LOCAL_TZ),
                    datetime.datetime.now(LOCAL_TZ),
                    1
                )
            )
        print_help(var=str(record[1]) + ' DATA PROCESSED SUCCESSFULY', username='PROCESS DATA ITEM')
    
    return data_insert_check_time, tmp_data_insert

def process_data_feature_and_distance(all_material, 
                                        all_title, 
                                        all_description, 
                                        all_weight, 
                                        all_dimension_length, 
                                        all_dimension_width,
                                        all_dimension_height, 
                                        all_price, 
                                        all_furniture_location, 
                                        all_color):
    print_help(var='BAG OF WORDS CATEGORICAL', username='CALCULATING BAG OF WORDS')

    # Get Vectorized_X and Feature Names for Categorical Featuers
    print_help(var='BOW COLOR', username='CALCULATING BAG OF WORDS')
    vectorized_X_color, color_feature_names = bag_of_words(all_color)

    print_help(var='BOW MATERIAL', username='CALCULATING BAG OF WORDS')
    vectorized_X_material, material_feature_names = bag_of_words(all_material, delimiter='comma')
    
    print_help(var='BOW FURNITURE LOCATION', username='CALCULATING BAG OF WORDS')
    vectorized_X_furniture_location, furniture_location_feature_names = bag_of_words(all_furniture_location, delimiter='comma')
    
    print_help(var='BOW DESCRIPTION', username='CALCULATING BAG OF WORDS')
    vectorized_X_description, description_feature_names = bag_of_words(all_description)
    
    print_help(var='BOW TITLE', username='CALCULATING BAG OF WORDS')
    vectorized_X_title, title_feature_names = bag_of_words(all_title)
    
    all_dimension = []

    for length, width, height in zip(all_dimension_length, all_dimension_width, all_dimension_height):
        length = float(length) if length != '' else 0
        width = float(width) if width != '' else 0
        height = float(height) if height != '' else 0
        all_dimension.append([length , width, height ])

    # Get Distances for Categorical Features
    print_help(var='FINDING COLOR DISTANCES....', username='CALCULATING BAG OF WORDS')
    color_distances = find_all_distance(vectorized_X_color,is_normalized_data=True, is_standard_scaler=False)
    
    print_help(var='FINDING MATERIAL DISTANCES....', username='CALCULATING BAG OF WORDS')
    material_distances = find_all_distance(vectorized_X_material,is_normalized_data=True, is_standard_scaler=False)
    
    print_help(var='FINDING DESCRIPTION DISTANCES....', username='CALCULATING BAG OF WORDS')
    description_distances = find_all_distance(vectorized_X_description,is_normalized_data=True, is_standard_scaler=False)
    
    print_help(var='FINDING TITLE DISTANCES....', username='CALCULATING BAG OF WORDS')
    title_distances = find_all_distance(vectorized_X_title,is_normalized_data=True, is_standard_scaler=False)
    
    print_help(var='FINDING FURNITURE LOCATION DISTANCES....', username='CALCULATING BAG OF WORDS')
    furniture_location_distances = find_all_distance(vectorized_X_furniture_location,is_normalized_data=True, is_standard_scaler=False)

    # Reshape All Numerical Features
    all_weight = np.asarray(all_weight).reshape(-1, 1)
    all_price = np.asarray(all_price).reshape(-1, 1)

    print_help(var='FINDING WEIGHT DISTANCES....', username='CALCULATING BAG OF WORDS')
    weight_distances = find_all_distance(all_weight,is_normalized_data=True, is_standard_scaler=False)
    
    print_help(var='FINDING DIMENSION DISTANCES....', username='CALCULATING BAG OF WORDS')
    dimension_distances = find_all_distance(all_dimension,is_normalized_data=True, is_standard_scaler=False)
    
    print_help(var='FINDING PRICE DISTANCES....', username='CALCULATING BAG OF WORDS')
    price_distances = find_all_distance(all_price,is_normalized_data=True, is_standard_scaler=False)

    return vectorized_X_color, color_feature_names, vectorized_X_material, material_feature_names, \
        vectorized_X_furniture_location, furniture_location_feature_names, vectorized_X_description, description_feature_names, \
            vectorized_X_title, title_feature_names, color_distances, material_distances, description_distances, title_distances, \
                furniture_location_distances, all_weight, all_price, all_dimension, weight_distances, dimension_distances, price_distances

def construct_distances(all_ids,
                        color_distances,
                        material_distances,
                        description_distances, 
                        title_distances, 
                        furniture_location_distances,
                        weight_distances, 
                        dimension_distances, 
                        price_distances):

    data_insert_distance_check_time = []
    for i in range(len(all_ids)):
        for j in range(i, len(all_ids)-1):
            
            total_distance = float(color_distances[i][j]) + float(title_distances[i][j]) + float(description_distances[i][j]) + float(material_distances[i][j]) \
                    + float(weight_distances[i][j]) + float(dimension_distances[i][j]) + float(price_distances[i][j]) + float(furniture_location_distances[i][j])
            
            data_insert_distance_check_time.append( 
                (
                    all_ids[i],
                    all_ids[j],
                    round(color_distances[i][j], 2),
                    round(title_distances[i][j], 2),
                    round(description_distances[i][j], 2),
                    round(material_distances[i][j], 2),
                    round(weight_distances[i][j], 2),
                    round(dimension_distances[i][j], 2),
                    round(price_distances[i][j], 2),
                    round(furniture_location_distances[i][j], 2),
                    round(total_distance, 2),
                    99.0,
                    ''
                )
            )
            if i % 400 == 0 and j % 400 == 0:
                print('====================================')
                print_help(var=color_distances[i][j], title='COLOR DISTANCES', username='CALCULATING DISTANCES')
                print_help(var=title_distances[i][j], title='TITLE DISTANCES', username='CALCULATING DISTANCES')
                print_help(var=description_distances[i][j], title='DESCRIPTION DISTANCES', username='CALCULATING DISTANCES')
                print_help(var=material_distances[i][j], title='MATERIAL DISTANCES', username='CALCULATING DISTANCES')
                print_help(var=weight_distances[i][j], title='WEIGHT DISTANCES', username='CALCULATING DISTANCES')
                print_help(var=dimension_distances[i][j], title='DIMENSION DISTANCES', username='CALCULATING DISTANCES')
                print_help(var=furniture_location_distances[i][j], title='FURNITURE LOCATION DISTANCES', username='CALCULATING DISTANCES')
                print_help(var=total_distance, title='TOTAL DISTANCES', username='CALCULATING DISTANCES')

                print(f'{i}th => {j}th')
                print('====================================')   

    return data_insert_distance_check_time

def construct_update_item(vectorized_X_color,
                            vectorized_X_material,
                            vectorized_X_description,
                            vectorized_X_title,
                            vectorized_X_furniture_location,
                            all_ids, 
                            all_weight, 
                            all_dimension, 
                            all_price):

    print_help(var='VECT X COLOR', username='MAKE LIST VECTORIZED COLOR')
    vectorized_X_color = vectorized_X_color.tolist()

    print_help(var='VECT X MATERIAL', username='MAKE LIST VECTORIZED MATERIAL')
    vectorized_X_material = vectorized_X_material.tolist()
    
    print_help(var='VECT X DESCRIPTION', username='MAKE LIST VECTORIZED DESCRIPTION')
    vectorized_X_description = vectorized_X_description.tolist()
    
    print_help(var='VECT X TITLE', username='MAKE LIST VECTORIZED TITLE')
    vectorized_X_title = vectorized_X_title.tolist()
    
    print_help(var='VECT X FURNITURE LOCATION', username='MAKE LIST VECTORIZED FURNITURE LOCATION')
    vectorized_X_furniture_location = vectorized_X_furniture_location.tolist()
    

    data_update_item_check_time = []
    for vector_color, vector_material, vector_description, vector_name, vector_furniture_location, _id, weight, dimension, price in \
        zip( vectorized_X_color, vectorized_X_material, vectorized_X_description, vectorized_X_title, vectorized_X_furniture_location , all_ids, all_weight, all_dimension, all_price):
        
        print_help(var=vector_color, title='VECT COLOR', username='PREVIEW VECT COLOR')
        print_help(var=vector_material, title='VECT MATERIAL', username='PREVIEW VECT MATERIAL')
        print_help(var=vector_description, title='VECT DESCRIPTION', username='PREVIEW VECT DESCRIPTION')
        print_help(var=vector_name, title='VECT NAME', username='PREVIEW VECT NAME')
        print_help(var=vector_furniture_location, title='VECT FURNITURE LOCATION', username='PREVIEW VECT FURNITURE LOCATION')
        print_help(var=weight[0], title='VECT WEIGHT', username='PREVIEW VECT WEIGHT')
        print_help(var=dimension[0], title='VECT DIMENSION', username='PREVIEW VECT DIMENSION')
        print_help(var=price[0], title='VECT PRICE', username='PREVIEW VECT PRICE')
        print_help(var=_id, title='ID', username='PREVIEW ID')

        data_update_item_check_time.append(
            (   _id,
                str(vector_color), 
                str(vector_material),
                str(vector_description),
                str(vector_name),
                str(vector_furniture_location),
                weight[0],
                dimension[0],
                float(price[0])
            )
        )

    return data_update_item_check_time

def try_catch_insert_data(script, data, fetch=False, page_size=10000, message=''):
    result = None
    
    try:
        conn = None
        with psycopg2.connect(
                    host = os.environ.get('hostname'),
                    dbname = os.environ.get('database'),
                    user = os.environ.get('username'),
                    password = os.environ.get('pwd'),
                    port = os.environ.get('port_id')) as conn:

            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                print_help(var=str(message), username='TRY CATCH INSERT DATA')
                
                result = psycopg2.extras.execute_values(cur, script, data, template=None, page_size=page_size, fetch=fetch)
                
                print_help(var=str(message) + ' SUCCESSFULY', username='TRY CATCH INSERT DATA')

    except Exception as e:
        print_help(var='EXCEPTION', username='TRY CATCH INSERT DATA')
        print_help(var=e, username='TRY CATCH INSERT DATA')
    finally:
        print_help(var='FINALLY', username='TRY CATCH INSERT DATA')
        if conn is not None:
            conn.close()

        if fetch:
            return result

def count_item(script, data):
    try:
        conn = None
        count = None
        with psycopg2.connect(
                    host = os.environ.get('hostname'),
                    dbname = os.environ.get('database'),
                    user = os.environ.get('username'),
                    password = os.environ.get('pwd'),
                    port = os.environ.get('port_id')) as conn:

            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

                cur.execute(script, data)
                count = cur.fetchone()
    except Exception as e:
        print_help(var='EXCEPTION', username='TRY CATCH INSERT DATA')
        print_help(var=e, username='TRY CATCH INSERT DATA')
    finally:
        print_help(var='FINALLY', username='TRY CATCH INSERT DATA')
        if conn is not None:
            conn.close()

        return count['count']

def truncate_database(script):
    try:
        conn = None
        with psycopg2.connect(
                    host = os.environ.get('hostname'),
                    dbname = os.environ.get('database'),
                    user = os.environ.get('username'),
                    password = os.environ.get('pwd'),
                    port = os.environ.get('port_id')) as conn:

            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(script)
                conn.commit()
                print('TABLE TRUNCATED SUCCESSFULY')

    except Exception as e:
        print_help(var='EXCEPTION', username='TRY CATCH INSERT DATA')
        print_help(var=e, username='TRY CATCH INSERT DATA')
    finally:
        print_help(var='FINALLY', username='TRY CATCH INSERT DATA')
        if conn is not None:
            conn.close()

def script_database(script, data=[]):
    try:
        conn = None
        res = None
        with psycopg2.connect(
                    host = os.environ.get('hostname'),
                    dbname = os.environ.get('database'),
                    user = os.environ.get('username'),
                    password = os.environ.get('pwd'),
                    port = os.environ.get('port_id')) as conn:

            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(script, data)
                res = cur.fetchall()

    except Exception as e:
        print_help(var='EXCEPTION', username='TRY CATCH INSERT DATA')
        print_help(var=e, username='TRY CATCH INSERT DATA')
    finally:
        print_help(var='FINALLY', username='TRY CATCH INSERT DATA')
        if conn is not None:
            conn.close()

        return res

def transfer_data_to_database():
   
    time_log = []
    is_update_distances_feature_vect = True

    start_time = start_timer()

    script = 'SELECT COUNT(*) FROM public.main_app_item'
    count_item_rows = count_item(script=script, data=[])
    check_count_item_rows = try_catch_insert_data(script=script, data=[], fetch=True)
    print(check_count_item_rows)
    
    if count_item_rows > 0:
        # Get Data From Every Module
        _, tmp_data_insert = process_data_item()

        # Truncating Data in Temp Item
        print_help(var='TRUNCATING TEMP ITEM', username='SCRAPING LATEST DATA')

        truncate_script = ''' TRUNCATE TABLE main_app_tempitem '''

        truncate_database(truncate_script)

        # Inserting to Temp Item from Every Module
        tmp_time_start = start_timer()

        print_help(var='INSERTING ITEM TO TEMP ITEM INSTEAD', username='SCRAPING LATEST DATA')

        insert_temp_item_script = '''
        INSERT INTO public.main_app_tempitem( 
                        name, 
                        slug ,
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
                        furniture_location,
                        created_at)
                        VALUES %s
                        RETURNING id
        '''
        all_ids = try_catch_insert_data(script=insert_temp_item_script, 
                                        data=tmp_data_insert, 
                                        fetch=True, 
                                        message='INSERTING TEMP ITEM')

        

        print_help(var=all_ids, title='TOTAL INSERTED' , username='INSERTING TEMP ITEM LATEST DATA')

        time_log = end_timer(start_time=tmp_time_start, time_log=time_log, add_time_log=True, message='INSERTING TEMP ITEM LATEST DATA')

        # Get Temp Item Except Item
        check_temp_item_except_item_script = '''
            SELECT ti.name, ti.slug, ti.price
            FROM main_app_tempitem AS ti
            EXCEPT 
            SELECT i.name, i.slug, i.price
            FROM main_app_item AS i
            ORDER BY NAME ASC
        '''
        unique_temp_item = script_database(script = check_temp_item_except_item_script)
        
        # Get Item Except Temp Item
        check_item_except_temp_item_script = '''
            SELECT i.name, i.slug, i.price
            FROM main_app_item AS i
            EXCEPT 
            SELECT ti.name, ti.slug, ti.price
            FROM main_app_tempitem AS ti
            ORDER BY NAME ASC
        '''
        unique_item = script_database(script = check_item_except_temp_item_script)

        print_help(var=unique_temp_item, title='UNIQUE TEMP ITEM ( NEW ITEM )', username='PREVIEW TEMP ITEM')

        print_help(var=unique_item, title='UNIQUE ITEM ( OLD ITEM )', username='PREVIEW ITEM')
        
        # Get Intersection from Table Item and Temp Item
        tmp_time_start = start_timer()

        # Intersection is List of Item With the Same Name and Slug, but different Price, It Only Needs to Update Price
        intersection = []
        
        # unique_item = [ ['Item Name', 'slug-name', 2600000], [...], [...] ]
        for item in unique_item:
            for temp_item in unique_temp_item:
                if item[0] == temp_item[0] and item[1] == temp_item[1]:
                    intersection.append(temp_item)
                    break
        
        print_help(var=len(unique_item), title='TOTAL DATA UNIQUE ITEM ITERATED' , username='TOTAL DATA UNIQUE ITEM ITERATED')
        
        print_help(var=intersection, title='INTERSECTION OLD AND NEW DATA', username='CHECK INTERSECTION BETWEEN 2 TABLES')

        time_log = end_timer(start_time=tmp_time_start, time_log=time_log, add_time_log=True, message='CHECK INTERSECTION BETWEEN 2 TABLES')

        # Find Old Data that Now Not Exists in Temp Item
        tmp_time_start = start_timer()
        
        # only_item_has is Item That Only Exist in Item, This Need to be Unactive
        only_item_has = []
        
        for item in unique_item:
            is_found = False
            for isc in intersection:
                if item[0] == isc[0] and item[1] == isc[1]:
                    is_found = True
                    break
            
            # Append If Not Found, Because Need to Find LEFT JOIN in Item
            if not is_found:
                only_item_has.append(item)

        print_help(var=len(unique_item), title='TOTAL DATA ONLY_ITEM_HAS ITERATED' , username='TOTAL DATA ONLY_ITEM_HAS ITERATED')
        
        print_help(var=only_item_has, title='DATA ONLY ITEM HAS', username='CHECK ONLY ITEM HAS')

        time_log = end_timer(start_time=tmp_time_start, time_log=time_log, add_time_log=True, message='CHECK ONLY ITEM HAS')

        # Find Data that Doesn't Exists in Item
        tmp_time_start = start_timer()
        
        # only_temp_item_has is Item That Only Exists in Temp Item, This Need to be Inserted to Database
        only_temp_item_has = []

        for temp_item in unique_temp_item:
            is_found = False
            for isc in intersection:
                if temp_item[0] == isc[0] and temp_item[1] == isc[1]:
                    is_found = True
                    break
            
            # Append If Not Found, Because Need to Find LEFT JOIN in Item
            if not is_found:
                only_temp_item_has.append(temp_item)

        print_help(var=len(unique_temp_item), title='TOTAL DATA ONLY_TEMP_ITEM_HAS ITERATED' , username='TOTAL DATA ONLY_TEMP_ITEM_HAS ITERATED')
        
        print_help(var=only_temp_item_has, title='DATA ONLY TEMP ITEM HAS', username='CHECK ONLY TEMP ITEM HAS')
        
        time_log = end_timer(start_time=tmp_time_start, time_log=time_log, add_time_log=True, message='CHECK ONLY TEMP ITEM HAS')
        
        # Check If There's Any Duplicate Between Data That "Now Not Exists in Temp Item" and "Doesn't Exists in Item"
        tmp_time_start = start_timer()

        # Check Duplicate, LEFT JOIN Item and Temp Item must be 0
        check_duplicate = []

        for item in only_item_has:
            for temp_item in only_temp_item_has:
                if item[0] == temp_item[0] and item[1] == temp_item[1]:
                    check_duplicate.append(item)
                    break
        
        print_help(var=len(only_item_has), title='TOTAL DATA TO CHECK DUPLICATE ITERATED' , username='TOTAL DATA TO CHECK DUPLICATE ITERATED')
        
        print_help(var=check_duplicate, title='DATA DUPLICATE', username='CHECK DUPLICATE BETWEEN LEFT JOIN ITEM AND TEMP ITEM')

        time_log = end_timer(start_time=tmp_time_start, time_log=time_log, add_time_log=True, message='CHECK DUPLICATE BETWEEN LEFT JOIN')
        
        # Double Check Status, Sometimes There's Data that Stuck and Need Reactivation
        double_check_intersection_script = '''
            SELECT ti.name, ti.slug, ti.price
            FROM main_app_tempitem AS ti
            INTERSECT 
            SELECT i.name, i.slug, i.price
            FROM main_app_item AS i
            ORDER BY NAME ASC
        '''
        check_intersection = script_database(script = double_check_intersection_script)
        intersection += check_intersection

        print_help(var=check_intersection, title='DOUBLE CHECK INTERSECTION', username='CHECK INTERSECTION FOR 2nd TIME')
        
        time_log = end_timer(start_time=tmp_time_start, time_log=time_log, add_time_log=True, message='CHECK INTERSECTION FOR 2nd TIME')

        # Update Data (price) That Intersect
        tmp_time_start = start_timer()

        # Prepare Intersection Data, Needs () in every data
        # From [ [name, slug, price], [...], [...] ] to [ (name, slug, price, modified_at), (...), (...) ]
        intersection = [ (isc[0], isc[1], isc[2], datetime.datetime.now(LOCAL_TZ), 1) for isc in intersection ]

        # Update Price and Modified At
        update_item_intersection_script = '''
            UPDATE public.main_app_item as t
            SET price = uv.price,
                modified_at = uv.modified_at,
                status = uv.status
            FROM (VALUES %s) AS uv (name,
                                    slug,
                                    price,
                                    modified_at,
                                    status)
            WHERE t.name = uv.name 
                AND t.slug = uv.slug;
        '''

        try_catch_insert_data(script=update_item_intersection_script, 
                                data=intersection, 
                                message='UPDATING PRICE ITEM')
        
        print_help(var='UPDATE PRICE ITEM', username='UPDATE PRICE INTERSECTION OLD AND NEW DATA')

        time_log = end_timer(start_time=tmp_time_start, time_log=time_log, add_time_log=True, message='UPDATE PRICE INTERSECTION OLD AND NEW DATA')

        # Update Status to 0 (Nonactive) to Item
        tmp_time_start = start_timer()

        # From [ [name, slug, price], [...], [...] ] to [ (name, slug, status, modified_at), (...), (...) ]
        only_item_has = [ (item[0], item[1], 0, datetime.datetime.now(LOCAL_TZ)) for item in only_item_has ]

        # Update Status and Modified At
        update_only_item_script = '''
            UPDATE public.main_app_item as t
            SET status = uv.status,
                modified_at = uv.modified_at
            FROM (VALUES %s) AS uv (name,
                                    slug,
                                    status,
                                    modified_at)
            WHERE t.name = uv.name 
                AND t.slug = uv.slug;
        '''

        try_catch_insert_data(script=update_only_item_script, 
                                data=only_item_has, 
                                message='UPDATING STATUS ITEM')
        
        print_help(var='UPDATE STATUS ITEM', username='UPDATE STATUS TO 0 IF OLD DATA DOESNT EXISTS')

        time_log = end_timer(start_time=tmp_time_start, time_log=time_log, add_time_log=True, message='UPDATE STATUS TO 0 IF OLD DATA DOESNT EXISTS')


        # Insert New Item from Temp Item
        tmp_time_start = start_timer()
        
        # From [ [name, slug, price], [...], [...] ] to [ [(name, slug)], [(...)], [(...)] ]
        only_temp_item_has = [ [(temp_item[0], temp_item[1])]  for temp_item in only_temp_item_has ]
        
        fetch_all_only_temp_item_script = '''
            SELECT ti.* 
            FROM public.main_app_tempitem AS ti
            WHERE (ti.name, ti.slug) IN (%s);
        '''
        result_fetch_all_temp_item = try_catch_insert_data(script=fetch_all_only_temp_item_script,
                                data=only_temp_item_has,
                                fetch=True,
                                message='FETCHING TEMP ITEM')
        
        print_help(var=result_fetch_all_temp_item, title='RESULT FETCH ALL TEMP ITEM', username='FETCH TEMP ITEM DATA')
        
        data_insert_temp_item = []

        for result_fetch in result_fetch_all_temp_item:
            tmp_data = ()
            for count, data in enumerate(result_fetch):
                if count == 0 or (count >= 20 and count <= 27):
                    continue
                tmp_data += (data),

            tmp_data += (datetime.datetime.now(LOCAL_TZ), 1)
            data_insert_temp_item.append(tmp_data)

        print_help(var='INSERTING NEW ITEM', username='INSERTING NEW ITEM FROM TEMP ITEM')

        insert_temp_item_script = '''
            INSERT INTO public.main_app_item( 
                            name, 
                            slug ,
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
                            furniture_location,
                            created_at,
                            modified_at,
                            status)
                            VALUES %s
                            RETURNING id
        '''
        all_ids = try_catch_insert_data(script=insert_temp_item_script, 
                                        data=data_insert_temp_item, 
                                        fetch=True, 
                                        message='INSERTING NEW ITEM FROM TEMP ITEM')

        all_ids = [ _id[0] for _id in all_ids]

        print_help(var=all_ids, title='ALL NEW DATA IDS', username='FINISHED INSERTING NEW ITEM FROM TEMP ITEM')

        time_log = end_timer(start_time=tmp_time_start, time_log=time_log, add_time_log=True, message='INSERT NEW ITEM FROM TEMP ITEM')

        # If There's No New Data, It Doesn't Count Distances
        if len(only_temp_item_has) <= 0:
            is_update_distances_feature_vect = False

    else:    
        # Get Data From Every Module
        tmp_time_start = start_timer()
        
        data_insert, _ = process_data_item()
        
        time_log = end_timer(start_time=tmp_time_start, time_log=time_log, add_time_log=True, message='PROCESS DATA ITEM')

        # Inserting Data to Table `Item`
        tmp_time_start = start_timer()

        print_help(var='INSERTING ITEM', username='INSERTING ITEM FROM SCRAPING')

        insert_script = '''
            INSERT INTO public.main_app_item( 
                            name, 
                            slug ,
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
                            furniture_location,
                            created_at,
                            modified_at,
                            status)
                            VALUES %s
                            RETURNING id
        '''
        all_ids = try_catch_insert_data(script=insert_script, 
                                        data=data_insert, 
                                        fetch=True, 
                                        message='INSERTING ITEM')

        all_ids = [ _id[0] for _id in all_ids]

        print_help(var=all_ids, title='ALL IDS', username='FINISHED INSERTING ITEM')

        time_log = end_timer(start_time=tmp_time_start, time_log=time_log, add_time_log=True, message='INSERTING ITEM AND CONSTRUCT IDS')

    # If New Item is Added, System Will Re-Calculating Distances, Feature, and Vectorized Data
    if is_update_distances_feature_vect:
        fetch_all_item_script = '''
            SELECT i.id,
                    i.material, 
                    i.name, 
                    i.description, 
                    i.weight, 
                    i.dimension_length, 
                    i.dimension_width, 
                    i.dimension_height,
                    i.price,
                    i.furniture_location,
                    i.color
            FROM public.main_app_item AS i
        '''
        all_item = script_database(script=fetch_all_item_script, data=[])

        print_help(var=all_item, title='FETCH ALL ITEM', username='FETCH ALL ITEM TO CALCULATE DISTANCES')

        # all_item = [ [material, title, description, weight, dimension, ....], [...], [...] ]
        all_ids, all_material, all_title, all_description, all_weight, all_dimension_length, \
            all_dimension_width, all_dimension_height, all_price, all_furniture_location, all_color = [], [], [], [], [], [], [], [], [], [], []

        for field in all_item:
            # field = [ [material, title, description, weight, dimension, ....] ]
            # This is array destructuring from field variable
            tmp_ids, tmp_material, tmp_title, tmp_description, tmp_weight, tmp_dimension_length, \
            tmp_dimension_width, tmp_dimension_height, tmp_price, tmp_furniture_location, tmp_color = field

            # Append 1 material to array of all material, etc
            all_ids += [tmp_ids]
            all_material += [tmp_material]
            all_title += [tmp_title]
            all_description += [tmp_description]
            all_weight += [tmp_weight]
            all_dimension_length += [tmp_dimension_length]
            all_dimension_width += [tmp_dimension_width]
            all_dimension_height += [tmp_dimension_height]
            all_price += [tmp_price]
            all_furniture_location += [tmp_furniture_location]
            all_color += [tmp_color]

        # Calculate Distance For Every Data
        tmp_time_start = start_timer()

        print_help(var='CALCULATING DISTANCES', username='START CALCULATING DISTANCES')

        vectorized_X_color, color_feature_names, vectorized_X_material, material_feature_names, \
        vectorized_X_furniture_location, furniture_location_feature_names, vectorized_X_description, \
        description_feature_names, vectorized_X_title, title_feature_names, color_distances, material_distances,\
        description_distances, title_distances, furniture_location_distances, all_weight, all_price, \
        all_dimension, weight_distances, dimension_distances, price_distances  = process_data_feature_and_distance(all_material=all_material,
                                                                                                    all_title=all_title,
                                                                                                    all_description=all_description,
                                                                                                    all_weight=all_weight,
                                                                                                    all_dimension_length=all_dimension_length,
                                                                                                    all_dimension_width=all_dimension_width,
                                                                                                    all_dimension_height=all_dimension_height,
                                                                                                    all_price=all_price,
                                                                                                    all_furniture_location=all_furniture_location,
                                                                                                    all_color=all_color)

        print_help(var='FINISHED CALCULATING DISTANCES', username='FINISHED CALCULATING DISTANCES')

        time_log = end_timer(start_time=tmp_time_start, time_log=time_log, add_time_log=True, message='PROCESS DATA FEATURE AND DISTANCE')

        # Truncating Table Distances
        print_help(var='TRUNCATING TABLE DISTANCES', username='TRUNCATE TABLE TO INSERT NEW DISTANCES')

        truncate_script = '''TRUNCATE TABLE main_app_distance'''

        truncate_database(truncate_script)

        # Constructing Distances
        tmp_time_start = start_timer()
        
        data_insert_distance = construct_distances(all_ids=all_ids,
                                                                color_distances=color_distances,
                                                                material_distances=material_distances,
                                                                description_distances=description_distances,
                                                                title_distances=title_distances,
                                                                furniture_location_distances=furniture_location_distances,
                                                                weight_distances=weight_distances,
                                                                dimension_distances=dimension_distances,
                                                                price_distances=price_distances )

        print_help(var='FINISHED CONSTRUCTING DISTANCES', username='FINISHED CONSTRUCTING DISTANCES')

        time_log = end_timer(start_time=tmp_time_start, time_log=time_log, add_time_log=True, message='CONSTRUCT DISTANCES')

        # Inserting Distances
        tmp_time_start = start_timer()

        print_help(var='INSERTING DISTANCES', username='INSERTING DISTANCES')

        insert_distance_script = '''
            INSERT INTO public.main_app_distance (
                product_id, 
                other_product_id, 
                color_distance, 
                name_distance, 
                description_distance, 
                material_distance, 
                weight_distance,  
                dimension_distance, 
                price_distance, 
                furniture_location_distance,
                total_distance,
                temp_distance,
                feature_added
            )
            VALUES %s;
        '''
        try_catch_insert_data(script=insert_distance_script, 
                                data=data_insert_distance, 
                                message='INSERTING DISTANCE')

        print_help(var='FINISHED INSERTING DISTANCES', username='FINISHED INSERTING DISTANCES')

        time_log = end_timer(start_time=tmp_time_start, time_log=time_log, add_time_log=True, message='INSERTING DISTANCES')

        # Construct Update Item (Vect Data)
        tmp_time_start = start_timer()
        
        data_update_item = construct_update_item(vectorized_X_color=vectorized_X_color,
                                                            vectorized_X_material=vectorized_X_material,
                                                            vectorized_X_description=vectorized_X_description,
                                                            vectorized_X_title=vectorized_X_title,
                                                            vectorized_X_furniture_location=vectorized_X_furniture_location,
                                                            all_ids=all_ids, 
                                                            all_weight=all_weight, 
                                                            all_dimension=all_dimension, 
                                                            all_price=all_price)

        print_help(var='FINISHED CONSTRUCTING UPDATE ITEM', username='FINISHED CONSTRUCTING ITEM VECT DATA')

        time_log = end_timer(start_time=tmp_time_start, time_log=time_log, add_time_log=True, message='CONSTRUCT UPDATE ITEM')

        # Update Item (Vect Data)
        tmp_time_start = start_timer()
        
        print_help(var='UPDATING ITEM', username='UPDATING ITEM VECT DATA')
        
        update_item_script = '''
            UPDATE public.main_app_item as t
            SET vect_color = uv.vect_color, 
                vect_material = uv.vect_material, 
                vect_description = uv.vect_description, 
                vect_name = uv.vect_name, 
                vect_furniture_location = uv.vect_furniture_location,
                normalized_weight = uv.normalized_weight, 
                normalized_dimension = uv.normalized_dimension,
                normalized_price = uv.normalized_price
            FROM (VALUES %s) AS uv (id,
                                    vect_color, 
                                    vect_material, 
                                    vect_description, 
                                    vect_name, 
                                    vect_furniture_location, 
                                    normalized_weight, 
                                    normalized_dimension,
                                    normalized_price)
            WHERE t.id = uv.id;
        '''

        try_catch_insert_data(script=update_item_script, 
                                data=data_update_item, 
                                message='UPDATING ITEM')

        print_help(var='FINISHED UPDATING ITEM', username='FINISHED UPDATING ITEM VECT DATA')

        time_log = end_timer(start_time=tmp_time_start, time_log=time_log, add_time_log=True, message='UPDATE ITEM')

        # Inserting Feature
        tmp_time_start = start_timer()
        
        print_help(var='INSERTING FEATURE', username='INSERTING FEATURE')
        
        insert_feature_script = '''
            INSERT INTO public.main_app_feature(
                        name_feature, 
                        color_feature, 
                        material_feature, 
                        description_feature, 
                        furniture_location_feature )
            VALUES %s;
        '''
        data_insert_feature = [
            (
                title_feature_names,
                color_feature_names,
                material_feature_names,
                description_feature_names,
                furniture_location_feature_names
            )
        ]
        
        try_catch_insert_data(script=insert_feature_script, 
                                data=data_insert_feature, 
                                message='INSERTING FEATURE')

        print_help(var='FINISHED INSERTING FEATURE', username='FINISHED INSERTING FEATURE')
        
        time_log = end_timer(start_time=tmp_time_start, time_log=time_log, add_time_log=True, message='INSERTING FEATURE')

    time_log = end_timer(start_time=start_time, time_log=time_log, add_time_log=True, message='TOTAL PROGRAM RUNTIME')

    [ print(log) for log in time_log ]

RUN_SCRAPING = False
RUN_TRANSFER_DATA = True

if __name__ == '__main__':
    if RUN_SCRAPING:
        run_all_web_scraper()

    if RUN_TRANSFER_DATA:
        transfer_data_to_database()