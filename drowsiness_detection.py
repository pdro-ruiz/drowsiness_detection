import cv2
import numpy as np
import dlib
from imutils import face_utils
from colorama import Fore, Style
import pygame
import os
import time

# Initialize pygame and alarms
pygame.mixer.init()

SLEEP_ALARM_PATH = "sounds/sleep_alarm.mp3"
YAWN_ALARM_PATH = "sounds/drowsy_alarm.mp3"
PREDICTOR_PATH = "data/shape_predictor_68_face_landmarks.dat"
EAR_THRESHOLD = 0.25
YAWN_THRESHOLD = 0.7
EYE_CLOSED_DURATION = 2  # seconds
ALARM_DISPLAY_DURATION = 5  # seconds

try:
    sleep_alarm = pygame.mixer.Sound(SLEEP_ALARM_PATH)
    yawn_alarm = pygame.mixer.Sound(YAWN_ALARM_PATH)
except pygame.error as e:
    raise FileNotFoundError(f"Error loading sound files: {e}")

# Verify that the predictor file exists
if not os.path.isfile(PREDICTOR_PATH):
    raise FileNotFoundError(f"The file {PREDICTOR_PATH} was not found. Make sure it is in the correct path.")

# Initialize the camera and capture instance
cap = cv2.VideoCapture(0)

# Initialize face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)

# Initial state
sleep = 0
yawn = 0
status = "All good!"
color = (0, 255, 0)
last_alarm_time = 0  # Timestamp of the last alarm
eye_closed_start = None  # Timestamp when eyes close
alarm_display_start = 0  # Timestamp to display the alarm

def compute(ptA, ptB):
    """Calculates the Euclidean distance between two points."""
    return np.linalg.norm(ptA - ptB)

def blinked(a, b, c, d, e, f):
    """
    Calculates the eye aspect ratio (EAR) to determine if the eye is closed.
    
    Args:
        a, b, c, d, e, f (tuple): Coordinates of the eye landmarks.
        
    Returns:
        int: 0 if the eye is closed, 1 if it is blinking, 2 if it is open.
    """
    up = compute(b, d) + compute(c, e)
    down = compute(a, f)
    ratio = up / (2.0 * down)
    if ratio > EAR_THRESHOLD:
        return 2
    elif ratio > 0.21 and ratio <= EAR_THRESHOLD:
        return 1
    else:
        return 0

def mouth_aspect_ratio(mouth):
    """
    Calculates the mouth aspect ratio (MAR) to determine if the mouth is open (yawn).
    
    Args:
        mouth (list): Coordinates of the mouth landmarks.
        
    Returns:
        float: Mouth aspect ratio.
    """
    A = compute(mouth[2], mouth[10])
    B = compute(mouth[4], mouth[8])
    C = compute(mouth[0], mouth[6])
    return (A + B) / (2.0 * C)

def play_alarm(alarm):
    """Plays an alarm if it has not been played recently."""
    global last_alarm_time
    current_time = time.time()
    if current_time - last_alarm_time > ALARM_DISPLAY_DURATION:
        pygame.mixer.Sound.play(alarm)
        last_alarm_time = current_time

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for face in faces:
        x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
        face_frame = frame.copy()
        cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        landmarks = predictor(gray, face)
        landmarks = face_utils.shape_to_np(landmarks)

        left_blink = blinked(landmarks[36], landmarks[37], landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right_blink = blinked(landmarks[42], landmarks[43], landmarks[44], landmarks[47], landmarks[46], landmarks[45])

        mouth = landmarks[48:68]
        mar = mouth_aspect_ratio(mouth)

        current_time = time.time()

        # Detection of closed eyes for more than 2 seconds
        if left_blink == 0 or right_blink == 0:
            if eye_closed_start is None:
                eye_closed_start = current_time
            elif current_time - eye_closed_start > EYE_CLOSED_DURATION:
                if status != "Danger! Serious signs of fatigue in your driving.":
                    play_alarm(sleep_alarm)
                    print(Fore.RED + Style.BRIGHT + "Attention! Serious signs of fatigue have been detected in your driving. Please consider stopping in a safe place and taking a break." + Style.RESET_ALL)
                    status = "Danger! Serious signs of fatigue in your driving."
                    color = (255, 0, 0)
                    alarm_display_start = current_time
        else:
            eye_closed_start = None

        # Detection of yawns
        if mar > YAWN_THRESHOLD:
            yawn += 1
            if yawn >= 1:
                if status != "Yawn detected. Please be alert.":
                    play_alarm(yawn_alarm)
                    print(Fore.RED + Style.BRIGHT + "Yawn detected. Please be alert and stop in case of fatigue." + Style.RESET_ALL)
                    status = "Yawn detected. Please be alert."
                    color = (0, 0, 255)
                    alarm_display_start = current_time
        else:
            yawn = 0  # Reset yawn counter if no yawn is detected

        # Reset status if no condition is detected
        if current_time - alarm_display_start > ALARM_DISPLAY_DURATION:
            if not (left_blink == 0 or right_blink == 0 or mar > YAWN_THRESHOLD):
                status = "All good!"
                color = (0, 255, 0)

        cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        for (x, y) in landmarks:
            cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)

    cv2.imshow("Frame", frame)
    cv2.imshow("Result of detector", face_frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
        break

cap.release()
cv2.destroyAllWindows()
