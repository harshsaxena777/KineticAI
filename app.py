import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import mediapipe as mp
import cv2
import numpy as np
import av

# --- ARCHITECTURE ---
# 1. Capture Frame -> 2. MediaPipe Pose Detection -> 3. Coordinate Extraction -> 4. Trigonometric Analysis -> 5. UI Overlay

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

class PoseProcessor(VideoProcessorBase):
    def __init__(self):
        self.count = 0
        self.stage = "up"
        self.feedback = "Get Ready!"

    def calculate_angle(self, a, b, c):
        a = np.array(a) # Hip
        b = np.array(b) # Knee
        c = np.array(c) # Ankle
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        return 360-angle if angle > 180 else angle

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
        results = pose.process(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            # Extract Squat Points
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            angle = self.calculate_angle(hip, knee, ankle)
            
            # Logic for Rep Counting
            if angle > 160: self.stage = "up"
            if angle < 90 and self.stage == "up":
                self.stage = "down"
                self.count += 1
                self.feedback = "Perfect Depth!"

            # Draw feedback on frame
            cv2.putText(img, f"Reps: {self.count} | {self.feedback}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
        return av.VideoFrame.from_ndarray(img, format="bgr24")

st.title("🏋️ KineticAI: Form Auditor")
webrtc_streamer(key="pose-checker", video_processor_factory=PoseProcessor)