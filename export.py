import json
from datetime import datetime
from videos import videos
import pandas as pd
import cv2 as cv

filename = 'cam_5m.mp4'
source = 'data/samples/' + filename

vehicles_speed = ['car', 'motorcycle']
vehicles = videos[filename].vehicles

period = 30

with open("result.json", "r+") as outfile:
    result = json.load(outfile)

speed_vehicle = {}

summary = {
    "Average speed": [],
    "Count": []
}

vehicles_name = []
vehicles_speed_name = []

for vehicle in vehicles:
    vehicles_name.append(vehicle)
    if len(result[vehicle]['speed']) != 0:
        speed_average = sum(result[vehicle]['speed']) / len(result[vehicle]['speed'])
    else:
        speed_average = ''

    summary["Average speed"].append(speed_average)
    summary["Count"].append(len(result[vehicle]['count']))

    if vehicle in vehicles_speed:
        speed_vehicle[vehicle] = {
            "Timestamp": [],
            "Speed": [],
        }
        vehicles_speed_name.append(vehicle)
        for i in range(len(result[vehicle]['speed'])):
            speed_vehicle[vehicle]["Speed"].append(result[vehicle]['speed'][i])
            speed_vehicle[vehicle]["Timestamp"].append(datetime.fromtimestamp(result[vehicle]['speed_timestamp'][i]))

writer = pd.ExcelWriter(
    "result.xlsx",
    engine="xlsxwriter",
    datetime_format="dd/mm/yyyy hh:mm:ss",
    date_format="dd/mm/yyyy",
)
summary_frame = pd.DataFrame(summary, index=vehicles_name)
summary_frame.to_excel(writer, sheet_name='Summary')

for vehicle in vehicles_speed_name:
    speed_vehicle_frame = pd.DataFrame(speed_vehicle[vehicle])
    speed_vehicle_frame.to_excel(writer, sheet_name=vehicle.capitalize())

    workbook = writer.book
    worksheet = writer.sheets[vehicle.capitalize()]
    (max_row, max_col) = speed_vehicle_frame.shape
    worksheet.set_column(1, max_col, 20)

writer.close()
print(speed_vehicle)
print(summary_frame)
