import os
from dotenv import load_dotenv
import pymysql
import psycopg2
import cx_Oracle

# .env 파일 로드
load_dotenv()

def test_connections():
    print("--- DB 연결 테스트 시작 ---")

    # 1. MySQL 테스트
    try:
        conn = pymysql.connect(
            host=os.getenv("MYSQL_HOST"),
            port=int(os.getenv("MYSQL_PORT")),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            db=os.getenv("MYSQL_DB")
        )
        print("✅ MySQL: 연결 성공!")
        conn.close()
    except Exception as e:
        print(f"❌ MySQL: 연결 실패 ({e})")

    # 2. PostgreSQL 테스트
    try:
        conn = psycopg2.connect(
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
            dbname=os.getenv("PG_DB")
        )
        print("✅ PostgreSQL: 연결 성공!")
        conn.close()
    except Exception as e:
        print(f"❌ PostgreSQL: 연결 실패 ({e})")

    # 3. Oracle 테스트
    try:
        conn = cx_Oracle.connect(
            user=os.getenv("ORA_USER"),
            password=os.getenv("ORA_PASSWORD"),
            dsn=os.getenv("ORA_DSN")
        )
        print("✅ Oracle: 연결 성공!")
        conn.close()
    except Exception as e:
        print(f"❌ Oracle: 연결 실패 ({e})")

    print("---------------------------")

if __name__ == "__main__":
    test_connections()