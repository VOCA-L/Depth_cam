#########################################
## Make CSV file. data is depth value  ##
## Save 15 frames each 1 second        ##
## IntelRealsense D455 Depth Cam.      ##
## Feb 03 2022 - Feb 07 2022           ##
#########################################

# First import the library
import csv
import pyrealsense2 as rs
# import numpy as np
from datetime import datetime, timedelta


try:
    # Create a context object. This object owns the handles to all connected realsense devices
    pipeline = rs.pipeline()

    # Configure streams
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)

    # Start streaming
    pipeline.start(config)

    # open csv file
    open_file = open("object_dataset_test.csv", "w")
    writer = csv.writer(open_file)
    # writer.writeheader()

    first_time = datetime.now()
    print(first_time)

    for i in range(15):
        # This call waits until a new coherent set of frames is available on a device
        # Calls to get_frame_data(...) and get_frame_timestamp(...) on a device will return stable values until wait_for_frames(...) is called
        # data_list = np.array([])
        data_list = []
        frames = pipeline.wait_for_frames()
        depth = frames.get_depth_frame()
        if not depth: continue
        
        # data_list = np.append(data_list, start_time)
        # data_list.append(start_time)
        loading = 0 #307,200

        for y in range(480):
            for x in range(640):
                loading = loading + 1
                dist = depth.get_data(x, y)
                dist = int(dist)
                data_list.append(dist)
                # print('LOADING :', loading, '/ 307200')

        data_list = map(int, data_list)
        writer.writerow(data_list)

        # exit(0)

    open_file.close()
    final_time = datetime.now()
    print(final_time - first_time)
except Exception as e:
    print(e)
    pass
