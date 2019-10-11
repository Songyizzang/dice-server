##### allproduct.py  
- 
  
  필요 request 없음  
  
  
  
  
##### changeSale.py
-  
  
1. request header    
  
  + request body   
  > 세일으로 변경  -> isSale == 1  
    **변수 7개 모두 타입 무관**  
      
    ① "isSale" : *1(고정값)*   
    ② "product_id" : *상품아이디*   
    ③ "saleType" : *0:정기세일  1:타임세일*
    ④ "percent" : *할인율*
    ⑤ "eventType" : *percent B1G1 B1G2*
    ⑥ "startdate" : *format( 2019-09-15 03:46:10 )*
    ⑦"enddate" : *format( 2019-09-15 03:46:10 )*
  
  > ② 비세일으로 변경 -> isSale == 0
    **변수 2개 모두 타입 무관**  
      
    ① "isSale" : *0(고정값)*   
    ② "product_id" : *상품아이디*   

  + response body
    {isSuccess :1 or 0}




##### changeCost.py
-
request header 
  {x-api-key: /* lambda 함수 changeCost api 게이트 웨이 누르면 api key 뜹니다*/}
request body 
  {"table":/*변경하고자하는 데이터가 저장된 table 명*/ ,
  "product_id":/*변경하고자하는 데이터의 primaryKey*/,
  "price":/*변경하고자하는 가격 데이터*/}