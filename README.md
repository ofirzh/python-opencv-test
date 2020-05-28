# python-opencv-test

Run pipeline that uses ZMQ IPC  
`python main.py -v /home/redbull/Videos/example_01.mp4`

[for more info about sending numpy arrays](https://pyzmq.readthedocs.io/en/latest/serialization.html#using-your-own-serialization)


Run pipeline that uses multiprocessing queues 
`python main.py -v /home/redbull/Videos/example_01.mp4 --no-zmq`