import os.path
import argparse
import time
from pipelines import VideoDetectionPipeline

# default video path
my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "People-6387.mp4")

if __name__ == "__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="path to the video file", default=path)
    ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
    ap.add_argument('--use-zmq', dest='use_zmq', default=True, action='store_true', help="Use standard multiprocessing queues "
                                                                         "instead of zmq")
    ap.add_argument('--max-speed', dest='max_speed', action='store_true', help="Process video as fast as possible "
                                                                             "regardless to FPS")
    args = vars(ap.parse_args())
    print(args)
    start_time = time.time()
    pipeline = VideoDetectionPipeline(args["video"], max_speed=args["max_speed"], min_area=args["min_area"], use_zmq_ipc=args["use_zmq"])
    pipeline.start()
    pipeline.join()
    print(f"ZMQ Workers Duration: {time.time()-start_time}s")
