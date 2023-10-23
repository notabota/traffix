import time


class Vehicle:
    def __init__(self, color, pos=(0, 0)):
        self.color = color  # BGR
        self.pos = pos
        self.count = []
        self.last_id = -1

        self.speed_value = []
        self.speed_timestamp = []

    def __str__(self):
        return f"count: {self.count}\nlast_id: {self.last_id}"


class Line:
    def __init__(self, begin, end, distance):
        self.begin = begin
        self.end = end
        self.distance = distance

        if begin[0][1] < end[0][1]:
            self.direction = 'right'
        else:
            self.direction = 'left'


class Video:
    def __init__(self, lines: Line, vehicles: {str: Vehicle}, timestamp, region=None):
        if region is None:
            region = [(0, 0), (1280, 0), (1280, 960), (0, 960)]
        self.lines = lines
        self.vehicles = vehicles
        self.timestamp = timestamp
        self.region = region


videos = {
    'cam.mp4': Video(
        lines=Line(((393, 282), (853, 244)), ((377, 363), (1016, 306)), 10),
        vehicles={
            'ambulance': Vehicle((55, 40, 243), (900, 80)),
            'bicycle': Vehicle((118, 79, 69), (550, 80)),
            'bus': Vehicle((0, 219, 254), (700, 40)),
            'car': Vehicle((0, 252, 124), (30, 40)),
            'motorcycle': Vehicle((255, 255, 0), (30, 80)),
            'person': Vehicle((208, 253, 255), (300, 40)),
            'truck': Vehicle((139, 0, 0), (1000, 40)),
        },
        timestamp=time.time()
    ),
    'cam_5m.mp4': Video(
        lines=Line(((393, 282), (853, 244)), ((377, 363), (1016, 306)), 12),
        vehicles={
            'ambulance': Vehicle((55, 40, 243), (900, 80)),
            'bicycle': Vehicle((118, 79, 69), (550, 80)),
            'bus': Vehicle((0, 219, 254), (700, 40)),
            'car': Vehicle((0, 252, 124), (30, 40)),
            'motorcycle': Vehicle((255, 255, 0), (30, 80)),
            'person': Vehicle((208, 253, 255), (300, 40)),
            'truck': Vehicle((139, 0, 0), (1000, 40)),
        },
        region=[(416, 194), (605, 187), (1280, 343), (1280, 720), (313, 720)],
        timestamp=1697879568
    ),
    'hmm.mp4': Video(
        lines=Line(((393, 282), (853, 244)), ((377, 363), (1016, 306)), 10),
        vehicles={
            'ambulance': Vehicle((55, 40, 243), (900, 80)),
            'bicycle': Vehicle((118, 79, 69), (550, 80)),
            'bus': Vehicle((0, 219, 254), (700, 40)),
            'car': Vehicle((0, 252, 124), (30, 40)),
            'motorcycle': Vehicle((255, 255, 0), (30, 80)),
            'person': Vehicle((208, 253, 255), (300, 40)),
            'truck': Vehicle((139, 0, 0), (1000, 40)),
        },
        timestamp=time.time()
    ),
    'cam2_2m30.mp4': Video(
        lines=Line(((550, 220), (1076, 216)), ((500, 280), (1236, 261)), 10),
        vehicles={
            'ambulance': Vehicle((55, 40, 243), (900, 80)),
            'bicycle': Vehicle((118, 79, 69), (550, 80)),
            'bus': Vehicle((0, 219, 254), (700, 40)),
            'car': Vehicle((0, 252, 124), (30, 40)),
            'motorcycle': Vehicle((255, 255, 0), (30, 80)),
            'person': Vehicle((208, 253, 255), (300, 40)),
            'truck': Vehicle((139, 0, 0), (1000, 40)),
        },
        timestamp=time.time()
    ),
    'cam2_2206.mp4': Video(
        lines=Line(((550, 220), (1076, 216)), ((500, 280), (1236, 261)), 10),
        vehicles={
            'ambulance': Vehicle((55, 40, 243), (900, 80)),
            'bicycle': Vehicle((118, 79, 69), (550, 80)),
            'bus': Vehicle((0, 219, 254), (700, 40)),
            'car': Vehicle((0, 252, 124), (30, 40)),
            'motorcycle': Vehicle((255, 255, 0), (30, 80)),
            'person': Vehicle((208, 253, 255), (300, 40)),
            'truck': Vehicle((139, 0, 0), (1000, 40)),
        },
        timestamp=time.time()
    )
}
