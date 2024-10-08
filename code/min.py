#  https://www.youtube.com/watch?v=bhlk2a1VCD0
import csv
import face_recognition as fr
import cv2 as cv
import os
#from tkinter import Tk
#Tk().withdraw()

img = fr.load_image_file('images/ma_and_elon.jpeg')

enc = fr.face_encodings(img)

def encode_face(folder) :
    encoding_list = []

    for filename in os.listdir(folder) :
        known_img = fr.load_image_file(f'{folder}{filename}')
        known_enc = fr.face_encodings(known_img)[0]
        encoding_list.append((known_enc,filename))

    return encoding_list

def find_face() :
    face_loc = fr.face_locations(img)

    for person in encode_face('images/') :
        enc_face = person[0]
        filename = person[1] 

        is_target_face = fr.compare_faces(enc_face,enc,tolerance=0.6)
        print(f'{is_target_face} {filename}')

        if face_loc:
            face_no = 0
            for location in face_loc :
                if is_target_face[face_no] :
                    label = filename
                    create_frame(location,label)
                face_no += 1

def create_frame(location,label) :
    top,right,bottom,left = location

    label = label.replace('.png','')
    label = label.replace('.jpg','')
    label = label.replace('.jpeg','')

    # # change start
    # with open('recognized_faces.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(['Recognized Faces'])
    #     writer.writerow([label])
    # # change end
    
    cv.rectangle(img,(left,top),(right,bottom),(26, 237, 30),2)
    cv.rectangle(img,(left,bottom+20),(right,bottom),(26, 237, 30),-1)
    cv.putText(img,label,(left+3,bottom+14),cv.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
    print(label + ' is present in photo')

def render_image() :
    rgb_img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
    cv.imshow('Face Recognition',rgb_img)
    cv.waitKey(0)

find_face()
render_image()

# with open('recognized_faces.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Recognized Faces'])
#     for face in recognized_faces:
#         writer.writerow([face])