import pyrealsense2 as rs
from pymongo import MongoClient

db_client = MongoClient("localhost", 27017)
db_doc = db_client['lidar_test']
db = db_doc['lt_2']

list_to_db = []

try:
    pipeline = rs.pipeline()

    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    pipeline.start(config)

    frames = pipeline.wait_for_frames()
    depth = frames.get_depth_frame()
    if not depth: print(f"error")

    coverage = [0]*64
    for y in range(480): 
        for x in range(640):
            dist = depth.get_distance(x, y)
            list_to_db.append(dist)
    print("fin")
    db.insert_one({"depth": list_to_db})
    exit(0)
except Exception as e:
    print(e)
    pass
