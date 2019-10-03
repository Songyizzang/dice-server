import sys
import logging
import pymysql
import json


host=
username=
pw=
db=


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


    

    
    curs.close()
    conn.close()

    return {
        'statusCode':200,
        'body':json.dumps(result,ensure_ascii=False)
    }