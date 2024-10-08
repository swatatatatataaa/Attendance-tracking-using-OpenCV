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
                FILE.writelines(f'\n{name},,Present,{dtString}')  # Writing in the Present column
            else:
                FILE.writelines(f'\n{name},Absent,,{dtString}')  # Writing in the Absent column


#1 
def find_target_face():
    face_location = fr.face_locations(target_image)

    for person in encode_faces('C:/Users/rawat/OneDrive/Desktop/minor_2/people1/'):
        encode_face = person[0]
        filename = person[1]

        is_target_face = fr.compare_faces(encode_face,target_encoding,tolerance=0.55)
        print(f'{is_target_face} {filename}')



        if face_location:
            face_number = 0

            for location in face_location:

                if is_target_face[face_number]:
                    label = filename
                    label = label.replace('.png','')
                    label = label.replace('.jpg','')
                    label = label.replace('.jpeg','')
                    create_frame(location,label)
                    makeAttendanceEntry(label,True)
                
                #edit
                else:
                    label = filename
                    label = label.replace('.png','')
                    label = label.replace('.jpg','')
                    label = label.replace('.jpeg','')
                    makeAttendanceEntry(label,False)



                #edit1

                face_number+=1


# def makeAttendanceEntry(name, present):
#     attendance_file_path = 'C:/Users/rawat/OneDrive/Desktop/minor_2/attendance_list.csv'

#     # Read all existing entries
#     with open(attendance_file_path, 'r') as FILE:
#         allLines = FILE.readlines()
    
#     # Append new entry
#     now = datetime.now()
#     dtString = now.strftime('%d/%b/%Y, %H:%M:%S')
#     new_entry = f'\n{name},{"" if present else "Absent"},{"" if present else dtString},{"Present" if present else ""},{dtString if present else ""}'
#     allLines.append(new_entry)

#     # Sort the list alphabetically based on the first element of each line
#     allLines.sort(key=lambda x: x.split(',')[0])

#     # Rewrite the entire file
#     with open(attendance_file_path, 'w') as FILE:
#         FILE.writelines(allLines)


# EDIT 3def find_target_face():
#     face_location = fr.face_locations(target_image)

#     for person in encode_faces('C:/Users/rawat/OneDrive/Desktop/minor_2/people1/'):
#         encode_face = person[0]
#         filename = person[1]

#         is_target_face = fr.compare_faces(encode_face, target_encoding, tolerance=0.55)
#         print(f'{is_target_face} {filename}')

#         if face_location:
#             face_number = 0
#             for location in face_location:
#                 if face_number < len(is_target_face):  # Ensure face_number is within the bounds of is_target_face list
#                     if is_target_face[face_number]:
#                         label = filename.replace('.png', '').replace('.jpg', '').replace('.jpeg', '')
#                         create_frame(location, label)
#                         makeAttendanceEntry(label, True)
#                     else:
#                         label = filename.replace('.png', '').replace('.jpg', '').replace('.jpeg', '')
#                         makeAttendanceEntry(label, False)
#                 else:
#                     # If face number exceeds the length of is_target_face, consider it as not recognized
#                     label = filename.replace('.png', '').replace('.jpg', '').replace('.jpeg', '')
#                     makeAttendanceEntry(label, False)

#                 face_number += 1


# #  EDIT 4 (GIVING MERGED LABEL)Dictionary to store unique labels for each person
# person_labels = {}

# def find_target_face():
#     face_location = fr.face_locations(target_image)

#     for person in encode_faces('C:/Users/rawat/OneDrive/Desktop/minor_2/people1/'):
#         encode_face = person[0]
#         filename = person[1]

#         # Get or assign a label for this person
#         label = person_labels.get(filename)
#         if label is None:
#             label = filename.replace('.png', '').replace('.jpg', '').replace('.jpeg', '')
#             person_labels[filename] = label

#         is_target_face = fr.compare_faces(encode_face, target_encoding, tolerance=0.55)
#         print(f'{is_target_face} {label}')  # Print the label instead of the filename

#         if face_location:
#             face_number = 0
#             for location in face_location:
#                 if face_number < len(is_target_face):  # Ensure face_number is within the bounds of is_target_face list
#                     if is_target_face[face_number]:
#                         create_frame(location, label)
#                         makeAttendanceEntry(label, True)
#                     else:
#                         makeAttendanceEntry(label, False)
#                 else:
#                     makeAttendanceEntry(label, False)

#                 face_number += 1


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
    





