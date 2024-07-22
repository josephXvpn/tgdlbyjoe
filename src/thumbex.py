import cv2

def extract_thumbnail(video_path, frame_number, thumbnail_path):
    video_capture = cv2.VideoCapture(video_path)
    if not video_capture.isOpened():
        print("Error: Unable to open video file.")
        return
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
    success, frame = video_capture.read()
    if not success:
        print("Error: Unable to read frame.")
        return
    cv2.imwrite(thumbnail_path, frame)
    video_capture.release()
