## 페이히어 과제 

## 디렉토리 구조

```├── app
│   ├── api
│   │   ├── common  ## 공통 모듈
│   │   │   └── dto
│   │   │       └── base_response_dto.py
│   │   ├── dependency.py
│   │   └── v1  # API V1
│   │       ├── endpoint.py
│   │       ├── product
│   │       │   ├── dto
│   │       │   │   ├── product_base.py
│   │       │   │   ├── request_update_user_product.py
│   │       │   │   ├── request_user_product.py
│   │       │   │   └── response_user_product_list.py
│   │       │   ├── endpoint.py 
│   │       │   ├── entity
│   │       │   │   └── product.py
│   │       │   └── service.py
│   │       └── user
│   │           ├── dto
│   │           │   ├── request_user_profile_dto.py
│   │           │   ├── request_user_remove_data.py
│   │           │   ├── request_user_sign.py
│   │           │   ├── request_user_sign_dto.py
│   │           │   └── request_user_sign_out_dto.py
│   │           ├── endpoint.py
│   │           ├── entity
│   │           │   └── user.py
│   │           ├── service.py
│   │           └── utils.py
│   ├── config
│   │   ├── config.py
│   │   ├── db
│   │   │   ├── database.py
│   │   │   └── time_stamp_mixin.py
│   │   └── redis_config.py
│   ├── main.py
│   └── models
├── db_script
│   ├── product.sql
│   └── user.sql
├── docker-compose.yml
├── env
│   └── local.env
├── requirement.txt
└── tests
    ├── api
    │   ├── test_product.py
    │   └── test_user.py
    └── conftest.py
```
## User API 
User Entity를 보면 핸드폰 번호를 char(11)가 아닌  varchar(255) 으로 한 이유는 개인 정보 보호법상 
암호롸를 해야하기 때문에 varchar(255)를 해놨는데 구현하지 않은 이유는 따로 명시를 하지 않았기때문에 구현하지 않았습니다.
<tr>
기본적인 로그인 로그아웃 구조는 access_token 과 refresh_token을 사용하였습니다.


## Product
Path Parameter로 user_id를 받아서 해당 유저의 상품을 조회하고 수정할 수 있습니다.
<tr>
다만 등록된 해당 Product ID의 user_id가 요청한 user_id와 다를 경우 400 에러를 반환합니다.

초성 키워드 검색은 like 형식이 아닌 full text search를 사용하였습니다.
<tr>
user_id를 index로 해놓고 like 형식으로 해도 괜찮지만 확장성을 고려해(카카오지하철의 역들 이름처럼) <tr>
full text search를 사용하였습니다.

