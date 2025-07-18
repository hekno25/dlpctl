import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from time import perf_counter
import os

class BubbleKalman(cv.KalmanFilter):
    def __init__(self, center, dt, process_noise=1e-2, measurement_noise=1e-1):
        super().__init__(2,1)
        # transition matrix F
        self.transitionMatrix = np.array([[1, dt],[0, 1]], dtype=np.float32)

        # measurement matrix H
        self.measurementMatrix = np.array([[1, 0]], dtype=np.float32)

        # process noise covariance Q
        self.processNoiseCov = process_noise * np.eye(2, dtype=np.float32)

        # measurement noise covariance R
        self.measurementNoiseCov = np.array([[measurement_noise]], dtype=np.float32)

        # initial state estimate
        self.statePost = np.zeros((2, 1), dtype=np.float32)

        # initial state covariance
        self.errorCovPost = np.eye(2, dtype=np.float32)
        self.center = center


kf = BubbleKalman((100, 100), 10)
# Initial prediction
kf.correct(np.array([[12.3]], dtype=np.float32))
kf.correct(np.array([[10]], dtype=np.float32))
kf.correct(np.array([[9]], dtype=np.float32))

# returns [[r]
           #[dr]]



circles = list()
kalman_filters = list()

video = cv.VideoCapture(os.path.join(os.path.dirname(__file__), '../static/sample_bubble_video.mp4'))
#sample_bubble_video
frame_start = 225
frame_end = 410

# video = cv.VideoCapture(os.path.join(os.path.dirname(__file__), '../static/sample_bubble_video_unstable.mp4'))
# # # sample_bubble_video_unstable
# frame_start = 0
# frame_end = 700

fps = video.get(cv.CAP_PROP_FPS)
ret, frame = video.read()
t0 = 0
scale_height = .55
scale_width = .55

# scale first frame to start video writing
frame = cv.resize(frame, (0, 0), fx=scale_width, fy=scale_height)
h, w = frame.shape[:2]

# start writing video
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter("output.avi", fourcc, fps, (w, h))

video.set(cv.CAP_PROP_POS_FRAMES, frame_start)

def nothing(val):
    pass

cv.namedWindow("Circle Detection")
cv.createTrackbar("thresh_val", "Circle Detection", 79, 255, nothing)
cv.createTrackbar("max_val", "Circle Detection",70, 255, nothing)
cv.createTrackbar("blur", "Circle Detection", 5, 100, nothing)
cv.createTrackbar("adapt_area", "Circle Detection", 60, 100, nothing)
cv.createTrackbar("adapt_c", "Circle Detection", 13, 100, nothing)
cv.createTrackbar("min_area", "Circle Detection", 25, 1000, nothing)

while video.isOpened():
    ret, frame = video.read()

    # trackbar positions
    thresh_val = cv.getTrackbarPos("thresh_val", "Circle Detection")
    max_val = cv.getTrackbarPos("max_val", "Circle Detection")
    blur = cv.getTrackbarPos("blur", "Circle Detection")
    if blur % 2 == 0:
        blur += 1
    adapt_area = cv.getTrackbarPos("adapt_area", "Circle Detection")
    if adapt_area % 2 == 0:
        adapt_area += 1
    adapt_c = cv.getTrackbarPos("adapt_c", "Circle Detection")
    min_area = cv.getTrackbarPos("min_area", "Circle Detection")

    # restart video
    if video.get(cv.CAP_PROP_POS_FRAMES) == frame_end:
        break
        print(f"blur:{blur}")
        print(f"adapt_area:{adapt_area}")
        print(f"adapt_c:{adapt_c}")
        print(f"min_area:{min_area}")
        video.set(cv.CAP_PROP_POS_FRAMES, frame_start)

    detected_idxs = list()

    # skip “black” frames
    h, w = frame.shape[:2]
    if not np.array_equal(frame[h//2, w//2], [0,0,0]):


        # resize and recalc frame shape
        frame = cv.resize(frame, (0, 0), fx=scale_width, fy=scale_height)
        # frame = frame[0:50, 600:650]
        h, w = frame.shape[:2]

        # contouring filters
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(gray, (blur, blur), 0)
        gray = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, adapt_area, adapt_c)

        # countour detection
        contours, _ = cv.findContours(gray, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for contour in contours:

            # Approximate the contour to a polygon
            perimeter = cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, 0.03 * perimeter, True)
        
            # Get the area of the (potentially irregular) contour
            area = cv.contourArea(contour)
            
            # filters out small circles
            if area < min_area:
                continue
        
            # Calculate circularity, ratio of the contour area to the smallest enclosing circle area
            (x, y), r = cv.minEnclosingCircle(contour)
            circle_area = np.pi * (r ** 2)

            if circle_area > 0:
                circularity = area/circle_area
            else:
                circularity = 0
            
            # checks number of points in countour (approx) and circularity (good if close to 1)
            if len(approx) > 4 and circularity > 0.7:
                
                # x = round(x)
                # y = round(y)
                center = (int(x), int(y))
                r = round(r, 2)
                cv.circle(frame, center, int(r), (255, 0, 255), 2)
                cv.circle(frame, center, 2, (0, 255, 0), 1)
                
                # on first frame populate circles
                if video.get(cv.CAP_PROP_POS_FRAMES) == frame_start + 1:
                    # print("FIRST FRAME")
                    circles.append([x, y, [(video.get(cv.CAP_PROP_POS_FRAMES), round(r, 2))]])                    
                    detected_idxs.append(len(circles) - 1)
                    kalman_filters.append(BubbleKalman(x, y, round(r, 2)))
                    kalman_filters[-1].correct(np.array([[r]], dtype=np.float32))

                
                # on all other frames, find matches
                else:
                    circles_np = np.array(circles, dtype=object)
                    subtracted_x = np.abs(circles_np[:, 0] - np.full(len(circles_np[:, 0]), x))
                    subtracted_y = np.abs(circles_np[:, 1] - np.full(len(circles_np[:, 1]), y))
                    
                    err = 5
                    closest_idx_x = np.where(subtracted_x < err)
                    closest_idx_y = np.where(subtracted_y < err)
                    closest_idx = np.intersect1d(closest_idx_x, closest_idx_y)
                    
                    # no match found, need to create a new circle list
                    if closest_idx.size == 0:
                        # print("MATCH NOT FOUND")
                        circles.append([round(x), round(y), [(video.get(cv.CAP_PROP_POS_FRAMES), round(r, 2))]])
                        kalman_filters.append(BubbleKalman(x, y, round(r, 2)))
                        kalman_filters[-1].correct(np.array([[r]], dtype=np.float32))
                        detected_idxs.append(len(circles) - 1)

                    # match found, update bucket
                    else:
                        # print(f"MATCH FOUND, closest index: {closest_idx}")
                        circles[closest_idx[0]][2].append((video.get(cv.CAP_PROP_POS_FRAMES), r))
                        detected_idxs.append(closest_idx[0])
                        kalman_filters[closest_idx[0]].correct(np.array([[r]], dtype=np.float32))


        # find circles that haven't been recognized
        found_idxs = np.zeros(len(circles), dtype=bool)
        found_idxs[detected_idxs] = True
        missing_idxs = np.where(found_idxs == False)[0]
        # print(f"frame: {video.get(cv.CAP_PROP_POS_FRAMES)}, missing ids: {missing_idxs}")
        if missing_idxs.size > 0:
            for i in missing_idxs:
                prediction = kalman_filters[i].predict()[0][0]
                circles[i][2].append((video.get(cv.CAP_PROP_POS_FRAMES), round(float(prediction), 2), "estimated"))

        # calculate fps
        real_fps = 1/(perf_counter()-t0)
        fps_text = f"FPS: {int(real_fps)}"
        cv.putText(frame, fps_text, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)
        t0 = perf_counter()

        out.write(frame)
        cv.imshow("Circle Detection", frame)
        cv.imshow("Filtered image", gray)
    # break on esc
    if cv.waitKey(1) & 0xFF == 27:
        break
    # if video.get(cv.CAP_PROP_POS_FRAMES) == frame_start + 1:
    #     break


out.release() 
cv.destroyAllWindows()
print(circles[53])

# graph coordinates for single circle
# x_coords = [pair[0] for pair in circles[0][2]]
# y_coords = [pair[1] for pair in circles[0][2]]

# plt.plot(x_coords, y_coords, 'o')
# plt.title("Radius per Frame of Single Circle")
# plt.xlabel("Frame")
# plt.ylabel("Radius (pixels)")
# plt.show()


# ability to select a bubble/multiple bubbles to track
# kalman filter so you don't lose track of bubbles