import cv2
import os
import numpy as np
import pyrealsense2 as rs
import time


def subDirPath(path):
    dir = os.path.dirname(os.path.realpath(__file__))
    new_dir = dir + path
    if not os.path.isdir(new_dir):
        os.makedirs(new_dir)
    return new_dir


# Create a pipeline
pipeline = rs.pipeline()
rs_config = rs.config()
rs_config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
rs_config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

# Start streaming

stream_started = False

try:
    profile = pipeline.start(rs_config)

    stream_started = True

    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        if not color_frame or not depth_frame:
            continue

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Render images
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(
            depth_image, alpha=0.03), cv2.COLORMAP_JET)

        time_now = str(int(time.time()))

        sub_dir = "/images/color"
        cv2.imwrite(subDirPath(sub_dir)+"/rgb-" +
                    time_now + ".jpg", color_image)

        sub_dir = "/images/depth"
        cv2.imwrite(subDirPath(sub_dir)+"/depth-" +
                    time_now + ".jpg", depth_colormap)

        break

except RuntimeError as err:
    print("Got runtime exception: " + str(err))

if stream_started:
    pipeline.stop()
