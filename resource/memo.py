from http import HTTPStatus
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql.connector.errors import Error
from my_sql_connection import get_connection
import mysql.connector

### API 를 만들기 위한 클래스 작성
### class(클래스) 란??  변수와 함수로 구성된 묶음!
### 클래스는 상속이 가능하다!
### API를 만들기 위한 클래스는, flask_restful 라이브러리의
### Resource 클래스를 상속해서 만들어야 한다.

class MemoListResource(Resource):
    # restful api 의 method 에 해당하는 함수 작성
    # jwt_required = api를 호출하려면 header부분에 Authorization key값이 없으면 처리를 하지 않는다.
    @jwt_required()
    def post(self) :
        # api 실행 코드를 여기에 작성

        # 클라이언트에서, body 부분에 작성한 json 을
        # 받아오는 코드
        data = request.get_json()

        # 암호화 한 token을 다시 보이게하는 코드
        user_id = get_jwt_identity()


        # 받아온 데이터를 디비 저장하면 된다.
        try :
            # 데이터 insert 
            # 1. DB에 연결
            connection = get_connection()

            # 2. 쿼리문 만들기
            query = '''insert into memo
                    (title, todo_date, content)
                    values
                    ( %s , %s , %s );'''
            
            record = (data['title'], data['todo_date'], data['content'], user_id )

            # 3. 커서를 가져온다.
            cursor = connection.cursor()

            # 4. 쿼리문을 커서를 이용해서 실행한다.
            cursor.execute(query, record)

            # 5. 커넥션을 커밋해줘야 한다 => 디비에 영구적으로 반영하라는 뜻
            connection.commit()

            # 6. 자원 해제
            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"error" : str(e)}, 503

        return {"result" : "success"}, 200