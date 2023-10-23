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

period = 30

with open("result.json", "r+") as outfile:
    result = json.load(outfile)

period_vehicle = {}

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
    summary["Count"].append(len(result[vehicle]['count']))

    period_vehicle[vehicle] = {
        "Average speed": [],
        "Count": [],
        "Timestamp": []
    }

    vehicle_count = 0
    period_timestamp = timestamp + period
    i = 0
    for _ in range(int(duration / period) + 1):
        vehicle_count = 0
        while i < len(result[vehicle]['count']) and result[vehicle]['count'][i] < period_timestamp:
            vehicle_count += 1
            i += 1
        else:
            period_vehicle[vehicle]["Count"].append(vehicle_count)

    if vehicle in vehicles_speed:
        speed_sum = 0
        speed_count = 0
        period_timestamp = timestamp + period
        for i in range(len(result[vehicle]['speed'])):
            if result[vehicle]['speed_timestamp'][i] < period_timestamp:
                speed_sum += result[vehicle]['speed'][i]
                speed_count += 1
            else:
                if speed_count != 0:
                    speed_average = speed_sum / speed_count
                else:
                    speed_average = None
                period_vehicle[vehicle]["Average speed"].append(speed_average)
                period_vehicle[vehicle]["Timestamp"].append(period_timestamp)
                period_timestamp += 30
                speed_sum = result[vehicle]['speed'][i]
                speed_count = 1

        if speed_count != 0:
            speed_average = speed_sum / speed_count
        else:
            speed_average = None
        period_vehicle[vehicle]["Average speed"].append(speed_average)
        period_vehicle[vehicle]["Timestamp"].append(timestamp + duration)

summary_frame = pd.DataFrame(summary, index=vehicles_name)
summary_frame.to_excel('result.xlsx')
print(period_vehicle)
print(summary_frame)
