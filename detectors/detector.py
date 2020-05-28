import cv2
import imutils


class Detector:
    def __init__(self, resize_width=500, min_area=500):
        self.first_frame = None
        self.resize_to_width = resize_width
        self.ratio = None
        self.min_area = min_area

    def predict(self, frame):
        """
        Recieves video frame (ndarray), search and return detections.
        :param frame:
        :return:
        """

        # resize the frame, convert it to grayscale, and blur it
        resized_frame = imutils.resize(frame, width=self.resize_to_width)
        gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if self.first_frame is None:
            self.first_frame = gray
            self.ratio = frame.shape[1]/resized_frame.shape[1]
            return []

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(self.first_frame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        rects = []
        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < self.min_area:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text

            rect = cv2.boundingRect(c)
            resized_rect = []
            for r in rect:
                resized_rect.append(int(r * self.ratio))
            rects.append(resized_rect)
        return rects
