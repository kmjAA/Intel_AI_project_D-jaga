import RPi.GPIO as GPIO  # Raspberry Pi GPIO 라이브러리
import time

# GPIO 핀 번호 설정
sound_pin1 = 22
sound_pin2 = 23

def setup():
    GPIO.setmode(GPIO.BCM)  # GPIO 핀 번호를 BCM 모드로 설정
    GPIO.setup(sound_pin1, GPIO.IN)  # 사운드 센서 핀을 입력으로 설정
    GPIO.setup(sound_pin2, GPIO.IN)  # 사운드 센서 핀을 입력으로 설정

def loop():
    while True:
        if GPIO.input(sound_pin1):  # 사운드 센서에서 신호를 읽어옴
            print("Sound L!")  # 소리를 감지했을 때 메시지 출력
        time.sleep(0.1)  # 0.1초 딜레이 후 다시 검사
        if GPIO.input(sound_pin2):
            print("Sound R!")
        time.sleep(0.1) 

def cleanup():
    GPIO.cleanup()  # GPIO 설정 초기화

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        cleanup()
