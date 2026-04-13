# 🚀 Multi-DB Monitoring System with Telegram Alert

다중 데이터베이스(Oracle, PostgreSQL)의 상태를 실시간으로 감시하고, 장애 발생 시 텔레그램으로 즉각 알림을 보내는 모니터링 시스템입니다. DBA 업무 자동화 및 장애 대응 속도 향상을 목적으로 제작되었습니다.

## 🛠 주요 기능
- **Multi-DB Support**: Oracle(`cx_Oracle`, `oracledb`) 및 PostgreSQL(`psycopg2`) 동시 모니터링.
- **Real-time Alert**: DB 다운 시 텔레그램 봇 API를 통한 실시간 장애 알림.
- **Log Management**: 모니터링 결과 및 에러 내역을 `db_monitor_log.txt`에 기록.
- **Security**: `.env` 파일을 활용한 DB 접속 정보 및 API 토큰 보안 관리.

## 💻 핵심 코드 (Core Logic)
`monitoring.py`에서 수행되는 데이터베이스 연결 확인 로직입니다.

```python
def check_db_connection(db_config, db_type):
    try:
        if db_type == 'oracle':
            conn = db_manager.get_oracle_connection(db_config)
        elif db_type == 'postgres':
            conn = db_manager.get_postgres_connection(db_config)
        
        if conn:
            conn.close()
            return True
    except Exception as e:
        # 장애 발생 시 텔레그램 전송 로직 호출
        send_telegram_message(f"⚠️ [장애발생] {db_type.upper()} 서버 확인 필요\n에러: {e}")
        return False
