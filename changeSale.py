import json
import sys
import logging
import pymysql


host=
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
    rst = 0
    result = dict()

    if event['isSale'] is 1: #세일한다고 바꿀 때 
        sale = Sale(event['product_id'], event['saleType'], event['percent'], event['eventType'],event['startdate'], event['enddate'])
        query1 = "UPDATE product SET isSale = 1 WHERE product_id= " + sale.product_id
        query2 = "insert into sale(sale_type,sale_percent,sale_startdate,sale_enddate,product_id,sale_eventtype) values(" + sale.saleType + ", " + sale.percent + ", \'" + sale.startdate + "\', \'" + sale.enddate + "\', " + sale.product_id + ", \'" + sale.eventType +"\')"

        rst1 = cursor.execute(query1)
        rst2 = cursor.execute(query2)

        if rst1 is 1 and rst2 is 1:
            conn.commit()
            result['isSuccess'] = 1 
        else:
            result['isSuccess'] = 0
            
    
    if event['isSale'] is 0: #세일안한다고 바꿀 때 
        query2 = "UPDATE product SET isSale = 0 WHERE product_id= " + event['product_id']
        rst = cursor.execute(query2)
        
        if rst is 1:
            conn.commit()
            result['isSuccess'] = 1 
        
        else:
            result['isSuccess'] = 0
    
    cursor.close()
    conn.close()
    
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }