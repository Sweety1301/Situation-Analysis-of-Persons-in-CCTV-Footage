import cv2 
import time 
import mediapipe as mp 
import pandas as pd 
import math 
# Initialize MediaPipe Pose detector 
mp_pose = mp.solutions.pose 
pose_detector = mp_pose.Pose(min_detection_confidence=0.5, 
min_tracking_confidence=0.5) 
# Function to calculate the angle between two vectors 
def calculate_angle(a, b, c): 
angle = math.atan2(c.y - b.y, c.x - b.x) - math.atan2(a.y - b.y, 
a.x - b.x) 
return abs(angle) * 180.0 / math.pi 
# Function to detect actions based on pose landmarks 
def detect_action(pose_landmarks): 
if pose_landmarks: 
# Get key body landmarks 
nose = pose_landmarks[0]  # Nose 
left_shoulder = pose_landmarks[11]  # Left shoulder 
right_shoulder = pose_landmarks[12]  # Right shoulder 
left_hip = pose_landmarks[23]  # Left hip 
right_hip = pose_landmarks[24]  # Right hip 
left_knee = pose_landmarks[25]  # Left knee 
right_knee = pose_landmarks[26]  # Right knee 
# Calculate angles to determine body posture 
angle_arms = calculate_angle(left_shoulder, nose, 
right_shoulder) 
angle_legs = calculate_angle(left_hip, left_knee, 
right_knee) 
# Define simple conditions to classify actions 
if angle_arms < 50 and angle_legs < 50: 
return "walking"  # When arms and legs show movement 
elif angle_arms > 130 and angle_legs > 130: 
return "sitting"  # Sitting posture (both arms and legs 
form larger angles) 
else: 
return "standing"  # Standing if angles are more neutral 
return "unknown" 
# Process video to detect actions 
def process_video(video_path): 
cap = cv2.VideoCapture(video_path) 
person_id = 0  # Unique ID for each person 
action_data = []  # List to store action data 
prev_actions = {}  # Store previous actions for persons 
start_time = time.time()  # Timer to track action duration 
current_action = None 
while cap.isOpened(): 
ret, frame = cap.read() 
if not ret: 
Break 
# Convert frame to RGB as MediaPipe expects RGB input 
frame_rgb = cv2.cvtColor(frame, 
cv2.COLOR_BGR2RGB) 
# Detect pose landmarks 
results = pose_detector.process(frame_rgb) 
if results.pose_landmarks: 
# For simplicity, assuming 1 person is detected; extend 
logic for multiple persons 
pose = results.pose_landmarks.landmark 
action = detect_action(pose) 
# If action has changed or person is new, reset timer 
if action != current_action: 
current_action = action 
start_time = time.time() 
# Save person action data 
action_data.append({ 
"person_id": person_id, 
"action": action, 
"time": round(time.time() - start_time, 2)  # Time 
spent in current action 
}) 
person_id += 1  # Increment person ID 
cap.release() 
return action_data 
# Save the results to a CSV 
def create_action_dataset(video_path, 
output_csv="action_dataset.csv"): 
output_csv="action_dataset.csv"): 
results = process_video(video_path
