import os
import time
from datetime import datetime
from dotenv import load_dotenv
import pymysql
import psycopg2
import oracledb
import requests 

load_dotenv()

# 2. 텔레그램 알림 전송 함수
def send_telegram_alert(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {"chat_id": chat_id, "text": message}
    try:
        requests.get(url, params=params, timeout=5)
    except Exception as e:
        save_log(f"⚠️ 텔레그램 전송 실패: {e}")

# 로그를 파일에 저장하는 함수
def save_log(message):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("db_monitor_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{now}] {message}\n")

# --- DB 체크 함수들 (기존과 동일) ---
def check_mysql():
    start = time.time()
    try:
        conn = pymysql.connect(
            host=os.getenv("MYSQL_HOST"),
            port=int(os.getenv("MYSQL_PORT")),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            db=os.getenv("MYSQL_DB"),
            connect_timeout=2
        )
        conn.close()
        latency = round((time.time() - start) * 1000, 2)
        return True, latency
    except Exception as e:
        save_log(f"❌ MySQL 연결 실패: {e}")
        return False, 0

def check_postgres():
    start = time.time()
    try:
        conn = psycopg2.connect(
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
            dbname=os.getenv("PG_DB"),
            connect_timeout=2
        )
        conn.close()
        latency = round((time.time() - start) * 1000, 2)
        return True, latency
    except Exception as e:
        save_log(f"❌ PostgreSQL 연결 실패: {e}")
        return False, 0

def check_oracle():
    start = time.time()
    try:
        conn = oracledb.connect(
            user=os.getenv("ORA_USER"),
            password=os.getenv("ORA_PASSWORD"),
            dsn=os.getenv("ORA_DSN")
        )
        conn.close()
        latency = round((time.time() - start) * 1000, 2)
        return True, latency
    except Exception as e:
        save_log(f"❌ Oracle 연결 실패: {e}")
        return False, 0

def run_monitor():
    save_log("▶ 모니터링 시스템 시작")
    
    # 3. 마지막 상태를 기억하기 위한 변수 (알림 도배 방지용)
    last_status = {"MySQL": True, "PostgreSQL": True, "Oracle": True}
    
    try:
        while True:
            os.system('cls')
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"==========================================")
            print(f"   DB 통합 모니터링 시스템 ({now})")
            print(f"==========================================")
            print(f"   DB 유형      |   상태   |   응답속도(ms)")
            print(f"------------------------------------------")
            
            results = [
                ("MySQL", check_mysql()),
                ("PostgreSQL", check_postgres()),
                ("Oracle", check_oracle())
            ]

            for name, (status, latency) in results:
                status_str = "✅ 정상" if status else "❌ 에러"
                latency_str = f"{latency}ms" if status else "N/A"
                print(f"   {name.ljust(10)} |   {status_str}   |   {latency_str}")

                # 4. 상태가 정상에서 에러로 변했을 때만 텔레그램 발송
                db_key = name.strip()
                if not status and last_status[db_key]:
                    msg = f"🚨 [DB 장애 발생] {db_key} 서버에 연결할 수 없습니다!\n시간: {now}"
                    send_telegram_alert(msg)
                    last_status[db_key] = False # 에러 상태로 기록
                
                # 에러였다가 다시 정상으로 돌아오면 알림
                elif status and not last_status[db_key]:
                    msg = f"✅ [DB 복구 완료] {db_key} 서버가 다시 정상 작동합니다.\n시간: {now}"
                    send_telegram_alert(msg)
                    last_status[db_key] = True # 정상 상태로 기록

            print(f"------------------------------------------")
            print(f" ※ 종료: Ctrl + C / 로그: db_monitor_log.txt")
            time.sleep(5)
            
    except KeyboardInterrupt:
        save_log("■ 사용자에 의해 모니터링 종료")
        print("\n로그를 저장하고 프로그램을 종료합니다.")

if __name__ == "__main__":
    run_monitor()