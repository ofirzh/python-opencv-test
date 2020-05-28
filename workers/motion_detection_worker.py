import numpy as np
from detectors.detector import Detector
from utils.zmq_utils import ZMQInput, ZMQOutput
from config import ipc_queue_max_size


def motion_detection_worker(in_queue, out_queue, min_area):
    """
    Worker function that reads frame from queue (ZMQ or MP.QUEUE) and search for detections
    :param in_queue:
    :param out_queue:
    :return:
    """
    # Init ZMQ if queue name is string
    if isinstance(in_queue, str):
        in_queue = ZMQInput(in_queue)
    if isinstance(out_queue, str):
        out_queue = ZMQOutput(out_queue, max_size=ipc_queue_max_size)

    detector = Detector(min_area=min_area)

    while True:
        frame = in_queue.receive()
        # if the frame could not be grabbed, then we have reached the end
        # of the video
        out_queue.send(frame)
        if frame is None or frame.shape == (1, 1):
            print("DetectionWorker: Last frame received")
            break
        detections = detector.predict(frame)
        out_queue.send(np.array(detections))
    # send empty detections list
    out_queue.send(np.array([]))
