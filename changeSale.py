import json
import sys
import logging
import pymysql
import ast 


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
    result['isSuccess'] = 0
    
    data = event.get('body')
    jdata = json.loads(data)
    jsondata = json.loads(jdata)
    
    if jsondata.get('isSale') is 1: #세일한다고 바꿀 때 
        sale = Sale(jsondata.get('product_id'), jsondata.get('saleType'), jsondata.get('percent'), jsondata.get('eventType'),jsondata.get('startdate'), jsondata.get('enddate'))
        
        query1 = "UPDATE product SET isSale = 1 WHERE product_id= " + str(sale.product_id)
        query2 = "insert into sale(sale_type,sale_percent,sale_startdate,sale_enddate,product_id,sale_eventtype) values(" + str(sale.saleType) + ", " + str(sale.percent) + ", \'" + sale.startdate + "\', \'" + sale.enddate + "\', " + str(sale.product_id) + ", \'" + sale.eventType +"\')"

        rst1 = cursor.execute(query1)
        rst2 = cursor.execute(query2)

        if rst1 is 1 and rst2 is 1:
            conn.commit()
            result['isSuccess'] = 1 
        else:
            result['isSuccess'] = 0
        
    if jsondata.get('isSale') is 0: #세일안한다고 바꿀 때 
        query2 = "UPDATE product SET isSale = 0 WHERE product_id = " + str(jsondata.get('product_id'))
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