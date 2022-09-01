import psycopg2
import psycopg2.extras
import os
from slugify import slugify
from AERDekoruma import all_data as AER_Dekoruma_All_Data
from AtesonHome import all_data as Ateson_Home_All_Data
from Balkaliving import all_data as Balkaliving_All_Data
from Nagarey import all_data as Nagarey_All_Data
from SohoID import all_data as SohoID_All_Data
from AERTEKA import all_data as AER_TEKA_All_Data
from AERDobidos import all_data as AER_Dobidos_All_Data
from AERGree import all_data as AER_Gree_All_Data
from AERSharp import all_data as AER_Sharp_All_Data
from AERPaloma import all_data as AER_Paloma_All_Data


AER_Dekoruma_All_Data = AER_Dekoruma_All_Data.all_data
Ateson_Home_All_Data = Ateson_Home_All_Data.all_data
Balkaliving_All_Data = Balkaliving_All_Data.all_data
Nagarey_All_Data = Nagarey_All_Data.all_data
SohoID_All_Data = SohoID_All_Data.all_data
AER_TEKA_All_Data = AER_TEKA_All_Data.all_data
AER_Dobidos_All_Data = AER_Dobidos_All_Data.all_data
AER_Gree_All_Data = AER_Gree_All_Data.all_data
AER_Sharp_All_Data = AER_Sharp_All_Data.all_data
AER_Paloma_All_Data = AER_Paloma_All_Data.all_data


if __name__ == '__main__':
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

                all_records = [(AER_Dekoruma_All_Data, 'AER DEKORUMA'), 
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