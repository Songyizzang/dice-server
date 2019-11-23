import boto3
import sys
import logging
import pymysql
import json
from urllib.parse import urlsplit, parse_qsl

host=
username=
pw=
db=


class Product:
    def __init__(self, brand, name, price, capacity, unit):
        self.brand = brand
        self.name = name
        self.price = price
        self.capacity = capacity
        self.unit = unit


def lambda_handler(event, context):
    
    httpmethod = event.get('httpMethod')
    
    #db 연결
    conn = pymysql.connect(host=host, user=username, password=pw, db=db,charset='utf8')
    curs = conn.cursor()
    result = dict()
    
    if httpmethod == "GET":
        
        query = "SELECT display.display_id,  product.product_id FROM display, product WHERE product.product_id = display.product_id"
        key = "display"
        curs.execute(query)
        
        result[key] = []
        
        display = curs.fetchall()
        for col in display:
            tmp = dict()
            tmp['display_id'] = col[0]
            tmp['product_id'] = col[1]
        
            result[key].append(tmp)
            
    
    elif httpmethod == "POST":
        #data = event.get('body')
        #param = dict(parse_qsl(urlsplit(data).path))
        
        rst1 = 0
        query1 = "insert into display(display_id, product_id) values(display_id," + "\'" + "product_id ," + "\')"
        rst1 = curs.execute(query1)
    
        if rst1 == 1:
            result['isSuccess'] = 1
            conn.commit()
            
    
        else:
            result['isSuccess'] = 0
        
    elif httpmethod == "PUT":
        data = event.get('body')
        param = dict(parse_qsl(urlsplit(data).path))
        display_id = param.get('display_id')
        product_id = param.get('product_id')
        
        rst2 = 0
        query2 = "UPDATE display SET product_id = " + param['product_id']  + " where display_id = " + param['display_id']
        rst2 = curs.execute(query2)
        
        if rst2 == 1:
            result['isSuccess'] = 1
            conn.commit()
            #mqtt
            pro_info_query = "SELECT common_brand,common_name,common_price,common_capacity,common_unit FROM common WHERE product_id = " + param['product_id']
            curs.execute(pro_info_query)
            r = curs.fetchone()
            
            product = Product(r[0], r[1], r[2], r[3], r[4])
            
            mqtt_msg = dict()
            mqtt_msg['bnc'] = "[" + product.brand + "] " + product.name + " " + str(product.capacity) + str(product.unit)
            mqtt_msg['price'] = str(product.price)
            mqtt_msg['ca'] = str(product.capacity)
            
            if int(product.capacity) < 100:
                tmp_unit = int(product.price) / int(product.capacity) * 10
                mqtt_msg['unit'] = "10" + product.unit + " / "+ str(int(tmp_unit))

            else:
                tmp_unit = int(product.price) / int(product.capacity) * 100
                mqtt_msg['unit'] = "100" + product.unit + " / "+ str(int(tmp_unit))
            
            
            
            client = boto3.client('iot-data', region_name='ap-northeast-2')
        
            response = client.publish(
                topic = "no" + str(display_id),
                qos=1,
                payload=json.dumps(mqtt_msg,ensure_ascii=False)
            )
        
        else:
            result['isSuccess'] = 0
            
        
    curs.close()
    conn.close()
    
    return {
        'statusCode':200,
        'body':json.dumps(result,ensure_ascii=False)
    }