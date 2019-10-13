## allproduct.py   
`url https://biw4gdguia.execute-api.ap-northeast-2.amazonaws.com/default/dice-allproduct `
  
  1. READ (모든 상품 정보 읽기)  
    + 필요 request 없음

  2. CREAT (상품 정보 등록)
    + httpmethod : **POST**  
      
    +  request body
        - common 
        **변수 8개 모두 타입 무관**    
           
        >① "product_type" : *common(고정값 - 테이블 이름임)*       
        >② "common_brand" : *상품 브랜드*       
        >③ "common_category" : *상품 종류*    
        >④ "common_name" : *이름*      
        >⑤ "common_price" : *가격*    
        >⑥ "common_capacity" : *용량*    
        >⑦ "common_unit" : *용량 단위* 
        >⑧ "common_displayType" : *큰디스플레이인지 작은 디스플레이 인지*


        -  beef
         **변수 7개 모두 타입 무관**    
           
        >① "product_type" : *beef(고정값 - 테이블 이름임)*       
        >② "beef_part" : *부위*       
        >③ "beef_pricePerUnitWeight" : *단위별가격*    
        >④ "beef_origin" : *원산지*      
        >⑤ "beef_usage" : *용도*    
        >⑥ "beef_identificationNum" : *식별번호*    
        >⑦ "beef_rate" : *등급* 
           
      
        -  wine
         **변수 8개 모두 타입 무관**    
           
        >① "product_type" : *wine(고정값 - 테이블 이름임)*       
        >② "wine_brand" : *브랜드*       
        >③ "wine_name" : *이름*    
        >④ "wine_price" : *가격*      
        >⑤ "wine_capacity" : *용량*    
        >⑥ "wine_origin" : *원산지*    
        >⑦ "wine_sugarContent" : *당도* 
        >⑧ "wine_frequency" : *도수*

    +  response body
        >{isSuccess :1 or 0}

  3. UPDATE (상품 정보 수정)
    + httpmethod : **PUT**  
      
    +  request body
      * create 에서 변수 ( product_id ) 1개 씩 추가됨
        - common 
        **변수 9개 모두 타입 무관**    
        
        >ⓞ "product_id" : *상품 id(기본키)*
        >① "product_type" : *common(고정값 - 테이블 이름임)*       
        >② "common_brand" : *상품 브랜드*       
        >③ "common_category" : *상품 종류*    
        >④ "common_name" : *이름*      
        >⑤ "common_price" : *가격*    
        >⑥ "common_capacity" : *용량*    
        >⑦ "common_unit" : *용량 단위* 
        >⑧ "common_displayType" : *큰디스플레이인지 작은 디스플레이 인지*


        -  beef
         **변수 8개 모두 타입 무관**    

        >ⓞ "product_id" : *상품 id(기본키)*
        >① "product_type" : *beef(고정값 - 테이블 이름임)*       
        >② "beef_part" : *부위*       
        >③ "beef_pricePerUnitWeight" : *단위별가격*    
        >④ "beef_origin" : *원산지*      
        >⑤ "beef_usage" : *용도*    
        >⑥ "beef_identificationNum" : *식별번호*    
        >⑦ "beef_rate" : *등급* 
           
      
        -  wine
         **변수 8개 모두 타입 무관**    
           
        >ⓞ "product_id" : *상품 id(기본키)*
        >① "product_type" : *wine(고정값 - 테이블 이름임)*       
        >② "wine_brand" : *브랜드*       
        >③ "wine_name" : *이름*    
        >④ "wine_price" : *가격*      
        >⑤ "wine_capacity" : *용량*    
        >⑥ "wine_origin" : *원산지*    
        >⑦ "wine_sugarContent" : *당도* 
        >⑧ "wine_frequency" : *도수*

    +  response body
        >{isSuccess :1 or 0}
ㄴ
      
  
  
## changeSale.py  
`url https://43nmzzrgt9.execute-api.ap-northeast-2.amazonaws.com/default/saleFunction`

1. request header    
  
    + request body     
      세일으로 변경  -> isSale == 1    
      **변수 7개 모두 타입 무관**    
          
        >① "isSale" : *1(고정값)*       
        >② "product_id" : *상품아이디*       
        >③ "saleType" : *0:정기세일  1:타임세일*    
        >④ "percent" : *할인율*      
        >⑤ "eventType" : *percent B1G1 B1G2*    
        > ⑥ "startdate" : *format( 2019-09-15 03:46:10 )*    
        >⑦"enddate" : *format( 2019-09-15 03:46:10 )* `    
            
    
      비세일으로 변경 -> isSale == 0    
      **변수 2개 모두 타입 무관**  
        
        >① "isSale" : *0(고정값)*     
        >② "product_id" : *상품아이디*     
  
    + response body  
      >{isSuccess :1 or 0}  
  
  
  
  







  
## changeCost.py

request header 
  {x-api-key: /* lambda 함수 changeCost api 게이트 웨이 누르면 api key 뜹니다*/}
request body 
  {"table":/*변경하고자하는 데이터가 저장된 table 명*/ ,
  "product_id":/*변경하고자하는 데이터의 primaryKey*/,
  "price":/*변경하고자하는 가격 데이터*/}