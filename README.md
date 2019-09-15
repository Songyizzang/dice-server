allproduct.py
필요 request 없음


changeCost.py
request header 
  {x-api-key: /* lambda 함수 changeCost api 게이트 웨이 누르면 api key 뜹니다*/}
request body 
  {"table":/*변경하고자하는 데이터가 저장된 table 명*/ ,
  "product_id":/*변경하고자하는 데이터의 primaryKey*/,
  "price":/*변경하고자하는 가격 데이터*/}