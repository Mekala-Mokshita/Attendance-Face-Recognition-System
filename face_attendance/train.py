import face_recognition
import os
import pickle

known_encodings = []
known_names = []

for person in os.listdir("known_faces"):
    person_folder = os.path.join("known_faces", person)

    if not os.path.isdir(person_folder):
        continue

    for image_name in os.listdir(person_folder):
        image_path = os.path.join(person_folder, image_name)

        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)

        if len(encodings) > 0:
            known_encodings.append(encodings[0])
            known_names.append(person)

print("Faces encoded:", len(known_encodings))

with open("encodings.pkl", "wb") as f:
    pickle.dump(
        {
            "encodings": known_encodings,
            "names": known_names
        },
        f
    )

print("Training completed!")