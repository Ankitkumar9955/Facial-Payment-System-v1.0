# Face Pay – Facial Recognition Based UPI Payment Prototype

A seamless and secure **payment system prototype** using **facial recognition and UPI PIN simulation**. Face Pay enables quick identity verification at merchant counters, where the user’s face becomes their authentication method — followed by a secure PIN entry step.

---

## Project Overview

**Face Pay** simulates a payment flow tailored for **merchant shops**, allowing the seller to enter the amount first. The system then uses **real-time facial recognition** to verify the customer’s identity and proceeds with a **PIN-based confirmation** to simulate a complete payment experience.

This prototype is designed for demonstration, educational purposes, and future integration with real-time payment systems like **UPI**.

---

## ✨ Features

* 🧾 **Amount Entry Interface**: Merchant inputs the amount before scanning begins
* 🎥 **Face Recognition with OpenCV**: Real-time face detection and identification using webcam
* 🔐 **UPI PIN Verification**: Secure PIN entry simulation post face match
* 🖥️ **Interactive GUI**: Clean and intuitive Tkinter interface for all steps
* 💾 **Local Face & PIN Storage**: Data stored securely using `pickle` and JSON
* 📊 **User Feedback**: Real-time messages for transaction success or failure

---

## 🛠️ Tech Stack & Requirements

> **Language**: Python 3.8+

**Libraries Used:**

* `opencv-python`
* `face_recognition`
* `pickle`
* `json`
* `tkinter`
* `os`
* `numpy`

---

## 🔧 Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/face-pay-prototype.git
cd face-pay-prototype

# 2. Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Usage

```bash
python main.py
```

### Workflow:

1. 👨‍💼 Merchant enters the **amount to be paid**
2. 🧠 Face recognition starts automatically via webcam
3. ✅ If face is recognized, user enters their **UPI PIN**
4. 💰 Transaction is **simulated** with a success/failure message

---

## 📁 File Structure

```
face-pay-prototype/
├── data/
│   ├── faces.pkl             # Stored face encodings
│   └── pin_data.json         # User PINs linked to names
├── face_recognition_module.py   # Face registration & recognition logic
├── pin_verification.py          # PIN validation functions
├── gui.py                       # GUI interfaces for amount, face, and PIN
├── register_user.py             # Optional script to register new users
├── main.py                      # Main program flow
├── requirements.txt
└── README.md
```

---

## Screenshots

| 🧾 Amount Entry                                                                                  | 🧠 Face Recognition                                                                                  | 🔐 PIN Verification                                                                           | ✅ Transaction Result                                                                                   |
| ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| ![Amount Entry](https://github.com/user-attachments/assets/897850af-817f-4f6a-a565-825721ab2dd5) | ![Face Recognition](https://github.com/user-attachments/assets/8dd5aa7c-33e8-4a7c-977d-bf45f023370f) | ![PIN Entry](https://github.com/user-attachments/assets/16733d21-8cae-40be-a061-64e069d13101) | ![Transaction Result](https://github.com/user-attachments/assets/7cbbb524-fc0a-424e-82a5-70dba756780f) |

> 💡 *Tip: If screenshots are broken, make sure the GitHub image URLs are publicly accessible or hosted in your repo's `assets` folder.*

---

## ⚠️ Limitations

* 🔒 Real UPI or payment API is **not integrated** (simulation only)
* 🧍 Face recognition accuracy depends on camera quality and lighting
* 🗃️ Data is stored locally — no cloud/database support

---

##  Future Enhancements
* 🔗 Integrate with **actual UPI API** (e.g., PhonePe for Business)
* 🌐 Web-based version using Flask or Streamlit
* 🧠 Add **liveness detection** to prevent spoofing
* 🧾 Generate digital receipts with QR code
* 🧠 Use ML models for fraud detection

---

##  Contributing

We welcome your contributions!
To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-name`)
3. Make your changes
4. Commit and push
5. Create a Pull Request 🚀

---

## 🧾 License

This project is licensed under the **MIT License**.

---

## 📌 Disclaimer

> **Face Pay** is a **proof-of-concept prototype** and does not perform real financial transactions.
> It is meant for **educational and demonstration** purposes only.


