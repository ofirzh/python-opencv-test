import cv2
from utils.zmq_utils import ZMQInput


def blur_detection(image, factor=3.0):
    # automatically determine the size of the blurring kernel based
    # on the spatial dimensions of the input image
    (h, w) = image.shape[:2]
    kW = int(w / factor)
    kH = int(h / factor)
    # ensure the width of the kernel is odd
    if kW % 2 == 0:
        kW -= 1
    # ensure the height of the kernel is odd
    if kH % 2 == 0:
        kH -= 1
    # apply a Gaussian blur to the input image using our computed
    # kernel size
    # return cv2.GaussianBlur(image, (kW, kH), 0)
    return cv2.GaussianBlur(image, (19, 19), 0)


def video_preview_worker(in_queue):
    """
    Receives frames and detections, draws detections on frame and preview
    blur from https://www.pyimagesearch.com/2020/04/06/blur-and-anonymize-faces-with-opencv-and-python/
    :param in_queue:
    :return:
    """
    if isinstance(in_queue, str):
        in_queue = ZMQInput(in_queue)
    while True:
        frame = in_queue.receive()
        rects = in_queue.receive()
        preview_frame = frame.copy()
        if rects is not None:
            for rect in rects:
                (x, y, w, h) = tuple(rect)
                preview_frame[y:y + h, x:x + w] = blur_detection(frame[y:y + h, x:x + w])
                cv2.rectangle(preview_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('frame', preview_frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or frame.shape == (1, 1):
            print("PreviewWorker: Last frame received")
            break

    cv2.destroyAllWindows()
