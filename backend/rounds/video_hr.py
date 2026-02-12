# rounds/video_hr.py

import cv2
import time


def video_hr_round(duration=30):
    """
    Runs video HR round for given duration (seconds).
    Returns confidence score based on face presence.
    """

    print("\n=== HR Video Round Started ===")
    print("Camera will run for", duration, "seconds.")
    print("Maintain eye contact and confidence.")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Could not access webcam.")
        return {"confidence_score": 0, "feedback": "Camera not accessible"}

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    start_time = time.time()
    frames_with_face = 0
    total_frames = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        total_frames += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        if len(faces) > 0:
            frames_with_face += 1

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.putText(
            frame,
            "HR Video Round - Confidence Analysis",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.imshow("AI Interview - HR Round", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        if time.time() - start_time > duration:
            break

    cap.release()
    cv2.destroyAllWindows()

    if total_frames == 0:
        confidence = 0
    else:
        confidence = round((frames_with_face / total_frames) * 10, 2)

    if confidence > 7:
        feedback = "Excellent eye contact and presence."
    elif confidence > 4:
        feedback = "Moderate confidence level."
    else:
        feedback = "Low presence detected. Improve posture and eye contact."

    return {
        "confidence_score": confidence,
        "feedback": feedback
    }
