#🏋️ KineticAI: Real-Time Form Auditor
KineticAI is a high-performance computer vision application designed to provide real-time biomechanical feedback during physical exercise. By utilizing neural pose estimation and coordinate geometry, it transforms a standard webcam into a sophisticated motion analysis tool to ensure optimal form and injury prevention.

#🔬 The Science: Biomechanical Analysis
The core of KineticAI lies in its ability to translate visual pixels into mathematical vectors. To audit a squat, the system monitors the Knee Flexion Angle by identifying three key landmarks: the Hip, Knee, and Ankle.

Analysis Logic Initialization
The system establishes a baseline "Up" state when $\theta > 160^\circ$.Threshold Detection: A successful repetition is registered only when the user breaks parallel, defined as $\theta < 90^\circ$.Feedback Loop: Real-time state management prevents partial-rep counting and provides immediate visual cues.

🏗️ Technical Architecture
Following a structured data flow, the application processes frames with minimal latency:Ingestion: Real-time video stream capture via streamlit-webrtc.Pose Estimation: Processing frames through the MediaPipe BlazePose pipeline (GHUM heavy model).Feature Extraction: Mapping 33 3D-landmark coordinates.Inference Engine: Computing joint angles and validating against biomechanical thresholds.Rendering: Asynchronous UI overlay showing rep counts and corrective feedback.

✨ Key Features

Sub-Millisecond Inference: Optimized for real-time processing using NumPy vectorization.

Dynamic UI Overlay: High-contrast text rendering for visibility during movement.

State Persistence: Robust rep-counting logic that handles varying speeds and slight occlusions.

Web-Native: Fully deployable via Streamlit Cloud for global accessibility.

🛠️ Tech Stack 

Core Engine: Python 3.9+
Computer Vision: MediaPipe, OpenCV
Mathematics: NumPy (Vectorized coordinate geometry)
Web Framework: Streamlit 
Stream Handling: PyAV & Streamlit-WebRTC

📜 License
This project is licensed under the MIT License
