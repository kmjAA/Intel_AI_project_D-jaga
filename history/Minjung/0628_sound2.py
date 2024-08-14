import serial
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

# 시리얼 포트 설정 (라즈베리 파이에서 확인한 포트에 맞춰 변경)
ser = serial.Serial('/dev/ttyACM0', 9600)  # 시리얼 포트 및 보드레이트 설정

# FFT 관련 설정
N = 256  # FFT 크기
fs = 1000  # 샘플링 주파수 (아두이노 측정 주기에 맞춰 설정)

data1 = np.zeros(N)
data2 = np.zeros(N)

plt.ion()  # 대화형 모드 설정
fig, (ax1, ax2) = plt.subplots(2, 1)

line1, = ax1.plot([], [])
line2, = ax2.plot([], [])
ax1.set_xlim(0, fs/2)
ax2.set_xlim(0, fs/2)
ax1.set_ylim(0, 1000)  # 임의의 초기 값 설정
ax2.set_ylim(0, 1000)  # 임의의 초기 값 설정
ax1.set_xlabel('Frequency (Hz)')
ax1.set_ylabel('Amplitude')
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Amplitude')
ax1.set_title('Frequency Spectrum 1')
ax2.set_title('Frequency Spectrum 2')
ax1.grid(True)
ax2.grid(True)

plt.tight_layout()

try:
    while True:
        # 아두이노에서 데이터 읽기
        line = ser.readline()
        try:
            line = line.decode('ascii').strip()
        except UnicodeDecodeError:
            print(f"Error decoding line: {line}")
            continue
        
        if line:
            try:
                values = list(map(int, line.split(',')))
                if len(values) == 2:  # 데이터가 두 개의 유효한 값으로 구성되어 있는지 확인
                    sensorValue1 = values[0]
                    sensorValue2 = values[1]
                    
                    # 데이터 업데이트 (순환 버퍼처럼 동작)
                    data1[:-1] = data1[1:]
                    data1[-1] = sensorValue1
                    data2[:-1] = data2[1:]
                    data2[-1] = sensorValue2
                    
                    # FFT 계산
                    spectrum1 = np.abs(fft(data1, N))
                    spectrum2 = np.abs(fft(data2, N))
                    
                    # 주파수 범위 계산
                    freq = np.fft.fftfreq(N, 1/fs)
                    
                    # 플롯 업데이트
                    line1.set_xdata(freq[:N//2])
                    line1.set_ydata(spectrum1[:N//2])
                    line2.set_xdata(freq[:N//2])
                    line2.set_ydata(spectrum2[:N//2])
                    
                    ax1.relim()
                    ax1.autoscale_view()
                    ax2.relim()
                    ax2.autoscale_view()
                    
                    fig.canvas.draw()
                    fig.canvas.flush_events()
            
            except ValueError as e:
                print("Error parsing data:", e)
                continue  # 데이터 파싱 오류가 발생하면 다음 루프로 넘어감
        
        else:
            print("Empty line received")

except KeyboardInterrupt:
    print("Program terminated by user")
finally:
    ser.close()  # 시리얼 포트 닫기
    plt.ioff()   # 대화형 모드 비활성화
    plt.close()  # 플롯 창 닫기
