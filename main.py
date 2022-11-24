import psycopg2
import psycopg2.extras
import os
from slugify import slugify
from ml_helper import *

import numpy as np
import time 
import datetime
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

######################################################################

    try:
        from Tokopedia import all_data as Tokopedia_All_Data
        Tokopedia_All_Data = Tokopedia_All_Data.all_data

    except ImportError as e:
        show_error_message(e, 'Tokopedia')

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
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                    RETURNING id '''

                all_records = get_all_data()
                                
                print('=========================================')
                all_ids = []
                all_material, all_title, all_title, all_description, all_weight, all_dimension_length = [], [], [], [], [], []
                all_dimension_width, all_dimension_height, all_price, all_furniture_location, all_color = [], [], [], [], []
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

                        tmp_data = (data['name'], 
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
                                    ','.join(data['furnitureLocation']))
                        cur.execute(insert_script, tmp_data)

                        _id = cur.fetchone()
                        all_ids.append(int(_id[0]))
                    print(record[1] + ' DATA INSERTED SUCCESSFULY')
                
                # Get Vectorized_X and Feature Names for Categorical Featuers
                vectorized_X_color, color_feature_names = bag_of_words(all_color)
                vectorized_X_material, material_feature_names = bag_of_words(all_material, delimiter='comma')
                vectorized_X_furniture_location, furniture_location_feature_names = bag_of_words(all_furniture_location, delimiter='comma')
                vectorized_X_description, description_feature_names = bag_of_words(all_description)
                vectorized_X_title, title_feature_names = bag_of_words(all_title)

                # Get Distances for Categorical Features
                color_distances = find_all_distance(vectorized_X_color,is_normalized_data=True, is_standard_scaler=False)
                material_distances = find_all_distance(vectorized_X_material,is_normalized_data=True, is_standard_scaler=False)
                description_distances = find_all_distance(vectorized_X_description,is_normalized_data=True, is_standard_scaler=False)
                title_distances = find_all_distance(vectorized_X_title,is_normalized_data=True, is_standard_scaler=False)
                furniture_location_distances = find_all_distance(vectorized_X_furniture_location,is_normalized_data=True, is_standard_scaler=False)

                # Reshape All Numerical Features
                all_weight = np.asarray(all_weight).reshape(-1, 1)
                all_price = np.asarray(all_price).reshape(-1, 1)

                all_dimension = []

                for length, width, height in zip(all_dimension_length, all_dimension_width, all_dimension_height):
                    length = float(length) if length != '' else 0
                    width = float(width) if width != '' else 0
                    height = float(height) if height != '' else 0
                    all_dimension.append([length , width, height ])


                weight_distances = find_all_distance(all_weight,is_normalized_data=True, is_standard_scaler=False)
                dimension_distances = find_all_distance(all_dimension,is_normalized_data=True, is_standard_scaler=False)
                price_distances = find_all_distance(all_price,is_normalized_data=True, is_standard_scaler=False)


                start_time = time.perf_counter()
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
                        temp_distance
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );
                '''
                
                for i in range(len(all_ids)):
                    for j in range(i, len(all_ids)-1):
                        if i % 400 == 0 and j % 400 == 0:
                            print('====================================')
                            print(f'{i}th => {j}th')
                            print(all_ids[i])
                            print(all_ids[j])
                            print(color_distances[i][j])
                            print(f'{start_time} has passed')
                            print('====================================')
                        total_distance = float(color_distances[i][j]) + float(title_distances[i][j]) + float(description_distances[i][j]) + float(material_distances[i][j]) \
                                + float(weight_distances[i][j]) + float(dimension_distances[i][j]) + float(price_distances[i][j]) + float(furniture_location_distances[i][j])

                        tmp_data = (
                            all_ids[i] ,
                            all_ids[j],
                            color_distances[i][j],
                            title_distances[i][j],
                            description_distances[i][j],
                            material_distances[i][j],
                            weight_distances[i][j],
                            dimension_distances[i][j],
                            price_distances[i][j],
                            furniture_location_distances[i][j],
                            total_distance,
                            99.0
                        )

                        cur.execute(insert_distance_script,tmp_data)

                print('TOTAL INSERTING DISTANCE')
                print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time)))


                start_time = time.perf_counter()

                update_item_script = '''
                UPDATE public.main_app_item
                SET vect_color = %s, 
                    vect_material = %s, 
                    vect_description = %s, 
                    vect_name = %s, 
                    vect_furniture_location = %s,
                    normalized_weight = %s, 
                    normalized_dimension = %s,
                    normalized_price = %s
                WHERE id = %s;
                '''
                vectorized_X_color = vectorized_X_color.tolist()
                vectorized_X_material = vectorized_X_material.tolist()
                vectorized_X_description = vectorized_X_description.tolist()
                vectorized_X_title = vectorized_X_title.tolist()
                vectorized_X_furniture_location = vectorized_X_furniture_location.tolist()
                
                for vector_color, vector_material, vector_description, vector_name, vector_furniture_location, _id, weight, dimension, price in \
                    zip( vectorized_X_color, vectorized_X_material, vectorized_X_description, vectorized_X_title, vectorized_X_furniture_location , all_ids, all_weight, all_dimension, all_price):
                    
                    tmp_data = (
                        vector_color, 
                        vector_material,
                        vector_description,
                        vector_name,
                        vector_furniture_location,
                        weight[0],
                        dimension[0],
                        price[0],
                        _id
                    )

                    cur.execute(update_item_script,tmp_data)
                
                print('TOTAL UPDATING VECTOR')
                print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time)))


                start_time = time.perf_counter()

                insert_feature_script = '''
                INSERT INTO public.main_app_feature(
                    name_feature, color_feature, material_feature, description_feature, 
                    furniture_location_feature )
                    VALUES (%s, %s, %s, %s, %s);
                '''
                tmp_data = (
                    title_feature_names,
                    color_feature_names,
                    material_feature_names,
                    description_feature_names,
                    furniture_location_feature_names
                )
                cur.execute(insert_feature_script,tmp_data)

                print('TOTAL INSERTING FEATURE')
                print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time)))

                print(color_feature_names)
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