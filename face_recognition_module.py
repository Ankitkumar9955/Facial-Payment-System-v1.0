#!/usr/bin/env python3
"""
Face Recognition Module for Face Pay
Handles face registration, encoding, and recognition
"""

import cv2
import face_recognition
import pickle
import os
import numpy as np
from typing import Dict, List, Tuple, Optional

class FaceRecognitionModule:
    def __init__(self, faces_file: str = "data/faces.pkl"):
        """Initialize the face recognition module"""
        self.faces_file = faces_file
        self.known_face_encodings = []
        self.known_face_names = []
        self.camera = None
        self.load_faces()
    
    def load_faces(self):
        """Load registered faces from pickle file"""
        try:
            if os.path.exists(self.faces_file):
                with open(self.faces_file, 'rb') as f:
                    data = pickle.load(f)
                    self.known_face_encodings = data.get('encodings', [])
                    self.known_face_names = data.get('names', [])
                print(f"✅ Loaded {len(self.known_face_names)} registered faces")
            else:
                print("ℹ️  No registered faces found. Please register users first.")
        except Exception as e:
            print(f"❌ Error loading faces: {e}")
            self.known_face_encodings = []
            self.known_face_names = []
    
    def save_faces(self):
        """Save registered faces to pickle file"""
        try:
            os.makedirs(os.path.dirname(self.faces_file), exist_ok=True)
            data = {
                'encodings': self.known_face_encodings,
                'names': self.known_face_names
            }
            with open(self.faces_file, 'wb') as f:
                pickle.dump(data, f)
            print(f"✅ Saved {len(self.known_face_names)} faces to {self.faces_file}")
        except Exception as e:
            print(f"❌ Error saving faces: {e}")
    
    def register_face(self, name: str) -> bool:
        """Register a new face for the given name"""
        print(f"📸 Registering face for: {name}")
        
        # Initialize camera
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            print("❌ Could not open camera")
            return False
        
        face_detected = False
        face_encoding = None
        
        print("👤 Please look at the camera and press 'R' to register your face...")
        print("Press 'Q' to quit registration")
        
        while True:
            ret, frame = camera.read()
            if not ret:
                print("❌ Failed to capture frame")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Find faces in the frame
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)
            
            # Draw rectangle around detected faces
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, "Face Detected", (left, top - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Show instructions
            cv2.putText(frame, "Press 'R' to Register Face", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'Q' to Quit", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow('Face Registration', frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord('r'):
                if face_encodings:
                    face_encoding = face_encodings[0]
                    face_detected = True
                    print("✅ Face captured successfully!")
                    break
                else:
                    print("❌ No face detected. Please position your face in the camera.")
        
        camera.release()
        cv2.destroyAllWindows()
        
        if face_detected and face_encoding is not None:
            # Check if name already exists
            if name in self.known_face_names:
                # Update existing face
                idx = self.known_face_names.index(name)
                self.known_face_encodings[idx] = face_encoding
                print(f"🔄 Updated face for existing user: {name}")
            else:
                # Add new face
                self.known_face_encodings.append(face_encoding)
                self.known_face_names.append(name)
                print(f"✅ Registered new user: {name}")
            
            self.save_faces()
            return True
        else:
            print("❌ Face registration failed")
            return False
    
    def start_recognition(self) -> Tuple[bool, Optional[str]]:
        """Start face recognition and return (success, user_name)"""
        print("🔍 Starting face recognition...")
        
        # Initialize camera
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            print("❌ Could not open camera")
            return False, None
        
        if not self.known_face_encodings:
            print("❌ No registered faces found")
            self.camera.release()
            return False, None
        
        print("👤 Please look at the camera for recognition...")
        print("Press 'Q' to quit recognition")
        
        while True:
            ret, frame = self.camera.read()
            if not ret:
                print("❌ Failed to capture frame")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Find faces in the frame
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)
            
            # Check each face found in the frame
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Compare with known faces
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.6)
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                
                if True in matches:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = 1 - face_distances[best_match_index]
                        
                        # Draw rectangle and name
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                        cv2.putText(frame, f"{name} ({confidence:.2f})", (left, top - 10), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                        
                        # Show recognition message
                        cv2.putText(frame, f"Recognized: {name}", (10, 30), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        cv2.putText(frame, "Press 'C' to Confirm", (10, 60), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                        
                        cv2.imshow('Face Recognition', frame)
                        
                        key = cv2.waitKey(1) & 0xFF
                        if key == ord('c'):
                            self.camera.release()
                            cv2.destroyAllWindows()
                            print(f"✅ Face recognized: {name}")
                            return True, name
                        elif key == ord('q'):
                            self.camera.release()
                            cv2.destroyAllWindows()
                            return False, None
                else:
                    # Unknown face
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.putText(frame, "Unknown", (left, top - 10), 
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
        return self.known_face_names.copy() 