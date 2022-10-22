#######################################
## Detph value store to Mongodb 3G   ##
## Save 20 frames in one field.      ##
## IntelRealsense D455 Depth Cam.    ##
## Feb 03 2022 - Feb 07 2022         ##
#######################################

import pyrealsense2 as rs
from pymongo import MongoClient
import time
from datetime import datetime, timedelta
# import numpy as np
import struct

db_client = MongoClient("localhost", 27017)
db_doc = db_client['depth_test']
db = db_doc['dt3_7']

try:
    ## Setup
    pipeline = rs.pipeline()

    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)

    pipeline.start(config)

    ## save time data and frame data to MongoDB
# while True:
    start_time = datetime.now()
    print(start_time)
    arr = []

    for i in range(15):
        frames = pipeline.wait_for_frames()
        depth = frames.get_depth_frame()
        if not depth: print(f"error")

        for y in range(480): 
            for x in range(640):
                dist = depth.get_distance(x, y) * 1000
                dist = int(dist)
                arr.append(dist)
        print(i)
    end_time = datetime.now()
    print(end_time)
    db.insert_one({"depth": arr})
    # break
# exit(0)

except Exception as e:
    print(e)
    pass


