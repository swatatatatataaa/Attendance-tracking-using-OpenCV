# taken from minor23
# check trial.py for commented / changes made
import cv2 as cv
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
import face_recognition as fr
from datetime import datetime
import pymongo as pm


Tk().withdraw
load_image = askopenfilename()

target_image  = fr.load_image_file(load_image)
target_encoding = fr.face_encodings(target_image)

client = pm.MongoClient("mongodb://localhost:27017")
db = client["minor"]
collection = db["encoded_faces"]

def encode_faces(folder):
    list_people_encoded = []

    for filename in os.listdir(folder):
        known_image = fr.load_image_file(f'{folder}{filename}')
        face_encodings = fr.face_encodings(known_image)

        if face_encodings:
            known_encoding = face_encodings[0]
            list_people_encoded.append((known_encoding,filename))
            collection.insert_one({"encoding": known_encoding.tolist(), "filename": filename})

    return list_people_encoded




def makeAttendanceEntry(name, recognized=True):
    with open('C:/Users/rawat/OneDrive/Desktop/minor_2/attendance_list.csv','r+') as FILE:
        allLines = FILE.readlines()
        attendanceList = []
        for line in allLines:
            entry = line.split(',')
            attendanceList.append(entry[0])
        if name not in attendanceList:
            now = datetime.now()
            dtString = now.strftime('%d/%b/%Y, %H:%M:%S')
            if recognized:
                FILE.writelines(f'\n{name},{dtString},Present')
            else:
                FILE.writelines(f'\n{name},{dtString},Absent')


def find_target_face():
    face_locations = fr.face_locations(target_image)
    recognized_faces = []

    # Recognize faces in the target photo
    for face_location in face_locations:
        encode_face = fr.face_encodings(target_image, known_face_locations=[face_location])[0]

        for person in encode_faces('C:/Users/rawat/OneDrive/Desktop/minor_2/people1/'):
            known_encoding = person[0]
            filename = person[1]

            is_target_face = fr.compare_faces([known_encoding], encode_face, tolerance=0.55)

            if any(is_target_face):
                recognized_faces.append(filename)
                create_frame(face_location, filename.replace('.png', '').replace('.jpg', '').replace('.jpeg', ''))

    # Mark attendance for recognized faces
    for filename in recognized_faces:
        label = filename
        label = label.replace('.png', '')
        label = label.replace('.jpg', '')
        label = label.replace('.jpeg', '')
        makeAttendanceEntry(label, recognized=True)

    # Mark attendance as absent for faces not recognized in the target photo
    all_faces = [filename for _, filename in encode_faces('C:/Users/rawat/OneDrive/Desktop/minor_2/people1/')]
    unrecognized_faces = list(set(all_faces) - set(recognized_faces))
    for filename in unrecognized_faces:
        label = filename
        label = label.replace('.png', '')
        label = label.replace('.jpg', '')
        label = label.replace('.jpeg', '')
        makeAttendanceEntry(label, recognized=False)


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
    





