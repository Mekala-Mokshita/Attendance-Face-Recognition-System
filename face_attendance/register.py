import cv2
import os
import subprocess

name = input("Enter Student Name: ")

if not name.strip():
    print("Invalid name!")
    exit()

folder = f"known_faces/{name}"
os.makedirs(folder, exist_ok=True)

cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("Could not access webcam")
    exit()

count = 0

print("\nInstructions:")
print("Press S to save image")
print("Press Q to quit\n")

while True:

    ret, frame = cam.read()

    if not ret:
        print("Could not access webcam")
        break

    cv2.putText(
        frame,
        f"Images Saved: {count}/5",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.imshow(
        "Student Registration",
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    # Save image when S is pressed
    if key == ord("s") or key == ord("S"):

        cv2.imwrite(
            f"{folder}/{count}.jpg",
            frame
        )

        count += 1

        print(f"Saved image {count}")

        if count == 5:
            print("\n5 images captured successfully!")
            break

    # Quit when Q is pressed
    elif key == ord("q") or key == ord("Q"):
        print("\nRegistration cancelled.")
        break

cam.release()
cv2.destroyAllWindows()

print(f"\nRegistration completed for {name}")

# Automatic Training

print("\nTraining faces...")

subprocess.run(
    ["python", "train.py"]
)

print("\nEncodings updated successfully!")
print("Student ready for attendance.")