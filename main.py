from videos import videos
from ultralytics import YOLO
from boxmot import BYTETracker
import cv2
import time
import json
import torch
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import logging

logging.getLogger("ultralytics").setLevel(logging.WARNING)

torch.cuda.set_device(0)

model = YOLO('models/model_- 14 october 2023 16_46.pt')
filename = 'cam_5m.mp4'
source = 'data/samples/' + filename
tracker = BYTETracker()
cap = cv2.VideoCapture(source)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
size = (frame_width, frame_height)
writer = cv2.VideoWriter('data/detect/result.avi',
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         30, size)

verify_object = {}
verify_frame = 30 * 2
passed_object = {}
thickness = 2
font_scale = 0.5
frame_counter = 0
stride = 1

vehicles_speed = ['car', 'motorcycle']
root_timestamp = time.time()


def stat_table(frame,
               font=cv2.FONT_HERSHEY_PLAIN,
               font_scale=2,
               text_color=(255, 255, 255),
               font_thickness=3,
               text_color_bg=(0, 0, 0)):
    cv2.rectangle(frame, (10, 10), (1270 - 10, 100), text_color_bg, -1)

    for vehicle, vehicle_object in vehicles.items():
        if len(vehicle_object.speed_value) == 0:
            vehicle_object_speed = None
        else:
            vehicle_object_speed = round(sum(vehicle_object.speed_value) / len(vehicle_object.speed_value), 2)
        cv2.putText(frame,
                    f"{vehicle}: {len(vehicle_object.count)} {vehicle_object_speed}",
                    vehicle_object.pos, font, font_scale, text_color,
                    font_thickness)


def draw_text(frame, text,
              pos=(0, 0),
              font=cv2.FONT_HERSHEY_PLAIN,
              font_scale=5,
              text_color=(0, 255, 0),
              font_thickness=2,
              text_color_bg=(0, 0, 0)
              ):
    x, y = pos
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    cv2.rectangle(frame, pos, (x + text_w, y + text_h), text_color_bg, -1)
    cv2.putText(frame, text, (x, int(y + text_h + font_scale - 1)), font, font_scale, text_color, font_thickness)

    return text_size


def direction(A, B, P):
    # Subtracting co-ordinates of 
    # point A from B and P, to 
    # make A as origin
    A = list(A)
    B = list(B)
    P = list(P)

    B[0] -= A[0]
    B[1] -= A[1]
    P[0] -= A[0]
    P[1] -= A[1]

    # Determining cross Product
    cross_product = B[0] * P[1] - B[1] * P[0]

    # Return RIGHT if cross product is positive
    if cross_product > 0:
        return 'right'

    # Return LEFT if cross product is negative
    if cross_product < 0:
        return 'left'

    # Return ZERO if cross product is zero
    return 'zero'


names: [str] = model.names

vehicles = videos[filename].vehicles
lines = videos[filename].lines
timestamp = videos[filename].timestamp
region = videos[filename].region

while cap.isOpened():
    success, frame = cap.read()

    if not success:
        break

    if frame_counter != stride:
        frame_counter += 1
        continue

    frame_counter = 1

    result = model(frame)
    result = result[0]

    ts = tracker.update(result.boxes.data.cpu().numpy(), frame)

    cv2.line(frame, lines.begin[0], lines.begin[1], (0, 0, 255), 2)
    cv2.line(frame, lines.end[0], lines.end[1], (0, 0, 255), 2)
    for i in range(len(region) - 1):
        cv2.line(frame, region[i], region[i + 1], (255, 255, 120), 1)
    cv2.line(frame, region[-1], region[0], (255, 255, 120), 1)

    xyxys = ts[:, 0:4].astype('int')  # float64 to int
    ids = ts[:, 4].astype('int')  # float64 to int
    confs = ts[:, 5]
    clss = ts[:, 6]

    if ts.shape[0] != 0:
        zip_data = zip(xyxys, ids, confs, clss)
        zip_data = sorted(zip_data, key=lambda x: x[1])

        for xyxy, id, conf, cls in zip_data:
            center = ((xyxy[0] + xyxy[2]) / 2, (xyxy[1] + xyxy[3]) / 2)
            if not Polygon(region).contains(Point(center)):
                continue

            cv2.rectangle(
                frame,
                (xyxy[0], xyxy[1]),
                (xyxy[2], xyxy[3]),
                vehicles[names[cls]].color,
                thickness
            )
            draw_text(
                frame,
                f'id: {id}, conf: {conf:.2f}, c: {names[cls]}',
                (xyxy[0], xyxy[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale,
                vehicles[names[cls]].color,
                thickness,
                (0, 0, 0)
            )

            verified = False
            if id not in verify_object:
                verify_object[id] = {
                    'frame': 1,
                    'cls': None,
                }
            elif verify_object[id]['frame'] < verify_frame:
                if id == 18:
                    print(verify_object[id]['frame'])
                if names[cls] == verify_object[id]['cls']:
                    verify_object[id]['frame'] += 1
                    if verify_object[id]['frame'] == verify_frame and id > vehicles[names[cls]].last_id:
                        vehicles[names[cls]].count.append(timestamp + (time.time() - root_timestamp))
                        vehicles[names[cls]].last_id = id
                else:
                    if id == 18:
                        print(f'{verify_object[id]["cls"]} / {names[cls]}')
                    verify_object[id]['frame'] = 1
                    verify_object[id]['cls'] = names[cls]
            else:
                verified = True

            if verified:
                vehicle_object = vehicles[verify_object[id]['cls']]

                if verify_object[id]['cls'] in vehicles_speed:

                    if id not in passed_object:
                        object_direction = direction(lines.begin[0], lines.begin[1], center)
                        if object_direction == 'zero' or lines.direction != object_direction:
                            # print('none')
                            # print(f'center: {center}')
                            # print(f'object_direction: {object_direction}')
                            # print(f'lines.direction: {lines.direction}')
                            # print('------------------------------------')
                            passed_object[id] = {}
                    elif 'begin' not in passed_object[id]:
                        object_direction = direction(lines.begin[0], lines.begin[1], center)
                        if object_direction == 'zero' or lines.direction == object_direction:
                            # print('begin')
                            # print(f'id: {id}')
                            # print(f'center: {center}')
                            # print(f'object_direction: {object_direction}')
                            # print(f'lines.direction: {lines.direction}')
                            # print('------------------------------------')

                            passed_object[id]['begin'] = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
                    elif 'end' not in passed_object[id]:
                        object_direction = direction(lines.end[0], lines.end[1], center)
                        if object_direction == 'zero' or lines.direction == object_direction:
                            # print('end')
                            # print(f'id: {id}')
                            # print(f'center: {center}')
                            # print(f'object_direction: {object_direction}')
                            # print(f'lines.direction: {lines.direction}')
                            # print('------------------------------------')

                            passed_object[id]['end'] = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000

                            vehicle_object.speed_timestamp.append(timestamp + (time.time() - root_timestamp))
                            vehicle_object.speed_value.append(
                                lines.distance / (passed_object[id]['end'] - passed_object[id]['begin'])
                                * 3600 / 1000)

    stat_table(frame)

    writer.write(frame)
    cv2.imshow("Results", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# for vehicle in vehicles:
#     for timestamp in vehicles[vehicle].speed_timestamp

cap.release()
writer.release()
cv2.destroyAllWindows()

speed_result = {}
for vehicle in vehicles:
    speed_result[vehicle] = {
        'count': vehicles[vehicle].count,
        'speed': vehicles[vehicle].speed_value,
        'timestamp': vehicles[vehicle].speed_timestamp
    }

print(speed_result)

with open("result.json", "w+") as outfile:
    json.dump(speed_result, outfile, indent=4)

print('finish')
