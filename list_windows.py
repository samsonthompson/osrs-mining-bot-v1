import cv2  # Import OpenCV

def list_video_capture_devices():
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            arr.append(index)
        cap.release()

        index += 1
    return arr

if __name__ == "__main__":
    devices = list_video_capture_devices()
    print("Available video capture devices:", devices)
