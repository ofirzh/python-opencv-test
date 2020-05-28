import os.path
import time
from pipelines import VideoDetectionPipeline

# default video path
my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "People-6387.mp4")

if __name__ == "__main__":
    cycles = 3
    total_zmq = 0
    total_mpq = 0
    for c in range(cycles):
        start_time = time.time()
        pipeline = VideoDetectionPipeline(path, max_speed=True, min_area=500, use_zmq_ipc=True)
        pipeline.start()
        pipeline.join()
        delta = time.time() - start_time
        total_zmq += delta
        print(f"ZMQ Workers Duration: {delta}s")

        start_time= time.time()
        pipeline = VideoDetectionPipeline(path, max_speed=True, min_area=500, use_zmq_ipc=False)
        pipeline.start()
        pipeline.join()
        delta = time.time() - start_time
        total_mpq += delta
        print(f"Mp Queue Workers Duration: {delta}s")

    print(f"AVG ZMQ Workers Duration: {total_zmq/cycles}s")
    print(f"AVG MP QUEUE Workers Duration: {total_mpq/cycles}s")