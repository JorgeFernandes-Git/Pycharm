import csv
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)


class QuestionClass:
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])  # to verify if it's correct answer

        self.user_answer = None  # verify if the user choose a answer

    def update(self, cursor, bboxs):
        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.user_answer = x + 1  # x + 1 because of the csv format
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)


# import csv file data
path_csv = "questions.csv"
with open(path_csv, newline="\n") as f:
    reader = csv.reader(f)
    data_total = list(reader)[1:]  # ignore the first row

# create object for each question
questions_list = []
for q in data_total:
    questions_list.append(QuestionClass(q))

q_num = 0
q_total = len(data_total)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    # iterate through all questions
    if q_num < q_total:
        question_simple = questions_list[q_num]
        img, bbox = cvzone.putTextRect(img, question_simple.question, [100, 100], 2, 2, offset=50, border=5,
                                       colorB=(255, 255, 255), colorR=(0, 0, 0), colorT=(255, 255, 255))
        img, bbox1 = cvzone.putTextRect(img, question_simple.choice1, [100, 250], 2, 2, offset=50, border=5,
                                        colorB=(255, 255, 255), colorR=(0, 0, 0), colorT=(255, 255, 255))
        img, bbox2 = cvzone.putTextRect(img, question_simple.choice2, [400, 250], 2, 2, offset=50, border=5,
                                        colorB=(255, 255, 255), colorR=(0, 0, 0), colorT=(255, 255, 255))
        img, bbox3 = cvzone.putTextRect(img, question_simple.choice3, [100, 400], 2, 2, offset=50, border=5,
                                        colorB=(255, 255, 255), colorR=(0, 0, 0), colorT=(255, 255, 255))
        img, bbox4 = cvzone.putTextRect(img, question_simple.choice4, [400, 400], 2, 2, offset=50, border=5,
                                        colorB=(255, 255, 255), colorR=(0, 0, 0), colorT=(255, 255, 255))

        if hands:  # hands are from the method findHands
            lm_list = hands[0]["lmList"]
            cursor = lm_list[8]  # tip of the index by mediapipe
            length, info = detector.findDistance(lm_list[8], lm_list[12])

            # click mode
            if length < 40:
                question_simple.update(cursor, [bbox1, bbox2, bbox3, bbox4])
                print(question_simple.user_answer)
                if question_simple.user_answer is not None:
                    time.sleep(0.3)
                    q_num += 1

    # draw progress bar
    bar_value = 150 + ((1100 - 150) // q_total) * q_num
    cv2.rectangle(img, (150, 600), (bar_value, 650), (255, 0, 0), cv2.FILLED)
    cv2.rectangle(img, (150, 600), (1100, 650), (0, 255, 0), 5)

    cv2.imshow("Image", img)

    # ESC to close
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break