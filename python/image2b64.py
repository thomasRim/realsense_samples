import cv2
import numpy as np
import pyrealsense2 as rs
import time

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

frame_n = 0

try:
    while True:

        frames = pipeline.wait_for_frames()
        if frame_n != 5:
            frame_n += 1
            continue
        frame_n = 0

        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        if not color_frame or not depth_frame:
            continue

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Render images
        depth_colormap = cv2.applyColorMap(
            cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET
        )

        image = color_image  # cv2.resize(color_image, (20, 20))
        cv2.imwrite("rgb-" + time.time() + ".jpg", image)

        image = cv2.resize(depth_colormap, (640, 480))
        cv2.imwrite("depth-" + time.time() + ".jpg", image)
        break


finally:

    # Stop streaming
    pipeline.stop()
#
