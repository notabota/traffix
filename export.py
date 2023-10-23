import json
import datetime
from videos import videos
import pandas as pd
import cv2 as cv

filename = 'cam_5m.mp4'
source = 'data/samples/' + filename

cap = cv.VideoCapture(source)
fps = cap.get(cv.CAP_PROP_FPS)
frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
duration = frame_count / fps

vehicles_speed = ['car', 'motorcycle']
vehicles = videos[filename].vehicles
lines = videos[filename].lines
timestamp = videos[filename].timestamp
region = videos[filename].region

period = 60

with open("result.json", "r+") as outfile:
    result = json.load(outfile)

period_speed = {}
for vehicle in vehicles_speed:
    period_speed[vehicle] = []
    speed_sum = 0
    speed_count = 0
    period_timestamp = timestamp + period
    count = len(result[vehicle]['speed'])
    print(count)
    for i in range(count):
        if result[vehicle]['timestamp'][i] < period_timestamp:
            speed_sum += result[vehicle]['speed'][i]
            speed_count += 1
        else:
            if speed_count != 0:
                speed_average = speed_sum / speed_count
            else:
                speed_average = None
            period_speed[vehicle].append((period_timestamp, speed_average))
            period_timestamp += 30
            speed_sum = 0
            speed_count = 0

    if speed_count != 0:
        speed_average = speed_sum / speed_count
    else:
        speed_average = None
    period_speed[vehicle].append((timestamp + duration, speed_average))

    print(period_speed)

summary = {
    "Average speed": [],
    "Count": []
}
vehicles_name = []

for vehicle in vehicles:
    vehicles_name.append(vehicle)
    if len(result[vehicle]['speed']) != 0:
        speed_average = sum(result[vehicle]['speed']) / len(result[vehicle]['speed'])
    else:
        speed_average = ''
    summary["Average speed"].append(speed_average)
    summary["Count"].append(result[vehicle]['count'])



summary_frame = pd.DataFrame(summary, index=vehicles_name)
print(summary_frame)
