# 🚀 Multi-DB Monitoring & Alert System

본 프로젝트는 DBA의 일상적인 운영 업무 자동화를 위해 설계된 **실시간 다중 데이터베이스 모니터링 시스템**입니다. Oracle, MySQL, PostgreSQL의 가용성을 동시에 감시하며, 장애 발생 및 복구 시 텔레그램을 통해 즉각적인 알림을 제공합니다.

## 🛠 주요 기능 및 기술적 특징
- **Multi-Vendor Support**: `oracledb`, `pymysql`, `psycopg2`를 활용한 이기종 DB 통합 관리.
- **Smart Alerting**: 이전 상태(`last_status`)를 추적하여 상태 변화(정상↔장애) 시점에만 알림을 발송 (알림 도배 방지 로직).
- **Latency Measurement**: 각 DB 연결 응답 속도(ms)를 측정하여 지연 상태까지 감시.
- **Auto Logging**: 모든 장애 내역 및 복구 이력을 `db_monitor_log.txt`에 타임스탬프와 함께 실시간 기록.
- **Security**: `.env` 환경 변수를 활용하여 DB 접속 정보 및 API 토큰 등 민감 정보 보안 강화.

## 💻 핵심 코드 (Core Logic)

### 1. 스마트 알림 로직
단순 반복 알림이 아닌, 상태가 변하는 시점에만 운영자에게 알림을 보냅니다.

```python
# 상태가 정상(True)에서 에러(False)로 변했을 때만 텔레그램 발송
if not status and last_status[db_key]:
    msg = f"🚨 [DB 장애 발생] {db_key} 서버 연결 실패!\n시간: {now}"
    send_telegram_alert(msg)
    last_status[db_key] = False  # 에러 상태로 기록

# 에러였다가 다시 정상으로 돌아오면 복구 알림
elif status and not last_status[db_key]:
    msg = f"✅ [DB 복구 완료] {db_key} 서버 정상화\n시간: {now}"
    send_telegram_alert(msg)
    last_status[db_key] = True  # 정상 상태로 기록
    except Exception as e:
        # 장애 발생 시 텔레그램 전송 로직 호출
        send_telegram_message(f"⚠️ [장애발생] {db_type.upper()} 서버 확인 필요\n에러: {e}")
        return False

```

![image alt](https://github.com/hyunholee9204/DB_Monitoring_System/blob/fce04c5f2877846e5333dff8f03a211d82b21dcf/telegram.jpg)

---

### 2. 가용성 체크 및 지연 시간 측정

```python
def check_mysql():
    start = time.time()
    try:
        conn = pymysql.connect(..., connect_timeout=2)
        conn.close()
        latency = round((time.time() - start) * 1000, 2) # 응답 속도(ms) 계산
        return True, latency
    except Exception as e:
        save_log(f"❌ MySQL 연결 실패: {e}")
        return False, 0
```
---

### 3. 로그 기록 및 장애 이력 관리
모든 이벤트는 타임스탬프와 함께 파일로 기록되어, 사후 장애 분석(Post-mortem) 자료로 활용할 수 있습니다.

```python
def save_log(message):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("db_monitor_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{now}] {message}\n")
```
---
