import cv2 as cv
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
import face_recognition as fr
from datetime import datetime

Tk().withdraw
load_image = askopenfilename()

target_image  = fr.load_image_file(load_image)
target_encoding = fr.face_encodings(target_image)

def encode_faces(folder):
    list_people_encoded = []

    for filename in os.listdir(folder):
        known_image = fr.load_image_file(f'{folder}{filename}')
        face_encodings = fr.face_encodings(known_image)

        if face_encodings:
            known_encoding = face_encodings[0]
            list_people_encoded.append((known_encoding,filename))

    return list_people_encoded



#EDIT 2 
def makeAttendanceEntry(name, present):
    with open('C:/Users/rawat/OneDrive/Desktop/minor_2/attendance_list.csv', 'r+') as FILE:
        allLines = FILE.readlines()
        attendanceList = []
        for line in allLines:
            entry = line.split(',')
            attendanceList.append(entry[0])

        if name not in attendanceList:
            now = datetime.now()
            dtString = now.strftime('%d/%b/%Y, %H:%M:%S')
            if present:
                FILE.writelines(f'\n{name},Present,{dtString}')  
            else:
                FILE.writelines(f'\n{name},Absent,{dtString}')  




def find_target_face():
    face_location = fr.face_locations(target_image)

    for person in encode_faces('C:/Users/rawat/OneDrive/Desktop/minor_2/people1/'):
        encode_face = person[0]
        filename = person[1]

        is_target_face = fr.compare_faces(encode_face, target_encoding, tolerance=0.55)
        print(f'{is_target_face} {filename}')

        if face_location:
            face_number = 0
            for location in face_location:
                if face_number < len(is_target_face):  
                    if is_target_face[face_number]:
                        label = filename.replace('.png', '').replace('.jpg', '').replace('.jpeg', '')
                        create_frame(location, label)
                        makeAttendanceEntry(label, True)
                    else:
                        label = filename.replace('.png', '').replace('.jpg', '').replace('.jpeg', '')
                        makeAttendanceEntry(label, False)
                else:
                    label = filename.replace('.png', '').replace('.jpg', '').replace('.jpeg', '')
                    makeAttendanceEntry(label, False)

                face_number += 1



def create_frame(location,label):
    top , right, bottom , left = location

    cv.rectangle(target_image, (left,top), (right,bottom),(255,0,0), 2)
    cv.rectangle(target_image, (left,bottom +20), (right,bottom),(255,0,0), cv.FILLED)
    cv.putText(target_image, label, (left+3, bottom+14 ), cv.FONT_HERSHEY_DUPLEX, 0.4 , (255,255,255) , 1)


def render_image():
    rgb_img = cv.cvtColor(target_image, cv.COLOR_BGR2RGB)
    cv.imshow('Face Recognition' , rgb_img)
    cv.waitKey(0)



find_target_face()
render_image()
    





