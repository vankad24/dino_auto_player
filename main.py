import cv2
import mss.tools
import pyautogui
import numpy as np
import matplotlib.pyplot as plt
import time

# делает задержку меньше
pyautogui.PAUSE = .01
# мышку в левый верхний угол, чтобы остановить программу
pyautogui.FAILSAFE = True

def get_fullscreen():
    with mss.mss() as sct:
        sct_img = sct.grab(sct.monitors[0])
        img = np.frombuffer(sct_img.rgb, dtype="uint8")
        return img.reshape((sct_img.height, sct_img.width, 3))

def get_part_of_screen(x, y, width, height):
    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": width, "height": height}
        sct_img = sct.grab(monitor)
        img = np.frombuffer(sct_img.rgb, dtype="uint8")
        return img.reshape((sct_img.height, sct_img.width, 3))

def get_ground_y(img):
    for i in range(img.shape[0]):
        k = 0
        for j in range(img.shape[1]):
            if not img[i][j]:
                k+=1
                if k>200:
                    return i
            else:
                k = 0

def binarize(img):
    return img[:,:,2] > 83

# time.sleep(1)
img = get_fullscreen()
# img = (plt.imread("dino.png")*256).astype("uint8")

shift_x = 200
shift_y = 100
img = img[shift_y:-120,shift_x:-200,2] > 150
# ground_y = int((img==0).sum(1).argmax())
ground_y = get_ground_y(img)


ground = np.where(img[ground_y]==0)[0]
game_x = shift_x+int(ground[0])
game_y = shift_y+ground_y+25-150
game_width = int(ground[-1] - ground[0])
game_height = game_width//5

def get_game_img():
    return binarize(get_part_of_screen(game_x, game_y, game_width, game_height))
# print(type(game_y))
print("Game at:")
print(game_x, game_y, game_width, game_height)


# plt.ion()
# plt.imshow(game, cmap="gray")
# plt.show()

# dangerous_zone = game[20:, 300:400]
# print(dangerous_zone.sum(), dangerous_zone.size)

cv2.namedWindow('Game', cv2.WINDOW_NORMAL)
# cv2.namedWindow('Dangerous zone', cv2.WINDOW_NORMAL)

# dangerous zone settings
dz_width = 50
dz_left = 90
dz_top = 20
dz_bottom = 10
# dz_width = 70
# dz_left = 130
# dz_top = 20
# dz_bottom = 10

prev = time.time()
pressed = False

start = 0

game = get_game_img()
while game[19, 318]!=0:
    game = get_game_img()

pyautogui.press("space")
time.sleep(.2)

start = time.time()
print("game started")

while True:
    ratio = 1.0 + (time.time()-start)/99.6
    # print(int((time.time()-prev)*1000))
    # prev = time.time()

    game = get_game_img()

    # pressed f4 or game over
    if cv2.pollKey()==7536640 or game[19, 318]==0:
        print("shut down")
        # plt.imsave("game2.png", game)
        cv2.destroyAllWindows()
        break

    dangerous_zone = game[dz_top:-dz_bottom, dz_left:dz_left+dz_width]
    # cv2.imshow('Dangerous zone', dangerous_zone.astype("uint8") * 255)

    if not np.all(dangerous_zone):
        if not pressed:
            # check if the dino in the air
            # if np.any(game[85, 57:69]):
            #     pyautogui.press("down")
            #     print("down")
                # time.sleep(.05)

            pyautogui.press("space")
            print("space")
            time.sleep(.1)
            pyautogui.press("down")

            # time.sleep(.1)
            pressed = True
    else:
        pressed = False

    dz_game = (game * 255).astype("uint8")
    dz_game[dz_top:-dz_bottom, dz_left:dz_left+dz_width]//=2
    cv2.imshow('Game', dz_game)
    time.sleep(.05)

# 12704 ms / 6.762
# 12704 / 762 = 16.6

# (6 + (delta_ms / 16.6) / 1000) / 6