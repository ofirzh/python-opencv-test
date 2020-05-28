import os
from multiprocessing import Process
from workers.motion_detection_worker import motion_detection_worker
from workers.video_preview_worker import video_preview_worker
from workers.video_streaming_worker import video_streaming_worker
from utils.mp_queue_utils import SizedQueue
from config import ipc_queue_max_size


class VideoDetectionPipeline:
    def __init__(self, video_path, max_speed=False, min_area=500, use_zmq_ipc=True):
        if not os.path.exists(video_path):
            raise Exception(f"Video file not found {video_path}")

        self.workers = []
        if use_zmq_ipc:
            print("Creating ZMQ pipeline")
            self.workers.append(Process(target=video_streaming_worker, args=(video_path, "decoder_out", max_speed)))
            self.workers.append(Process(target=motion_detection_worker, args=("decoder_out", "processor_out", min_area)))
            self.workers.append(Process(target=video_preview_worker, args=("processor_out",)))
        else:
            print("Creating mp queues pipeline")
            decoder_out = SizedQueue(ipc_queue_max_size)
            detector_out = SizedQueue(ipc_queue_max_size)
            self.workers.append(Process(target=video_streaming_worker, args=(video_path, decoder_out, max_speed)))
            self.workers.append(Process(target=motion_detection_worker, args=(decoder_out, detector_out, min_area)))
            self.workers.append(Process(target=video_preview_worker, args=(detector_out,)))

    def start(self):
        for w in self.workers:
            w.start()

    def join(self):
        for w in self.workers:
            w.join()
