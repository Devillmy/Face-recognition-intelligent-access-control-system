import cv2
import time
import signal  
import atexit
import numpy as np
import face_recognition
import RPi.GPIO as GPIO
from oled import song_oled

try:
    song_oled("初始化00")
except:
    print("初始化错误")

atexit.register(GPIO.cleanup)   
  
servopin = 21  
GPIO.setmode(GPIO.BCM)  
GPIO.setup(servopin, GPIO.OUT, initial=False)  
p = GPIO.PWM(servopin,50) #50HZ  
p.start(0)  
time.sleep(2)  
  
def opendoor():

    for i in range(0,181,10):  
        p.ChangeDutyCycle(5 + 10 * i / 180) #设置转动角度  
        time.sleep(0.02)                      #等该20ms周期结束  
        p.ChangeDutyCycle(0)    #归零信号 
        time.sleep(0.1)                   
    time.sleep(3)  

    for i in range(181,0,-10):  
        p.ChangeDutyCycle(5 + 10 * i / 180)  
        time.sleep(0.02)  
        p.ChangeDutyCycle(0)  
        time.sleep(0.1)  

video_capture = cv2.VideoCapture(0)

try:
    song_oled("初始化30")
except:
    print("初始化错误")

#宿舍的人脸
#李洪涛 孟朝阳 刘佳昊 殷周涛 汪大烜 王林 张存杰 石海波
lht_image = face_recognition.load_image_file("face_hub/lht.png") 
#mzy_image = face_recognition.load_image_file("face_hub/mzy.jpg")


#人脸编码
lht_face_encoding = face_recognition.face_encodings(lht_image)[0]
#mzy_face_encoding = face_recognition.face_encodings(mzy_image)[0]



# 创建一个数组对应他们的名字
known_face_encodings = [
    lht_face_encoding,
    #mzy_face_encoding,

]
known_face_names = [
    "Li Hongtao",
    #"Meng Zhaoyang",

]


face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
try:
    song_oled("初始化50")
except:
    print("初始化错误")

while True:

    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    if process_this_frame:
   
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:

            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                
                if name == "Li Hongtao":
                    print("你好 李洪涛大王")
                    try:
                        song_oled("你好 李洪涛")
                    except:
                        print("error")

                    opendoor()
                    time.sleep(4)
                    
                else:
                    print("有陌生人闯入")
                    try:
                        song_oled("有陌生人闯入")
                    except:
                        print("error")
            face_names.append(name)

    process_this_frame = not process_this_frame


    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video_capture.release()
cv2.destroyAllWindows()
