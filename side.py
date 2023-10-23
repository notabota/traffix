from ultralytics import YOLO
from boxmot import BYTETracker
import cv2

source = 'data/samples/cam.mp4'
cap = cv2.VideoCapture(source)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
size = (frame_width, frame_height)


def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'({x}, {y})')



while cap.isOpened():
    success, frame = cap.read()

    if not success:
        break

    cv2.line(frame, (411, 220), (582, 193), (0, 255, 0), 2)
    cv2.line(frame, (582, 193), (1279, 464), (0, 255, 0), 2)
    cv2.line(frame, (1279, 464), (1279, 718), (0, 255, 0), 2)
    cv2.line(frame, (1279, 718), (313, 718), (0, 255, 0), 2)
    cv2.line(frame, (313, 718), (411, 220), (0, 255, 0), 2)

    cv2.imshow("result", frame)
    cv2.setMouseCallback('result', click_event)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print('finish')
