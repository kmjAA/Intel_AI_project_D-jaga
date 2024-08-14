import serial
import matplotlib.pyplot as plt

# 시리얼 포트 설정 (아두이노와 연결된 포트에 맞게 수정)
ser = serial.Serial('/dev/ttyACM0', 9600)  

try:
    while True:
        if ser.in_waiting > 0:  # 시리얼 버퍼에 읽을 데이터가 있는 확인
            data = ser.readline().decode('utf-8').rstrip()  # 시리얼에서 한 줄을 읽고, 문자열로 변환
            print(" ", data) # 읽은 데이터를 출력
            plt.ion()
            
            
except KeyboardInterrupt:
    print("Interrupted") # 중단 메세지 출력
    
finally:
    ser.close()
