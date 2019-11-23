import math
import boto3
import sys
import logging
import pymysql
import json
from urllib.parse import urlsplit, parse_qsl

host="dicerds.cn7oixdffz0i.ap-northeast-2.rds.amazonaws.com"
username="root"
pw="root1234"
db="dicedb"


def lambda_handler(event, context):
    
    #db 연결
    conn = pymysql.connect(host=host, user=username, password=pw, db=db,charset='utf8')
    curs = conn.cursor()
    result = dict()
    
    
    httpmethod = event.get('httpMethod')

    if httpmethod == "GET":
        
        query = "SELECT product.product_id,isSale,common_brand,common_name,common_price,common_capacity,common_unit,common_displayType,common_category FROM product JOIN common ON product.product_id = common.product_id;"
        key = "common"
        curs.execute(query)
    
        result[key]=[]

        common = curs.fetchall()
        for col in common:
            tmp = dict()
            tmp['product_id'] = col[0]
            tmp['isSale'] = col[1]
            tmp['common_brand'] = col[2]
            tmp['common_name'] = col[3]
            tmp['common_price'] = col[4]
            tmp['common_capacity'] = col[5]
            tmp['common_unit'] = col[6]
            tmp['common_displayType'] = col[7]
            tmp['common_category'] = col[8]

            if  tmp['isSale'] is 1:
                query = "select sale_type,sale_eventtype,sale_percent,sale_startdate,sale_enddate FROM sale WHERE product_id="+ str(tmp['product_id']) + " ORDER BY sale_id DESC limit 1"
                curs.execute(query)
                row2 = curs.fetchone()
                t = dict()
                t['sale_type'] = row2[0]
                t['sale_eventtype'] = row2[1]
                t['sale_percent'] = row2[2]
                t['sale_startdate'] = str(row2[3])
                t['sale_enddate'] = str(row2[4])
                tmp['sale_info'] = t
            
            result[key].append(tmp)
            
        
        
        #beef 
        query = "SELECT product.product_id,isSale,beef_part,beef_pricePerUnitWeight,beef_origin,beef_usage,beef_identificationNum,beef_rate FROM product,beef WHERE product.product_id = beef.product_id"
        key = "beef"
        curs.execute(query)

        result[key]=[]



        beef = curs.fetchall()
        for col in beef:
            tmp = dict()
            tmp['product_id'] = col[0]
            tmp['isSale'] = col[1]
            tmp['beef_part'] = col[2]
            tmp['beef_pricePerUnitWeight'] = col[3]
            tmp['beef_origin'] = col[4]
            tmp['beef_usage'] = col[5]
            tmp['beef_identificationNum'] = col[6]
            tmp['beef_rate'] = col[7]

            if  tmp['isSale'] is 1:
                query = "select sale_type,sale_eventtype,sale_percent,sale_startdate,sale_enddate FROM sale WHERE product_id="+ str(tmp['product_id']) + " ORDER BY sale_id DESC limit 1"
                curs.execute(query)
                row2 = curs.fetchone()
                t = dict()
                t['sale_type'] = row2[0]
                t['sale_eventtype'] = row2[1]
                t['sale_percent'] = row2[2]
                t['sale_startdate'] = str(row2[3])
                t['sale_enddate'] = str(row2[4])
                tmp['sale_info'] = t
            
            result[key].append(tmp) 
   
        
        #wine
        query = "SELECT product.product_id,isSale,wine_brand,wine_name,wine_price,wine_capacity,wine_origin,wine_sugarContent,wine_frequency FROM product,wine WHERE product.product_id = wine.product_id;"
        key = "wine"
        curs.execute(query)

        result[key]=[]

        wine = curs.fetchall()
        for col in wine:
            tmp = dict()
            tmp['product_id'] = col[0]
            tmp['isSale'] = col[1]
            tmp['wine_brand'] = col[2]
            tmp['wine_name'] = col[3]
            tmp['wine_price'] = col[4]
            tmp['wine_capacity'] = col[5]
            tmp['wine_origin'] = col[6]
            tmp['wine_sugarContent'] = col[7]
            tmp['wine_frequency'] = col[8]

            if  tmp['isSale'] is 1:
                query = "select sale_type,sale_eventtype,sale_percent,sale_startdate,sale_enddate FROM sale WHERE product_id="+ str(tmp['product_id']) + " ORDER BY sale_id DESC limit 1"
                curs.execute(query)
                row2 = curs.fetchone()
                t = dict()
                t['sale_type'] = row2[0]
                t['sale_eventtype'] = row2[1]
                t['sale_percent'] = row2[2]
                t['sale_startdate'] = str(row2[3])
                t['sale_enddate'] = str(row2[4])
                tmp['sale_info'] = t
            
            result[key].append(tmp)    
        
    
    elif httpmethod == "POST":
        data = event.get('body')
        param = dict(parse_qsl(urlsplit(data).path))
        product_type = param.get('product_type')

        
        rst1 = 0
        query1 = "insert into product(isSale, product_type) values(0, \'" + product_type + "\')"
        rst1 = curs.execute(query1)
        if product_type == 'common':
            query2 = "insert into common(product_id, common_brand, common_name, common_price, common_capacity, common_unit, common_displayType, common_category) "
            query2 += "values(LAST_INSERT_ID(), " 
            query2 += "\'" + param['common_brand'] + "\', "
            query2 += "\'" + param['common_name'] + "\', " 
            query2 += param['common_price'] + ", " 
            query2 += param['common_capacity'] + ", " 
            query2 += "\'" + param['common_unit'] + "\', " 
            query2 += "\'" + param['common_displayType'] + "\', " 
            query2 += "\'" + param['common_category'] + "\')"    
        
        elif product_type == 'beef':
            query2 = "insert into beef(product_id, beef_part, beef_pricePerUnitWeight, beef_origin, beef_usage, beef_identificationNum, beef_rate) "
            query2 += "values(LAST_INSERT_ID(), " 
            query2 += "\'" + param['beef_part'] + "\', " 
            query2 += param['beef_pricePerUnitWeight'] + ", " 
            query2 += "\'" + param['beef_origin'] + "\', " 
            query2 += "\'" + param['beef_usage'] + "\', " 
            query2 += param['beef_identificationNum'] + ", " 
            query2 += "\'" + param['beef_rate'] + "\')"
            
        elif product_type == 'wine':
            query2 = "insert into wine(product_id, wine_brand, wine_name, wine_price, wine_capacity, wine_origin, wine_sugarContent, wine_frequency) "
            query2 += "values(LAST_INSERT_ID(), " 
            query2 += "\'" + param['wine_brand'] + "\', " 
            query2 += "\'" + param['wine_name'] + "\', " 
            query2 += param['wine_price'] + ", " 
            query2 += param['wine_capacity'] + ", " 
            query2 += "\'" + param['wine_origin'] + "\', " 
            query2 += param['wine_sugarContent'] + ", " 
            query2 += param['wine_frequency'] + ")"    
        rst2 = 0
        rst2 = curs.execute(query2)

        if rst1 == 1 and rst2 == 1:
            result['isSuccess'] = 1
            conn.commit()
                
        else:
            result['isSuccess'] = 0

        
            
    elif httpmethod == "PUT":
        data = event.get('body')
        param = dict(parse_qsl(urlsplit(data).path))
        product_type = param.get('product_type')
        dic = dict()
        
        if product_type == 'common':
            query = "UPDATE common SET "
            query += "common_brand = \'" + param['common_brand'] + "\', "
            query += "common_name = \'" + param['common_name'] + "\', " 
            query += "common_price = " + param['common_price'] + ", " 
            query += "common_capacity = " + param['common_capacity'] + ", " 
            query += "common_unit = \'" + param['common_unit'] + "\', " 
            query += "common_displayType = \'" + param['common_displayType'] + "\', " 
            query += "common_category = \'" + param['common_category'] + "\' "    
            query += "where product_id=" + param['product_id']
            

        elif product_type == 'beef':
            query = "UPDATE beef SET "
            query += "beef_part = \'" + param['beef_part'] + "\', "  
            query += "beef_pricePerUnitWeight = " + param['beef_pricePerUnitWeight'] + ", " 
            query += "beef_origin = \'" + param['beef_origin'] + "\', " 
            query += "beef_usage= \'" + param['beef_usage'] + "\', " 
            query += "beef_identificationNum = " + param['beef_identificationNum'] + ", " 
            query += "beef_rate = \'" + param['beef_rate'] + "\' "
            query += "where product_id=" + param['product_id']
            
            
            dic['p'] = param['beef_part']
            dic['w'] = param['beef_pricePerUnitWeight']
            dic['o'] = param['beef_origin']
            dic['s'] = param['beef_usage']
            dic['i'] = param['beef_identificationNum']
            dic['r'] = param['beef_rate']
            
            
            
        elif product_type == 'wine':
            query = "UPDATE wine SET "
            query += "wine_brand = \'" + param['wine_brand'] + "\', " 
            query += "wine_name = \'" + param['wine_name'] + "\', " 
            query += "wine_price = " + param['wine_price'] + ", " 
            query += "wine_capacity = " + param['wine_capacity'] + ", " 
            query += "wine_origin = \'" + param['wine_origin'] + "\', " 
            query += "wine_sugarContent = " + param['wine_sugarContent'] + ", " 
            query += "wine_frequency  = " + param['wine_frequency'] + " "  
            query += "where product_id=" + param['product_id']
            
            
            
        
        
        rst = 0
        rst = curs.execute(query)
        
        if rst == 1:
            result['isSuccess'] = 1
            
            conn.commit()
            #mqtt
            display_query = "SELECT display_id from display where product_id = " + param['product_id']
            curs.execute(display_query)
            r = curs.fetchone()
            if r is not None:
                display_id = r[0]
            
            
            
                if product_type == 'common':
                    dic['bnc'] = "[" + param['common_brand'] + "] " + param['common_name'] + " " + param['common_capacity'] + param['common_unit']
                    dic['price'] = param['common_price']
                    dic['ca'] = param['common_capacity']
                    
                    if int(param['common_capacity']) < 100:
                        tmp_unit = int(param['common_price']) / int(param['common_capacity']) * 10
                        dic['unit'] = "10" + param['common_unit'] + " / "+ str(int(tmp_unit))

                    else:
                        tmp_unit = int(param['common_price']) / int(param['common_capacity']) * 100
                        dic['unit'] = "100" + param['common_unit'] + " / "+ str(int(tmp_unit))
                    
                

            
                client = boto3.client('iot-data', region_name='ap-northeast-2')
        
                response = client.publish(
                    topic = "no" + str(display_id),
                    qos=1,
                    payload=json.dumps(dic,ensure_ascii=False)
                )
            
            
            
        else:
            result['isSuccess'] = 0
            
            

        
        
    
    curs.close()
    conn.close()

    return {
        'statusCode':200,
        'body':json.dumps(result,ensure_ascii=False)
    }

    