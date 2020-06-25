import pyrealsense2 as rs
import numpy as np
import cv2

pipe = rs.pipeline()
cfg =rs.config()
profile = pipe.start(cfg)

for x in range(5):
  pipe.wait_for_frames()

# Store next frameset for later processing:
frameset = pipe.wait_for_frames()
color_frame = frameset.get_color_frame()
depth_frame = frameset.get_depth_frame()

# Cleanup:
pipe.stop()

pc = rs.pointcloud();
pc.map_to(color_frame);
pointcloud = pc.calculate(depth_frame);
pointcloud.export_to_ply("1.ply", color_frame);

