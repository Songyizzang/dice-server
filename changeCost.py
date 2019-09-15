import json
import sys
import logging
import pymysql


host=#비밀
username=#비밀
pw=#비밀
db=#비밀


class Product:
    def __init__(self, table, product_id, price):
        self.table = table
        self.product_id = product_id
        self.price = price




def lambda_handler(event, context):
    
    pro=Product(event['table'], event['product_id'], event['price'])

    
    conn = pymysql.connect(host=host, user=username, password=pw, db=db,charset='utf8')
    cursor = conn.cursor()

    query = "UPDATE " + pro.table + " SET " + pro.table + "_price = " + pro.price + " WHERE product_id=" + pro.product_id
    
    rst = cursor.execute(query)
    conn.commit()
    
    
    cursor.close()
    conn.close()
    
    
    return {
        'statusCode': 200,
        'body': json.dumps(rst)
    }
