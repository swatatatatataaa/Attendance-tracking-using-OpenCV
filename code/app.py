from Flask import Flask, render_template, request, send_file
import cv2 as cv
import numpy as np
import os
import face_recognition as fr
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def encode_faces(folder):
    list_people_encoded = []

    for filename in os.listdir(folder):
        known_image = fr.load_image_file(os.path.join(folder, filename))
        face_encodings = fr.face_encodings(known_image)

        if face_encodings:
            known_encoding = face_encodings[0]
            list_people_encoded.append((known_encoding, filename))

    return list_people_encoded

def makeAttendanceEntry(name, recognized=True):
    with open('attendance_list.csv','a') as FILE:
        now = datetime.now()
        dtString = now.strftime('%d/%b/%Y, %H:%M:%S')
        if recognized:
            FILE.write(f'\n{name},{dtString},Present')
        else:
            FILE.write(f'\n{name},{dtString},Absent')

def find_target_face(target_image):
    face_locations = fr.face_locations(target_image)
    recognized_faces = []

    # Recognize faces in the target photo
    for face_location in face_locations:
        encode_face = fr.face_encodings(target_image, known_face_locations=[face_location])[0]

        for person in encode_faces('people1/'):
            known_encoding = person[0]
            filename = person[1]

            is_target_face = fr.compare_faces([known_encoding], encode_face, tolerance=0.55)

            if any(is_target_face):
                recognized_faces.append(filename)

    # Mark attendance for recognized faces
    for filename in recognized_faces:
        label = filename
        label = label.split('.')[0]
        makeAttendanceEntry(label, recognized=True)

    # Mark attendance as absent for faces not recognized in the target photo
    all_faces = [filename for _, filename in encode_faces('people1/')]
    unrecognized_faces = list(set(all_faces) - set(recognized_faces))
    for filename in unrecognized_faces:
        label = filename
        label = label.split('.')[0]
        makeAttendanceEntry(label, recognized=False)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    # Load the uploaded image using face_recognition
    nparr = np.fromstring(file.read(), np.uint8)
    target_image = cv.imdecode(nparr, cv.IMREAD_COLOR)
    
    # Call the find_target_face function
    find_target_face(target_image)

    # Render the result image
    cv.imwrite('result.jpg', target_image)
    return send_file('result.jpg', mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
