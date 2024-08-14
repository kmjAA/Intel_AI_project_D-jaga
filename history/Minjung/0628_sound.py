import serial
import matplotlib.pyplot as plt
from collections import deque

# 시리얼 포트 설정 (아두이노와 연결된 포트에 맞게 수정)
ser = serial.Serial('/dev/ttyACM0', 9600)

# 그래프 초기 설정
plt.ion()  # 대화형 모드 설정
fig, ax = plt.subplots()
ax.set_xlabel('Time')
ax.set_ylabel('Sensor Value')
ax.set_title('Real-time Sensor Data')
plt.show()

# 데이터 저장을 위한 deque 설정 (최근 데이터 N개 저장)
N = 100
times = deque(maxlen=N)
values = deque(maxlen=N)

try:
    while True:
        if ser.in_waiting > 0:  # 시리얼 버퍼에 읽을 데이터가 있는지 확인
            data = ser.readline().decode('utf-8').rstrip()  # 시리얼에서 한 줄을 읽고, 문자열로 변환
            print("Received:", data)  # 읽은 데이터를 출력
            
            # 데이터 파싱
            try:
                time, value = map(float, data.split(','))
                times.append(time)
                values.append(value)
                
                # 그래프 업데이트
                ax.clear()
                ax.plot(times, values, marker='o', linestyle='-')
                ax.set_xlabel('Time')
                ax.set_ylabel('Sensor Value')
                ax.set_title('Real-time Sensor Data')
                ax.grid(True)
                fig.canvas.draw()
                fig.canvas.flush_events()
                
            except ValueError as e:
                print(f"Error parsing data: {e}")
                continue
        
except KeyboardInterrupt:
    print("Interrupted")  # 사용자에 의한 중단 메시지 출력

finally:
    ser.close()  # 시리얼 포트 닫기
