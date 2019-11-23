import json
import boto3
import sys
import logging
import pymysql
import ast



host="dicerds.cn7oixdffz0i.ap-northeast-2.rds.amazonaws.com"
username="root"
pw="root1234"
db="dicedb"


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
    curs = conn.cursor()
    result = dict()
    
    query = "SELECT product.product_id, display_id, product.product_type FROM product,sale,display WHERE isSale = 1 AND sale_enddate < now();"
    curs.execute(query)
    
    rst = curs.fetchall()
    for col in rst:
        endSaleQuery = "UPDATE product SET isSale = 0 WHERE product_id = " + str(col[0])
        rst = curs.execute(endSaleQuery)
        print (str(col[0]))
        
        if rst is 1 :
            conn.commit()
            client = boto3.client('iot-data', region_name='ap-northeast-2')
            dic = dict()
            dic['isSale'] = '0'
            
            print(str(col[1]))
            
            response = client.publish(
                topic = "no" + str(col[1]),
                qos=1,
                payload=json.dumps(dic,ensure_ascii=False)
            )
            
    curs.close()
    conn.close()
    
        
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }