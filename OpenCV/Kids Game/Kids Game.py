import os
import random

import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = FaceMeshDetector(maxFaces=1)
id_list = [0, 17, 78, 292]

# import objects
folder_eatable = 'Objects/eatable'
list_eatable = os.listdir(folder_eatable)
eatables = []
for obj in list_eatable:
    eatables.append(cv2.imread(f'{folder_eatable}/{obj}', cv2.IMREAD_UNCHANGED))

folder_noneatable = 'Objects/noneatable'
list_noneatable = os.listdir(folder_noneatable)
noneatables = []
for obj in list_noneatable:
    noneatables.append(cv2.imread(f'{folder_noneatable}/{obj}', cv2.IMREAD_UNCHANGED))

current_obj = eatables[0]
pos = [300, 0]
speed = 10
count = 0
misses = 0
is_eatable = True
game_over = False


def reset_obj():
    global is_eatable
    pos[0] = random.randint(100, 1280 - 100)
    pos[1] = 0
    rand_obj = random.randint(0, 1)
    if rand_obj == 0:
        current_obj = noneatables[random.randint(0, 3)]
        is_eatable = False
    else:
        current_obj = eatables[random.randint(0, 3)]
        is_eatable = True
    return current_obj


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img, faces = detector.findFaceMesh(img, draw=False)

    img = cvzone.overlayPNG(img, current_obj, pos)
    pos[1] += speed
    if pos[1] > 720 - 100 - 50:
        current_obj = reset_obj()
    if not game_over:
        if faces:
            face = faces[0]
            # for id_num, point in enumerate(face):
            #     cv2.putText(img, str(id_num), point, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 1)

            for id in id_list:
                cv2.circle(img, face[id], 5, (255, 0, 255), 5)
            cv2.line(img, face[id_list[0]], face[id_list[1]], (0, 255, 0), 3)
            cv2.line(img, face[id_list[2]], face[id_list[3]], (0, 255, 0), 3)

            up = face[id_list[0]]
            down = face[id_list[1]]
            # print(up)

            up_down, _ = detector.findDistance(face[id_list[0]], face[id_list[1]])
            left_right, _ = detector.findDistance(face[id_list[2]], face[id_list[3]])
            ratio = int(up_down / left_right * 100)
            # print(ratio)

            cx, cy = (up[0] + down[0]) // 2, (up[1] + down[1]) // 2
            cv2.line(img, (cx, cy), (pos[0] + 50, pos[1] + 50), (0, 255, 0), 3)
            dist_mouth_obj, _ = detector.findDistance((cx, cy), (pos[0] + 50, pos[1] + 50))
            # print(dist_mouth_obj)

            if ratio > 60:
                mouth_status = "OPEN"
            else:
                mouth_status = "CLOSED"
            cv2.putText(img, mouth_status, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)

            if dist_mouth_obj < 100 and ratio > 60:
                if is_eatable:
                    count += 1
                else:
                    game_over = True
                current_obj = reset_obj()

            if is_eatable and pos[1] > 720 - 100 - 50 - 10:
                misses += 1

            cv2.putText(img, f'Eaten: {str(count)}', (1100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 4)
            cv2.putText(img, f'Missed: {str(misses)}', (1100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 4)
            # print(is_eatable)
    else:
        cv2.putText(img, 'GAME OVER', (200, 400), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 255), 5)
        cv2.putText(img, f'You Ate {str(count)} Objects', (200, 500), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)
        cv2.putText(img, f'You Missed {str(misses)} Objects', (100, 600), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)

    cv2.imshow("Image", img)
    # ESC to close
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    if k == ord('r') and game_over:
        reset_obj()
        current_obj = eatables[random.randint(0, 3)]
        is_eatable = True
        game_over = False
        count = 0
        misses = 0

