import os
import sys
import msvcrt  # Windows 환경에서 키 입력 감지를 위한 라이브러리
from PIL import Image, ImageDraw
import adafruit_st7735
import board
import digitalio

# 특정 디렉토리에서 이미지 로드 함수
def load_images_from_directory(directory_path, display_size):
    images = {}
    for filename in os.listdir(directory_path):
        if filename.endswith(".png"):  # PNG 파일만 로드
            image_path = os.path.join(directory_path, filename)
            image_key = filename.split(".")[0]  # 파일 이름에서 확장자 제거하여 키 생성
            img = Image.open(image_path).convert("RGBA")
            background = Image.new("RGBA", display_size, (255, 255, 255, 255))
            background.paste(img, ((display_size[0] - img.width) // 2, (display_size[1] - img.height) // 2), img)
            images[image_key] = background
    return images

# 키 입력을 감지하는 함수
def get_key():
    return msvcrt.getch().decode('utf-8')

# 메인 함수
if __name__ == "__main__":
    # 디스플레이 크기 설정
    display_size = (480, 480)  # 패널 해상도에 맞게 변경

    # 이미지 디렉토리 설정
    image_directory = "images"  # 모든 이미지를 저장한 디렉토리 이름
    images = load_images_from_directory(image_directory, display_size)

    # 디스플레이 초기화
    spi = board.SPI()
    tft_cs = digitalio.DigitalInOut(board.D5)
    tft_dc = digitalio.DigitalInOut(board.D6)
    tft_rst = digitalio.DigitalInOut(board.D9)

    display = adafruit_st7735.ST7735R(spi, cs=tft_cs, dc=tft_dc, rst=tft_rst)

    # 기본 이미지 출력
    if "eye_open" in images:
        display.show(images["eye_open"])  # 기본 이미지를 'eye_open'으로 설정
    else:
        raise ValueError("기본 이미지인 'eye_open'이 디렉토리에 없습니다.")

    # 사용자 입력을 대기하면서 이미지 변경
    while True:
        key = get_key()
        if key.lower() in images:
            display.show(images[key.lower()])