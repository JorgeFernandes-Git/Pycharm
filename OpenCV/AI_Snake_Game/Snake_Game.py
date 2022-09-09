import math
import random

import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=1)


class SnakeGameClass:
    def __init__(self, path_food):
        self.points = []  # all points of the snake
        self.lengths = []  # distance between each point
        self.current_length = 0  # total length of the snake
        self.allowed_length = 200  # total allowed length
        self.previous_head = 0, 0  # previous head point

        self.img_food = cv2.imread(path_food, cv2.IMREAD_UNCHANGED)
        self.h_food, self.w_food, _ = self.img_food.shape
        self.food_points = 0, 0
        self.random_food_location()

        self.score = 0
        self.game_over = False

    def random_food_location(self):
        self.food_points = random.randint(100, 1000), random.randint(100, 600)

    def update(self, img_main, current_head):

        if self.game_over:
            cvzone.putTextRect(img_main, "GAME OVER", [300, 400], scale=7, thickness=5, offset=20)
            cvzone.putTextRect(img_main, f'Final Score: {self.score}', [200, 550], scale=7, thickness=5, offset=20)
        else:
            px, py = self.previous_head
            cx, cy = current_head

            self.points.append([cx, cy])
            distance = math.hypot(cx - px, cy - py)
            self.lengths.append(distance)
            self.current_length += distance
            self.previous_head = cx, cy

            # Length reduction
            if self.current_length > self.allowed_length:
                for i, length in enumerate(self.lengths):
                    self.current_length -= length
                    self.lengths.pop(i)
                    self.points.pop(i)

                    if self.current_length < self.allowed_length:
                        break

            # Check if the snake ate the food
            rx, ry = self.food_points
            if rx - self.w_food // 2 < cx < rx + self.w_food // 2 and ry - self.h_food // 2 < cy < ry + self.h_food // 2:
                # print('ate')
                self.random_food_location()
                self.allowed_length += 50
                self.score += 1
                # print(self.score)

            # Draw snake
            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(img_main, self.points[i - 1], self.points[i], (0, 0, 255), 20)
                cv2.circle(img_main, self.points[-1], 20, (255, 0, 255), cv2.FILLED)

            # Draw food
            img_main = cvzone.overlayPNG(img_main, self.img_food, (rx - self.w_food // 2, ry - self.h_food // 2))
            cvzone.putTextRect(img_main, f'Score: {self.score}', [50, 80], scale=3, thickness=3, offset=10)

            # check for collision
            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img_main, [pts], False, (0, 200, 0), 3)
            min_dist = cv2.pointPolygonTest(pts, (cx, cy), True)
            print(min_dist)
            if -0.5 <= min_dist <= 0.5:
                # print('hit')
                self.game_over = True
                self.points = []  # all points of the snake
                self.lengths = []  # distance between each point
                self.current_length = 0  # total length of the snake
                self.allowed_length = 500  # total allowed length
                self.previous_head = 0, 0  # previous head point
                self.random_food_location()

        return img_main


game = SnakeGameClass('Donut.png')

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lm_list = hands[0]['lmList']
        point_index = lm_list[8][0:2]
        img = game.update(img, point_index)

    cv2.imshow("Image", img)
    # ESC to close
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    if k == ord('r') and game.game_over:
        game.game_over = False
        game.score = 0
