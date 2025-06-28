#!/usr/bin/env python3
"""
Simple Face Detection Module for Face Pay
Uses OpenCV for basic face detection (fallback when face_recognition is not available)
"""

import cv2
import pickle
import os
import numpy as np
from typing import Dict, List, Tuple, Optional
import time

class SimpleFaceDetection:
    def __init__(self, faces_file: str = "data/faces.pkl"):
        """Initialize the simple face detection module"""
        self.faces_file = faces_file
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.known_faces = {}  # name -> list of face_data (multiple samples)
        self.camera = None
        self.load_faces()
    
    def load_faces(self):
        """Load registered faces from pickle file"""
        try:
            if os.path.exists(self.faces_file):
                with open(self.faces_file, 'rb') as f:
                    self.known_faces = pickle.load(f)
                print(f"✅ Loaded {len(self.known_faces)} registered faces")
            else:
                print("ℹ️  No registered faces found. Please register users first.")
                self.known_faces = {}
        except Exception as e:
            print(f"❌ Error loading faces: {e}")
            self.known_faces = {}
    
    def save_faces(self):
        """Save registered faces to pickle file"""
        try:
            os.makedirs(os.path.dirname(self.faces_file), exist_ok=True)
            with open(self.faces_file, 'wb') as f:
                pickle.dump(self.known_faces, f)
            print(f"✅ Saved {len(self.known_faces)} faces to {self.faces_file}")
        except Exception as e:
            print(f"❌ Error saving faces: {e}")
    
    def extract_face_features(self, face_img):
        """Extract simple features from face image"""
        # Resize to standard size
        face_img = cv2.resize(face_img, (100, 100))
        # Convert to grayscale
        gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        # Flatten and normalize
        features = gray.flatten() / 255.0
        return features
    
    def compare_faces(self, features1, features2, threshold=0.6):
        """Compare two face feature vectors"""
        # Simple correlation-based comparison
        correlation = np.corrcoef(features1, features2)[0, 1]
        return correlation > threshold, correlation
    
    def register_face(self, name: str) -> bool:
        """Register a new face for the given name"""
        print(f"📸 Registering face for: {name}")
        
        # Initialize camera
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            print("❌ Could not open camera")
            return False
        
        face_samples = []
        samples_needed = 3
        current_sample = 0
        
        print(f"👤 Please look at the camera. We need {samples_needed} face samples.")
        print("Press 'R' to capture each sample, 'Q' to quit")
        
        while current_sample < samples_needed:
            ret, frame = camera.read()
            if not ret:
                print("❌ Failed to capture frame")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 3, minSize=(30, 30))
            
            # Draw rectangle around detected faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, "Face Detected", (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Show instructions
            cv2.putText(frame, f"Sample {current_sample + 1}/{samples_needed}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'R' to Capture Sample", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'Q' to Quit", (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow('Face Registration', frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord('r'):
                if len(faces) > 0:
                    # Extract the first detected face
                    x, y, w, h = faces[0]
                    face_img = frame[y:y+h, x:x+w]
                    face_features = self.extract_face_features(face_img)
                    face_samples.append(face_features)
                    current_sample += 1
                    print(f"✅ Captured sample {current_sample}/{samples_needed}")
                    
                    # Add a small delay to avoid capturing the same frame
                    time.sleep(0.5)
                else:
                    print("❌ No face detected. Please position your face in the camera.")
        
        camera.release()
        cv2.destroyAllWindows()
        
        if len(face_samples) == samples_needed:
            # Store face features
            self.known_faces[name] = face_samples
            self.save_faces()
            print(f"✅ Registered new user: {name} with {len(face_samples)} samples")
            return True
        else:
            print("❌ Face registration failed - not enough samples captured")
            return False
    
    def start_recognition(self) -> Tuple[bool, Optional[str]]:
        """Start face recognition and return (success, user_name)"""
        print("🔍 Starting face recognition...")
        
        # Initialize camera
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            print("❌ Could not open camera")
            return False, None
        
        if not self.known_faces:
            print("❌ No registered faces found")
            self.camera.release()
            return False, None
        
        print("👤 Please look at the camera for recognition...")
        print("Press 'C' to confirm when recognized, or 'Q' to quit")
        
        while True:
            ret, frame = self.camera.read()
            if not ret:
                print("❌ Failed to capture frame")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 3, minSize=(30, 30))
            
            # Check each detected face
            for (x, y, w, h) in faces:
                face_img = frame[y:y+h, x:x+w]
                current_features = self.extract_face_features(face_img)
                
                # Compare with known faces
                best_match = None
                best_confidence = 0
                
                for name, known_features_list in self.known_faces.items():
                    # Check against all samples for this user
                    for known_feature in known_features_list:
                        is_match, confidence = self.compare_faces(current_features, known_feature)
                        if is_match and confidence > best_confidence:
                            best_match = name
                            best_confidence = confidence
                
                if best_match:
                    # Draw rectangle and name
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, f"{best_match} ({best_confidence:.2f})", (x, y-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    
                    # Show recognition message
                    cv2.putText(frame, f"Recognized: {best_match}", (10, 30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(frame, f"Confidence: {best_confidence:.2f}", (10, 60), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(frame, "Press 'C' to Confirm", (10, 90), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    
                    cv2.imshow('Face Recognition', frame)
                    
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('c'):
                        self.camera.release()
                        cv2.destroyAllWindows()
                        print(f"✅ Face recognized: {best_match}")
                        return True, best_match
                    elif key == ord('q'):
                        self.camera.release()
                        cv2.destroyAllWindows()
                        return False, None
                else:
                    # Unknown face
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.putText(frame, "Unknown", (x, y-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
            # Show instructions
            cv2.putText(frame, "Press 'Q' to Quit", (10, frame.shape[0] - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow('Face Recognition', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        
        self.camera.release()
        cv2.destroyAllWindows()
        return False, None
    
    def stop_recognition(self):
        """Stop face recognition and release camera"""
        if self.camera:
            self.camera.release()
        cv2.destroyAllWindows()
    
    def get_registered_users(self) -> List[str]:
        """Get list of registered user names"""
        return list(self.known_faces.keys()) 