import sys
import time
import msvcrt  # Windows 환경에서 키 입력 감지를 위한 라이브러리
from PIL import Image, ImageDraw
import adafruit_st7735
import board
import digitalio

# 키 입력을 감지하는 함수 (Windows용)
def get_key():
    return msvcrt.getch().decode('utf-8')  # 사용자가 키를 입력하면 반환

# PNG 이미지를 로드하고 흰 배경 추가
def prepare_image(image_path, display_size):
    img = Image.open(image_path).convert("RGBA")
    background = Image.new("RGBA", display_size, (255, 255, 255, 255))
    background.paste(img, ((display_size[0] - img.width) // 2, (display_size[1] - img.height) // 2), img)
    return background

# 깜빡이는 모션 추가
def blink_animation(display, eye_open_image, eye_closed_image, blink_count=5, blink_interval=0.5):
    for _ in range(blink_count):
        # 눈을 감은 상태 표시
        display.show(eye_closed_image)
        time.sleep(blink_interval)

        # 눈을 뜬 상태 표시
        display.show(eye_open_image)
        time.sleep(blink_interval)

# 메인 함수
if __name__ == "__main__":
    # 디스플레이 크기 설정
    display_size = (480, 480)

    # 이미지 준비
    eye_open_path = "eye_open.png"
    eye_closed_path = "eye_closed.png"
    happy_eye_path = "happy_eye.png"
    sad_eye_path = "sad_eye.png"
    angry_eye_path = "angry_eye.png"
    surprised_eye_path = "surprised_eye.png"
    crying_eye_path = "crying_eye.png"
    excited_eye_path = "excited_eye.png"
    awkward_eye_path = "awkward_eye.png"

    # 이미지 객체 생성
    eye_open_image = prepare_image(eye_open_path, display_size)
    eye_closed_image = prepare_image(eye_closed_path, display_size)
    happy_eye_image = prepare_image(happy_eye_path, display_size)
    sad_eye_image = prepare_image(sad_eye_path, display_size)
    angry_eye_image = prepare_image(angry_eye_path, display_size)
    surprised_eye_image = prepare_image(surprised_eye_path, display_size)
    crying_eye_image = prepare_image(crying_eye_path, display_size)
    excited_eye_image = prepare_image(excited_eye_path, display_size)
    awkward_eye_image = prepare_image(awkward_eye_path, display_size)

    # 디스플레이 초기화
    spi = board.SPI()
    tft_cs = digitalio.DigitalInOut(board.D5)
    tft_dc = digitalio.DigitalInOut(board.D6)
    tft_rst = digitalio.DigitalInOut(board.D9)

    display = adafruit_st7735.ST7735R(spi, cs=tft_cs, dc=tft_dc, rst=tft_rst)

    # 기본 이미지 출력
    display.show(eye_open_image)
    print("특정 키를 입력하면 이미지가 변경됩니다!")
    print("h: 행복한 눈, s: 슬픈 눈, a: 화난 눈, u: 놀란 눈, c: 우는 눈, e: 신난 눈, w: 머쓱한 눈")

    # 사용자 입력을 대기하면서 이미지 변경
    blinking = True  # 깜빡임 상태를 제어하는 플래그
    while True:
        if blinking:
            blink_animation(display, eye_open_image, eye_closed_image)  # 기본 깜빡임 동작

        key = get_key()
        if key.lower() == "h":
            blinking = False  # 깜빡임 중지
            display.show(happy_eye_image)
        elif key.lower() == "s":
            blinking = False
            display.show(sad_eye_image)
        elif key.lower() == "a":
            blinking = False
            display.show(angry_eye_image)
        elif key.lower() == "u":
            blinking = False
            display.show(surprised_eye_image)
        elif key.lower() == "c":
            blinking = False
            display.show(crying_eye_image)
        elif key.lower() == "e":
            blinking = False
            display.show(excited_eye_image)
        elif key.lower() == "w":
            blinking = False
            display.show(awkward_eye_image)