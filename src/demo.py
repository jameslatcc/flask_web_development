import threading
import time
import cv2

cap = cv2.VideoCapture(0)  # 0 for default camera

def play():
    print('當前play的執行續: ', threading.current_thread())
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Webcam", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
            break
    cap.release()
    cv2.destroyAllWindows()

def print_sec():
    i = 1
    print('當前print_sec的執行續: ', threading.current_thread())
    while i < 10:
        print(" ", i, " seconds")
        i += 1
        time.sleep(1)


if __name__ == "__main__":
    m = threading.Thread(target = play) 
    t = threading.Thread(target = print_sec) 

    m.start()
    t.start()