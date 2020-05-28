import cv2
import time
import numpy as np
from utils.zmq_utils import ZMQOutput
from config import ipc_queue_max_size


def video_streaming_worker(video_path, out_queue, max_speed=False):
    if isinstance(out_queue, str):
        out_queue = ZMQOutput(out_queue, max_size=ipc_queue_max_size)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    time_per_frame = 1 / fps
    while (cap.isOpened()):
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            print("StreamingWorker: sending Last Frame")
            out_queue.send(np.empty([1, 1]))
            break
        out_queue.send(frame)
        if not max_speed:
            loop_time = time.time() - start_time
            if loop_time < time_per_frame:
                time.sleep(time_per_frame - loop_time)

