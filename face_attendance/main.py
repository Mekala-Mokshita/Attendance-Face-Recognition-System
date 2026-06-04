import cv2
import face_recognition
import pickle
import numpy as np
import sqlite3
from datetime import datetime

# =========================
# Attendance Function
# =========================

def mark_attendance(name):

    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M:%S")

    conn = sqlite3.connect("attendance.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM attendance WHERE name=? AND date=?",
        (name, today)
    )

    record = cursor.fetchone()

    if record is None:

        cursor.execute(
            "INSERT INTO attendance(name,time,date) VALUES(?,?,?)",
            (name, now, today)
        )

        conn.commit()

        print(f"Attendance marked for {name}")

    conn.close()


# =========================
# Load Encodings
# =========================

with open("encodings.pkl", "rb") as f:

    data = pickle.load(f)

known_encodings = data["encodings"]
known_names = data["names"]

# Avoid duplicate marking during current run

marked_today = set()

# =========================
# Start Webcam
# =========================

cam = cv2.VideoCapture(0)

while True:

    ret, frame = cam.read()

    if not ret:
        print("Could not access webcam")
        break

    # Resize for faster recognition

    small_frame = cv2.resize(
        frame,
        (0, 0),
        fx=0.25,
        fy=0.25
    )

    rgb_small = cv2.cvtColor(
        small_frame,
        cv2.COLOR_BGR2RGB
    )

    # Detect faces

    face_locations = face_recognition.face_locations(
        rgb_small
    )

    face_encodings = face_recognition.face_encodings(
        rgb_small,
        face_locations
    )

    # Process each face

    for (top, right, bottom, left), face_encoding in zip(
        face_locations,
        face_encodings
    ):

        name = "Unknown"

        matches = face_recognition.compare_faces(
            known_encodings,
            face_encoding
        )

        face_distances = face_recognition.face_distance(
            known_encodings,
            face_encoding
        )

        if len(face_distances) > 0:

            best_match_index = np.argmin(
                face_distances
            )

            confidence = (
                1 - face_distances[best_match_index]
            )

            if (
                matches[best_match_index]
                and confidence > 0.50
            ):

                name = known_names[
                    best_match_index
                ]

                if name not in marked_today:

                    mark_attendance(name)

                    marked_today.add(name)

        # Scale back coordinates

        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw Rectangle

        cv2.rectangle(
            frame,
            (left, top),
            (right, bottom),
            (0, 255, 0),
            2
        )

        # Display Name

        cv2.putText(
            frame,
            name,
            (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.imshow(
        "Face Recognition Attendance System",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()

cv2.destroyAllWindows()