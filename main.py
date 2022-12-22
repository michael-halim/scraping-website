import psycopg2
import psycopg2.extras
import os
from slugify import slugify
from ml_helper import *

import numpy as np
import time 
import datetime

def print_help(var, title=''):
    print('============================================')
    if isinstance(var, str) and title == '':
        print(var)
        print('============================================')

    else:
        print(title)
        print(var)
        try:
            print(f'LENGTH : {len(var)}')
            print('============================================')
        except TypeError as e:
            print('============================================')

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

    import datetime
    print('ALL SCRAPING RUNTIME')
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time_parent)))


def process_data_item():
    all_records = get_all_data()
    data_insert_check_time = []
    all_material, all_title, all_title, all_description, all_weight, all_dimension_length = [], [], [], [], [], []
    all_dimension_width, all_dimension_height, all_price, all_furniture_location, all_color = [], [], [], [], []
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
            

            all_material.append(data['material'])
            all_color.append(data['color'])
            all_description.append(data['description'])
            all_title.append(data['name'])
            all_weight.append(weight)
            all_dimension_length.append(dimension_length)
            all_dimension_height.append(dimension_height)
            all_dimension_width.append(dimension_width)
            all_price.append(data['price'])
            all_furniture_location.append(','.join(data['furnitureLocation']))

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
                    data['material'],
                    weight,
                    data['weight_unit'],
                    data['color'],
                    dimension_length,
                    dimension_width,
                    dimension_height,
                    data['dimension_unit'], 
                    isProduct,
                    ','.join(data['furnitureLocation'])
                )
            )
        print(record[1] + ' DATA PROCESSED SUCCESSFULY')
    return all_material, all_title, all_description, all_weight, all_dimension_length, all_dimension_width, all_dimension_height, \
            all_price, all_furniture_location, all_color, data_insert_check_time

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
    print_help('BAG OF WORDS CATEGORICAL')
    # Get Vectorized_X and Feature Names for Categorical Featuers
    print_help('BOW COLOR')
    vectorized_X_color, color_feature_names = bag_of_words(all_color)

    print_help('BOW MATERIAL')
    vectorized_X_material, material_feature_names = bag_of_words(all_material, delimiter='comma')
    
    print_help('BOW FURNITURE LOCATION')
    vectorized_X_furniture_location, furniture_location_feature_names = bag_of_words(all_furniture_location, delimiter='comma')
    
    print_help('BOW DESCRIPTION')
    vectorized_X_description, description_feature_names = bag_of_words(all_description)
    
    print_help('BOW TITLE')
    vectorized_X_title, title_feature_names = bag_of_words(all_title)
    
    all_dimension = []

    for length, width, height in zip(all_dimension_length, all_dimension_width, all_dimension_height):
        length = float(length) if length != '' else 0
        width = float(width) if width != '' else 0
        height = float(height) if height != '' else 0
        all_dimension.append([length , width, height ])

    # Get Distances for Categorical Features
    print_help('FINDING COLOR DISTANCES....')
    color_distances = find_all_distance(vectorized_X_color,is_normalized_data=True, is_standard_scaler=False)
    
    print_help('FINDING MATERIAL DISTANCES....')
    material_distances = find_all_distance(vectorized_X_material,is_normalized_data=True, is_standard_scaler=False)
    
    print_help('FINDING DESCRIPTION DISTANCES....')
    description_distances = find_all_distance(vectorized_X_description,is_normalized_data=True, is_standard_scaler=False)
    
    print_help('FINDING TITLE DISTANCES....')
    title_distances = find_all_distance(vectorized_X_title,is_normalized_data=True, is_standard_scaler=False)
    
    print_help('FINDING FURNITURE LOCATION DISTANCES....')
    furniture_location_distances = find_all_distance(vectorized_X_furniture_location,is_normalized_data=True, is_standard_scaler=False)

    # Reshape All Numerical Features
    all_weight = np.asarray(all_weight).reshape(-1, 1)
    all_price = np.asarray(all_price).reshape(-1, 1)

    print_help('FINDING WEIGHT DISTANCES....')
    weight_distances = find_all_distance(all_weight,is_normalized_data=True, is_standard_scaler=False)
    
    print_help('FINDING DIMENSION DISTANCES....')
    dimension_distances = find_all_distance(all_dimension,is_normalized_data=True, is_standard_scaler=False)
    
    print_help('FINDING PRICE DISTANCES....')
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
                    99.0
                )
            )
            if i % 400 == 0 and j % 400 == 0:
                print('====================================')
                print_help(color_distances[i][j], 'COLOR DISTANCES')
                print_help(title_distances[i][j], 'TITLE DISTANCES')
                print_help(description_distances[i][j], 'DESCRIPTION DISTANCES')
                print_help(material_distances[i][j], 'MATERIAL DISTANCES')
                print_help(weight_distances[i][j], 'WEIGHT DISTANCES')
                print_help(dimension_distances[i][j], 'DIMENSION DISTANCES')
                print_help(furniture_location_distances[i][j], 'FURNITURE LOCATION DISTANCES')
                print_help(total_distance, 'TOTAL DISTANCES')

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

    print_help('VECT X COLOR')
    vectorized_X_color = vectorized_X_color.tolist()

    print_help('VECT X MATERIAL')
    vectorized_X_material = vectorized_X_material.tolist()
    
    print_help('VECT X DESCRIPTION')
    vectorized_X_description = vectorized_X_description.tolist()
    
    print_help('VECT X TITLE')
    vectorized_X_title = vectorized_X_title.tolist()
    
    print_help('VECT X FURNITURE LOCATION')
    vectorized_X_furniture_location = vectorized_X_furniture_location.tolist()
    

    data_update_item_check_time = []
    for vector_color, vector_material, vector_description, vector_name, vector_furniture_location, _id, weight, dimension, price in \
        zip( vectorized_X_color, vectorized_X_material, vectorized_X_description, vectorized_X_title, vectorized_X_furniture_location , all_ids, all_weight, all_dimension, all_price):
        
        print_help(vector_color, 'VECT COLOR')
        print_help(vector_material, 'VECT MATERIAL')
        print_help(vector_description, 'VECT DESCRIPTION')
        print_help(vector_name, 'VECT NAME')
        print_help(vector_furniture_location, 'VECT FURNITURE LOCATION')
        print_help(weight[0], 'VECT WEIGHT')
        print_help(dimension[0], 'VECT DIMENSION')
        print_help(price[0], 'VECT PRICE')
        print_help(_id, 'ID')

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
                print(message)
                if fetch:
                    result = psycopg2.extras.execute_values(cur, script, data, template=None, page_size=page_size, fetch=fetch)
                else:
                    psycopg2.extras.execute_values(cur, script, data, template=None, page_size=page_size, fetch=fetch)
                print(message, 'SUCCESSFULY')
    except Exception as e:
        print('EXCEPTION')
        print(e)
    finally:
        print('FINALLY')
        print(conn)
        print(type(conn))
        if conn is not None:
            conn.close()

        if fetch:
            return result

def transfer_data_to_database():
    """  TESTING FASTER TIME QUERY """

    time_log = []
    start_time = time.perf_counter()

    tmp_time = time.perf_counter()
    # === Process ===
    all_material, all_title, all_description, all_weight, all_dimension_length, all_dimension_width, \
    all_dimension_height, all_price, all_furniture_location, all_color, data_insert_check_time = process_data_item()
    # === End Process ===
    time_log.append(('PROCESS DATA ITEM', str(datetime.timedelta(seconds = time.perf_counter() - tmp_time)) ) )
    print('PROCESS DATA ITEM')
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - tmp_time)))


    tmp_time = time.perf_counter()
    # === Process ===
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
    # === End Process ===
    time_log.append(('PROCESS DATA FEATURE AND DISTANCE', str(datetime.timedelta(seconds = time.perf_counter() - tmp_time)) ) )
    print('PROCESS DATA FEATURE AND DISTANCE')
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - tmp_time)))

    tmp_time = time.perf_counter()
    # === Process ===
    insert_script_check_time = '''
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
                        furniture_location)
                        VALUES %s
                        RETURNING id
    '''
    all_ids = try_catch_insert_data(script=insert_script_check_time, 
                                    data=data_insert_check_time, 
                                    fetch=True, 
                                    message='INSERTING ITEM')
    all_ids = [ _id[0] for _id in all_ids]
    # === End Process ===
    time_log.append(('INSERTING ITEM AND CONSTRUCT IDS', str(datetime.timedelta(seconds = time.perf_counter() - tmp_time)) ) )
    print('INSERTING ITEM AND CONSTRUCT IDS')
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - tmp_time)))

    tmp_time = time.perf_counter()
    # === Process ===
    data_insert_distance_check_time = construct_distances(all_ids=all_ids,
                                                            color_distances=color_distances,
                                                            material_distances=material_distances,
                                                            description_distances=description_distances,
                                                            title_distances=title_distances,
                                                            furniture_location_distances=furniture_location_distances,
                                                            weight_distances=weight_distances,
                                                            dimension_distances=dimension_distances,
                                                            price_distances=price_distances )
    # === End Process ===
    time_log.append(('CONSTRUCT DISTANCES', str(datetime.timedelta(seconds = time.perf_counter() - tmp_time)) ) )
    print('CONSTRUCT DISTANCES')
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - tmp_time)))

    tmp_time = time.perf_counter()
    # === Process ===
    insert_distance_script_check_time = '''
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
            temp_distance
        )
        VALUES %s;
    '''
    try_catch_insert_data(script=insert_distance_script_check_time, 
                            data=data_insert_distance_check_time, 
                            message='INSERTING DISTANCE')
    # === End Process ===
    time_log.append(('INSERTING DISTANCES', str(datetime.timedelta(seconds = time.perf_counter() - tmp_time)) ) )
    print('INSERTING DISTANCES')
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - tmp_time)))


    tmp_time = time.perf_counter()
    # === Process ===
    data_update_item_check_time = construct_update_item(vectorized_X_color=vectorized_X_color,
                                                        vectorized_X_material=vectorized_X_material,
                                                        vectorized_X_description=vectorized_X_description,
                                                        vectorized_X_title=vectorized_X_title,
                                                        vectorized_X_furniture_location=vectorized_X_furniture_location,
                                                        all_ids=all_ids, 
                                                        all_weight=all_weight, 
                                                        all_dimension=all_dimension, 
                                                        all_price=all_price)
    # === End Process ===
    time_log.append(('CONSTRUCT UPDATE ITEM', str(datetime.timedelta(seconds = time.perf_counter() - tmp_time)) ) )
    print('CONSTRUCT UPDATE ITEM')
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - tmp_time)))

    tmp_time = time.perf_counter()
    # === Process ===
    update_item_script_check_time = '''
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

    try_catch_insert_data(script=update_item_script_check_time, 
                            data=data_update_item_check_time, 
                            message='UPDATING ITEM')
    # === End Process ===
    time_log.append(('UPDATE ITEM', str(datetime.timedelta(seconds = time.perf_counter() - tmp_time)) ) )
    print('UPDATE ITEM')
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - tmp_time)))

    tmp_time = time.perf_counter()
    # === Process ===
    insert_feature_script_check_time = '''
        INSERT INTO public.main_app_feature(
                    name_feature, 
                    color_feature, 
                    material_feature, 
                    description_feature, 
                    furniture_location_feature )
        VALUES %s;
    '''
    data_insert_feature_check_time = [
        (
            title_feature_names,
            color_feature_names,
            material_feature_names,
            description_feature_names,
            furniture_location_feature_names
        )
    ]
    
    try_catch_insert_data(script=insert_feature_script_check_time, 
                            data=data_insert_feature_check_time, 
                            message='INSERTING FEATURE')
    # === End Process ===
    time_log.append(('INSERTING FEATURE', str(datetime.timedelta(seconds = time.perf_counter() - tmp_time)) ) )
    print('INSERTING FEATURE')
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - tmp_time)))

    print('TOTAL INSERTING DATA')
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time)))
    
    [ print(log) for log in time_log ]

RUN_SCRAPING = False
RUN_TRANSFER_DATA = True

if __name__ == '__main__':
    if RUN_SCRAPING:
        run_all_web_scraper()

    if RUN_TRANSFER_DATA:
        transfer_data_to_database()