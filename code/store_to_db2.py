#################################
# Detph value store to db 2G
# Save 15 frames in one field.
# IntelRealsense D455 Depth Cam.
#################################

import pyrealsense2 as rs
from pymongo import MongoClient
import time
from datetime import datetime, timedelta

db_client = MongoClient("localhost", 27017)
db_doc = db_client['depth_test']
db = db_doc['dt6']

list_to_db = []

try:
    ## Setup
    pipeline = rs.pipeline()

    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)

    pipeline.start(config)
    ## save time data and frame data
    count = 0
    while True:
        start = datetime.now()
        print(start)

        frames = pipeline.wait_for_frames()
        depth = frames.get_depth_frame()
        if not depth: print(f"error")

        for y in range(480): 
            for x in range(640):
                dist = depth.get_distance(x, y)
                list_to_db.append(dist)
        print(count)
        count = count + 1
        end = datetime.now()
        print(end)
        print(end - start)
        db.insert_one({"time": start, "depth": list_to_db})
        print("#############################################")
        # print(end)
        # print(end - start)
    exit(0)
except Exception as e:
    print(e)
    pass

