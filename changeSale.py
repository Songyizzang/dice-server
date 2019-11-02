import json
import boto3
import sys
import logging
import pymysql
import ast
from urllib.parse import urlsplit, parse_qsl


host=
username=
pw=
db=


class Sale:
    def __init__(self, product_id, saleType, percent, eventType, startdate, enddate):
        self.product_id = product_id
        self.saleType = saleType
        self.percent = percent
        self.eventType = eventType
        self.startdate = startdate
        self.enddate = enddate
        




def lambda_handler(event, context):
    
    conn = pymysql.connect(host=host, user=username, password=pw, db=db,charset='utf8')
    cursor = conn.cursor()
    
    result = dict()
    data = event.get('body')
    dicdata = dict(parse_qsl(urlsplit(data).path))
    
    tmp = dicdata
    
    
    
    
    if dicdata.get('isSale') is '1': #세일한다고 바꿀 때 
        sale = Sale(dicdata.get('product_id'), dicdata.get('saleType'), dicdata.get('percent'), dicdata.get('eventType'),dicdata.get('startdate'), dicdata.get('enddate'))
        
        query1 = "UPDATE product SET isSale = 1 WHERE product_id= " + sale.product_id
        query2 = "insert into sale(sale_type,sale_percent,sale_startdate,sale_enddate,product_id,sale_eventtype) values(" + sale.saleType + ", " + sale.percent + ", \'" + sale.startdate + "\', \'" + sale.enddate + "\', " + sale.product_id + ", \'" + sale.eventType +"\')"

        rst1 = cursor.execute(query1)
        rst2 = cursor.execute(query2)

        if rst1 is 1 and rst2 is 1:
            conn.commit()
            result['isSuccess'] = 1
            
            
            #mqtt
            display_query = "SELECT display_id from display where product_id = " + dicdata.get('product_id')
            display_id = cursor.execute(display_query)
            
            client = boto3.client('iot-data', region_name='ap-northeast-2')
            dic = dict()
            dic['t'] = sale.saleType
            dic['p'] = sale.percent
            dic['et'] = sale.eventType
            dic['d'] = sale.startdate + " ~ " + sale.enddate
            
            response = client.publish(
                topic = "no" + str(display_id),
                qos=1,
                payload=json.dumps(dic,ensure_ascii=False)
            )
            
        else:
            result['isSuccess'] = 0
        
    if dicdata.get('isSale') is '0': #세일안한다고 바꿀 때 
        update_query = "UPDATE product SET isSale = 0 WHERE product_id = " + dicdata.get('product_id')
        rst = cursor.execute(update_query)
           
            
        if rst is 1:
            conn.commit()
            result['isSuccess'] = 1
            
            #mqtt
            display_query = "SELECT display_id from display where product_id = " + dicdata.get('product_id')
            display_id = cursor.execute(display_query)
            
            client = boto3.client('iot-data', region_name='ap-northeast-2')
            dic = dict()
            dic['isSale'] = '0'
            
            response = client.publish(
                topic = "no" + str(display_id),
                qos=1,
                payload=json.dumps(dic,ensure_ascii=False)
            )
        
        else:
            result['isSuccess'] = 0
    
    
    cursor.close()
    conn.close()
    
        
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }