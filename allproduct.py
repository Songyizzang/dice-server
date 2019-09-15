import sys
import logging
import pymysql
import json


host=#비밀
username=#비밀
pw=#비밀
db=#비밀


def lambda_handler(event, context):

    #db 연결
    conn = pymysql.connect(host=host, user=username, password=pw, db=db,charset='utf8')
    curs = conn.cursor()
    
    
    result = dict()
    
    
    #common 
    query = "SELECT product.product_id,isSale,common_brand,common_name,common_price,common_capacity,common_unit,common_displayType,common_category FROM product JOIN common ON product.product_id = common.product_id;"
    key = "common"
    curs.execute(query)

    result[key]=[]

    while True:
        row = curs.fetchone()
        if not row:
            break

        tmp = dict()
        tmp['product_id'] = row[0]
        #tmp['isSale'] = row[1]
        tmp['common_brand'] = row[2]
        tmp['common_name'] = row[3]
        tmp['common_price'] = row[4]
        tmp['common_capacity'] = row[5]
        tmp['common_unit'] = row[6]
        tmp['common_displayType'] = row[7]
        tmp['common_category'] = row[8]
        
        if  row[1] is 1:
            query = "select sale_type,sale_eventtype,sale_percent,sale_startdate,sale_enddate FROM sale WHERE product_id="+ str(tmp['product_id'])
            curs.execute(query)
            row = curs.fetchone()
            t = dict()
            t['sale_type'] = row[0]
            t['sale_eventtype'] = row[1]
            t['sale_percent'] = row[2]
            t['sale_startdate'] = str(row[3])
            t['sale_enddate'] = str(row[4])
        
        tmp['sale_info'] = t
           
        
        
        
        result[key].append(tmp)   




    #beef 
    query = "SELECT product.product_id,isSale,beef_part,beef_pricePerUnitWeight,beef_origin,beef_usage,beef_identificationNum,beef_rate FROM product,beef WHERE product.product_id = beef.product_id"
    key = "beef"
    curs.execute(query)

    result[key]=[]

    while True:
        row = curs.fetchone()
        if not row:
            break

        tmp = dict()
        tmp['product_id'] = row[0]
        tmp['isSale'] = row[1]
        tmp['beef_part'] = row[2]
        tmp['beef_pricePerUnitWeight'] = row[3]
        tmp['beef_origin'] = row[4]
        tmp['beef_usage'] = row[5]
        tmp['beef_identificationNum'] = row[6]
        tmp['beef_rate'] = row[7]
        
        result[key].append(tmp) 
        
        
        
        
    #wine
    query = "SELECT product.product_id,isSale,wine_brand,wine_name,wine_price,wine_capacity,wine_origin,wine_sugarContent,wine_frequency FROM product,wine WHERE product.product_id = wine.product_id;"
    key = "wine"
    curs.execute(query)

    result[key]=[]

    while True:
        row = curs.fetchone()
        if not row:
            break

        tmp = dict()
        tmp['product_id'] = row[0]
        tmp['isSale'] = row[1]
        tmp['wine_brand'] = row[2]
        tmp['wine_name'] = row[3]
        tmp['wine_price'] = row[4]
        tmp['wine_capacity'] = row[5]
        tmp['wine_origin'] = row[6]
        tmp['wine_sugarContent'] = row[7]
        tmp['wine_frequency'] = row[8]
        
        result[key].append(tmp) 

    conn.close()

    return {
        'statusCode':200,
        'body':json.dumps(result,ensure_ascii=False)
    }