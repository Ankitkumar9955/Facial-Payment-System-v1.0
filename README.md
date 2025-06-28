# Face Pay - Facial Recognition Payment System

A Python-based prototype of a secure facial recognition payment system that simulates a complete payment flow using face authentication and PIN verification.

## 🚀 Features

- **Face Recognition**: Real-time face detection and recognition using OpenCV and face_recognition libraries
- **PIN Verification**: Secure 4-6 digit PIN validation with SHA-256 hashing
- **Modern GUI**: Beautiful Tkinter-based interface with intuitive user experience
- **User Management**: Easy registration and management of users
- **Security**: Face encodings and PINs stored securely in local files
- **Simulation**: Complete payment flow simulation without real UPI integration

## 📁 Project Structure

```
face_pay/
├── main.py                 # Main application entry point
├── face_recognition_module.py  # Face detection and recognition
├── pin_verification.py     # PIN validation and security
├── gui.py                  # Tkinter GUI interface
├── register_user.py        # Standalone user registration script
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── data/                  # Data storage directory
    ├── faces.pkl          # Face encodings (auto-generated)
    └── pin_data.json      # PIN data (auto-generated)
```

## 🛠️ Installation

### Prerequisites

- Python 3.7 or higher
- Webcam for face recognition
- Windows/Linux/macOS

### Setup

1. **Clone or download the project**
   ```bash
   cd face_pay
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## 🎯 Usage

### Main Application

1. **Start the application**
   ```bash
   python main.py
   ```

2. **Register a new user** (if needed)
   - Click "Register User" button
   - Enter your name
   - Look at the camera and press 'R' to capture your face
   - Enter a 4-6 digit PIN

3. **Make a payment**
   - Click "Start Face Scan"
   - Look at the camera for recognition
   - Press 'C' to confirm when recognized
   - Enter your PIN
   - Click "Verify & Pay"

### User Registration Script

For advanced user management, use the standalone registration script:

```bash
python register_user.py
```

This provides options to:
- Register new users
- List all registered users
- Remove users
- Change PINs

## 🔧 Technical Details

### Face Recognition
- Uses OpenCV for camera capture
- face_recognition library for face detection and encoding
- Stores face encodings in `data/faces.pkl`
- Supports real-time recognition with confidence scoring

### PIN Security
- SHA-256 hashing with salt
- 4-6 digit PIN validation
- Stored securely in `data/pin_data.json`
- No plain text storage

### GUI Features
- Modern dark theme
- Real-time status updates
- Thread-safe face recognition
- Intuitive button layout
- Success/error feedback

## 🎨 Screenshots

The application features:
- Clean, modern interface
- Real-time face recognition window
- PIN entry with masked input
- Success/error message display
- User-friendly registration process

## 🔒 Security Features

- **Face Encoding**: Biometric data stored as numerical encodings
- **PIN Hashing**: Passwords hashed with SHA-256 and salt
- **Local Storage**: All data stored locally on your machine
- **No Network**: No external API calls or data transmission

## 🚨 Important Notes

- This is a **prototype/simulation** only
- No real payment processing
- No actual UPI integration
- Face data and PINs stored locally
- Requires webcam for functionality

## 🐛 Troubleshooting

### Common Issues

1. **Camera not working**
   - Ensure webcam is connected and not in use by other applications
   - Check camera permissions

2. **Face recognition not working**
   - Ensure good lighting
   - Face should be clearly visible
   - Try registering face again

3. **Dependencies issues**
   - Update pip: `pip install --upgrade pip`
   - Install Visual C++ build tools (Windows)
   - Use conda for easier installation

### Installation Troubleshooting

**Windows:**
```bash
pip install cmake
pip install dlib
pip install -r requirements.txt
```

**Linux/macOS:**
```bash
sudo apt-get install cmake  # Ubuntu/Debian
brew install cmake          # macOS
pip install -r requirements.txt
```

## 🤝 Contributing

This is a prototype project. Feel free to:
- Report bugs
- Suggest improvements
- Add new features
- Improve documentation

## 📄 License

This project is for educational and demonstration purposes.

## 🙏 Acknowledgments

- OpenCV for computer vision capabilities
- face_recognition library for face detection
- Tkinter for GUI framework
- Python community for excellent libraries

---

**Note**: This system is designed for educational purposes and demonstrates the concept of facial recognition payment systems. It does not implement actual payment processing or real-world security measures. 