allproduct.py
필요 request 없음






changeSale.py
request header 
  {x-api-key: /* lambda 함수 saleFunction api 게이트 웨이 누르면 api key 뜹니다*/}
request body 
① 세일한다고 바꿀 때  -> isSale == 1

{"isSale":(int)1,  
"product_id":/* String 상품아이디 */, 
"saleType":/* String 0:정기세일 1:타임세일 */, 
"percent":/* String 할인율*/,
"eventType":/* String percent B1G1 B1G2 */,
"startdate": /* Stirng format( 2019-09-15 03:46:10 )*/,
"enddate":/* Stirng format( 2019-09-15 03:46:10 )*/ }


② 세일안한다 !!! -> isSale == 0
{"isSale":(int)0,
"product_id":/* String 상품아이디 */ }

response
isSuccess :1 or 0


changeCost.py
request header 
  {x-api-key: /* lambda 함수 changeCost api 게이트 웨이 누르면 api key 뜹니다*/}
request body 
  {"table":/*변경하고자하는 데이터가 저장된 table 명*/ ,
  "product_id":/*변경하고자하는 데이터의 primaryKey*/,
  "price":/*변경하고자하는 가격 데이터*/}