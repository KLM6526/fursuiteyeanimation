import pygame
from PIL import Image
import random

class EyeDisplay:
    def __init__(self, resolution=(480, 480)):
        pygame.init()
        self.screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption("감정 표현 및 깜빡임 테스트")
        self.resolution = resolution

        # 이미지 경로 (감정별 이미지)
        self.image_paths = {
            "neutral": "C:\\Users\\eric2\\Documents\\stoneprj\\images\\eye_open.png",
            "happy": "C:\\Users\\eric2\\Documents\\stoneprj\\images\\eye_happy.png",
            "sad": "C:\\Users\\eric2\\Documents\\stoneprj\\images\\eye_sad.png",
            "angry": "C:\\Users\\eric2\\Documents\\stoneprj\\images\\eye_angry.png",
            "surprised": "C:\\Users\\eric2\\Documents\\stoneprj\\images\\eye_surprised.png",
            "fear": "C:\\Users\\eric2\\Documents\\stoneprj\\images\\eye_fear.png",
            "embarrassed": "C:\\Users\\eric2\\Documents\\stoneprj\\images\\eye_embarrassed.png",
            "sleepy": "C:\\Users\\eric2\\Documents\\stoneprj\\images\\eye_sleepy.png",
            "affection": "C:\\Users\\eric2\\Documents\\stoneprj\\images\\eye_affection.png",
            "closed": "C:\\Users\\eric2\\Documents\\stoneprj\\images\\eye_closed.png"  # 눈 감은 상태 이미지
        }
        self.images = {emotion: self.load_image(path) for emotion, path in self.image_paths.items()}
        if any(img is None for img in self.images.values()):
            print("Failed to load one or more images.")
            pygame.quit()
            return

        # 현재 감정 상태
        self.current_emotion = "neutral"
        self.next_emotion = None  # 변경될 감정 상태 저장
        self.running = True
        self.blink_counter = 0

    def load_image(self, filepath):
        try:
            img = Image.open(filepath)
            surface = pygame.image.fromstring(img.tobytes(), img.size, img.mode)
            return surface
        except FileNotFoundError:
            print(f"File not found: {filepath}")
            return None

    def blink_animation(self, blink_duration=100):
        """
        눈 감기 애니메이션 후 지정된 감정으로 변경
        """
        # 눈 감기 상태
        self.screen.blit(self.images["closed"], (0, 0))
        pygame.display.update()
        pygame.time.wait(blink_duration)  # 눈을 감고 있는 시간

        # 감정 변경 (키보드 입력으로 받은 값)
        if self.next_emotion:
            self.current_emotion = self.next_emotion
            self.next_emotion = None  # 다음 감정 상태 초기화

        # 변경된 감정 출력
        self.screen.blit(self.images[self.current_emotion], (0, 0))
        pygame.display.update()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    # 감정 변경을 위한 키 입력
                    if event.key == pygame.K_n:
                        self.next_emotion = "neutral"
                    elif event.key == pygame.K_h:
                        self.next_emotion = "happy"
                    elif event.key == pygame.K_s:
                        self.next_emotion = "sad"
                    elif event.key == pygame.K_a:
                        self.next_emotion = "angry"
                    elif event.key == pygame.K_u:
                        self.next_emotion = "surprised"
                    elif event.key == pygame.K_f:
                        self.next_emotion = "fear"
                    elif event.key == pygame.K_e:
                        self.next_emotion = "embarrassed"
                    elif event.key == pygame.K_l:
                        self.next_emotion = "sleepy"
                    elif event.key == pygame.K_x:
                        self.next_emotion = "affection"

                    # 깜빡임 후 감정 변경
                    self.blink_animation()

            # 배경 초기화
            self.screen.fill((0, 0, 0))

            # 현재 감정 렌더링
            self.screen.blit(self.images[self.current_emotion], (0, 0))
            pygame.display.update()

            # 기본 표정일 경우 깜빡임 발생 (자동 깜빡임 유지)
            if self.current_emotion == "neutral":
                self.blink_counter += 1
                if self.blink_counter >= random.randint(180, 360):  # 약 3~6초
                    self.blink_animation()
                    self.blink_counter = 0

            # 약간의 대기 (프레임 속도 조절)
            pygame.time.wait(16)

        pygame.quit()

if __name__ == "__main__":
    display = EyeDisplay()
    display.run()