import requests
import json
import time
import os
from database import DataBase

file_names = [
    ('1.jpg', 'hybrid'), # 012-34-589
    ('2.jpg', 'fuel'), # 750-62-834
    ('4.jpg', 'hybrid'),  # 29-521-65
    ('5.jpg', 'fuel'),  # 19-210-2017
    ('6.jpg', 'hybrid'), # 26-405-20
    ('25.jpg','public'), # 012-34-525
    ('26.jpg','public'), # 012-34-526
    ('30.jpg','fuel'), # 012-34-530
    ('45.jpg','hybrid'), # 012-34-545
    ('90.jpg', 'fuel'), # 29-521-90
    ('00.jpg', 'hybrid'), # 012-34-500
]

def parking_entrance(file_name):
    car_number = get_car_number_from_image(file_name)
    if car_number == 0:
        raise Exception('failed to retrieve car number from image file: '+file_name)
    can_enter= parking_permission_check(car_number)
    return can_enter, car_number

def get_car_number_from_image(file_name):
    url = 'https://api.ocr.space/parse/image'
    headers = {
        'apikey': '71c2191a3688957',
        # 'apikey': 'helloworld',
    }

    payload = {
        'OCREngine' : '2',
        'scale' : 'true',
        'filetype' : 'JPG',
        'language' : 'eng'
    }

    files = [
        ('upload_file', (file_name, open(file_name, 'rb'), 'image/jpeg'))
    ]
    with requests.Session() as s:
        r = s.post(url, files=files, data= payload,headers=headers)

    try:
        if r.status_code != 200:
            raise Exception('failed to upload image file , status:'+ str(r.status_code))
        content = json.loads(r.content)
        parsed_result = content['ParsedResults']
        parsed_text = parsed_result[0]['ParsedText']
        car_number_items = parsed_text.split('\n')
        car_number = car_number_items[0].replace('\r', '')
        parts = []
        for index in range(0, len(car_number)):
            char = car_number[index]
            if char.isdigit():
                parts.append(char)
            else:
                parts.append('-')
        plate_number = ''.join(parts)
        print(plate_number)
    except Exception as e:
        print('couldnt retrieve car number, '+ e.message )
        raise
    return plate_number

def parking_permission_check(car_number):
    can_enter= False
    public_tansport = ['25','26']
    last_digits = ['85','86','87','88','89','00']
    seven_digits = ['0','5']

    start, middle, end = car_number.split('-')
    license_len = len(start) + len(middle) + len(end)
    last_digit = end[len(end)-1:]
    last_2_digits = end[len(end)-2:]

    if license_len == 7:
        if last_digit not in seven_digits:
            can_enter = True
    else:
        if last_2_digits in public_tansport:
            can_enter = True
        elif last_2_digits not in last_digits:
            can_enter = True

    return can_enter


def write_result_in_database(license_number,can_enter,car_type ):
    timestamp = time.time()
    if can_enter:
        allowed = 'allowed'
    else:
        allowed = 'denied'
    database.insert(license_number,allowed,timestamp,car_type)


if __name__ == "__main__":
    database = DataBase()
    database.create_database()

    for file_name in file_names:
        current_dir = os.getcwd()
        image_file_name = file_name[0]
        car_type = file_name[1]
        full_file_path = os.path.join(current_dir,image_file_name)
        can_enter, license_number = parking_entrance(full_file_path)
        if can_enter :
            print ('{} can enter the parking'.format(license_number))
        else:
            print ('{} is not allowed to enter the parking'.format(license_number))
        write_result_in_database(license_number,can_enter,car_type)

    visitors_list = database.get_all_visitors()
    if visitors_list:
        for visitor in visitors_list:
            print visitor
    else:
        print (' Visitors table is empty! ')

    # close database connection
    database.close()

