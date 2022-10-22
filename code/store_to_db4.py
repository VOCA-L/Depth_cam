#######################################
## Detph value store to Mongodb 4G   ##
## Save 15 frames in one field.      ##
## IntelRealsense D455 Depth Cam.    ##
## Feb 07 2022 - Feb 14 2022         ##
#######################################

import pyrealsense2 as rs
from pymongo import MongoClient
import time
from datetime import datetime, timedelta
import numpy as np
import mongowrapper as mdb
import sys 

# db_client = MongoClient("localhost", 27017)
# db_doc = db_client['depth_test']
# db = db_doc['dt4_8']

db = mdb.MongoWrapper(dbName='depth_test', collectionName='dt4_8', hostname='localhost', port='27017')

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
    arr = np.array([])



    for i in range(15):
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()

        depth_image = depth_frame.get_data()
        depth_image = np.asanyarray(depth_image)
        depth_image = depth_image.ravel()
        arr = np.append(arr, depth_image)
        print(i)
        
    # print(arr)
    print(sys.getsizeof(arr))
    my_dict = {'data':'1', 'data':arr}
    # db.insert_one({"depth": arr})
    db.save(my_dict)
    end_time = datetime.now()
    print(end_time)
    print(end_time - start_time)
    exit(0)

except Exception as e:
    print(e)
    pass


