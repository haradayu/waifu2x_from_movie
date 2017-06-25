#coding=utf-8
import numpy as np
import cv2
import hashlib

cap = cv2.VideoCapture('./testsisters.mp4')

result = "./output.avi" 
fps    = cap.get(cv2.cv.CV_CAP_PROP_FPS)
height = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
width  = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
# fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
fourcc = cv2.cv.CV_FOURCC('D','I','V','X')
out = cv2.VideoWriter(result,fourcc, fps, (int(width), int(height)))

end_frame = cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
previous_frame = 1000
index = 0
BUFFER_SIZE = 10
write_frame = 0
while(cap.isOpened()):
    saved_frame_que = []
    saved_filename_que = []
    while len(saved_frame_que) < BUFFER_SIZE:
        now_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
        if end_frame <= now_frame:
            break
        ret, frame = cap.read()
        print now_frame
        if np.mean(previous_frame - frame) > 10:
            print(np.mean(previous_frame - frame))
            filename = "keyframe/%03d.png" % len(saved_frame_que)
            cv2.imwrite(filename,frame)
            saved_filename_que.append(filename)
            saved_frame_que.append(now_frame)
            previous_frame = frame
    key_frame = saved_frame_que.pop(0)
    key_frame_image = cv2.imread(saved_filename_que.pop(0))
    key_frame = saved_frame_que.pop(0)
    while write_frame < now_frame:
        if key_frame <= write_frame:
            if len(saved_frame_que) == 0:
                key_frame = end_frame
            else:
                key_frame = saved_frame_que.pop(0)
            key_frame_image = cv2.imread(saved_filename_que.pop(0))
        out.write(key_frame_image)
        write_frame += 1
        
    if end_frame <= now_frame:
        break
    # out.write(previous_frame)
    # index += 1

cap.release()
out.release()