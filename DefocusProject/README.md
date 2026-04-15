# Synthetic Image Defocusing

[cite_start]**A B.Tech Final Year Project in Computer Vision and Image Processing** [cite: 2, 21]

[cite_start]**Submitted by:** Shaurya Jain (Reg No. 220905032) [cite: 5, 6]  
[cite_start]**Under the Guidance of:** Dr. Radhika Kamath, Associate Professor [cite: 8, 9]  
[cite_start]**Institution:** Department of Computer Science and Engineering, Manipal Institute of Technology (MIT), MAHE [cite: 1, 10, 11]  

---

## 📖 Project Overview
[cite_start]Digital image processing and computer vision have revolutionized how we interact with visual data[cite: 14]. [cite_start]Traditionally, achieving a professional "portrait effect" or "bokeh" (where the subject is sharp and the background is blurred) required expensive dual-lens cameras or specialized LiDAR hardware[cite: 16, 29]. 

[cite_start]This project provides a software-only solution[cite: 30]. [cite_start]Utilizing Artificial Intelligence and Monocular Depth Estimation [cite: 17, 33][cite_start], this application processes standard 2D images (JPEG/PNG) [cite: 39] to mathematically simulate physical lens blur. [cite_start]Users can interactively click anywhere on an image to dynamically shift the focal plane[cite: 34].

## ✨ Key Advanced Features
* [cite_start]**Monocular Depth Estimation:** Utilizes a Convolutional Neural Network (PyTorch/MiDaS) to generate 3D depth maps from flat 2D images without extra sensors[cite: 33, 40, 41].
* **Edge-Preserving Refinement:** Implements OpenCV Bilateral Filtering to smooth depth maps while strictly preserving the sharp edges of foreground subjects.
* **Dynamic Depth of Field (DoF):** Replaces basic hard-cutoff blending with a mathematical alpha-blending gradient matrix. [cite_start]Blur radius dynamically scales based on the exact absolute distance from the user-selected focal plane[cite: 35].
* [cite_start]**Interactive GUI:** A custom-built Tkinter desktop interface for seamless image uploading, asynchronous processing, interactive "click-to-focus" mapping, and file exporting[cite: 36].

---

## 🏗️ System Architecture
The codebase strictly follows Object-Oriented Programming (OOP) principles, dividing the application into modular components for scalability and memory management.

```text
DefocusProject/
│
├── core/
│   ├── blur_engine.py       # Algorithmic image processing & NumPy matrix math
│   └── depth_estimator.py   # AI Engine handling PyTorch model & inferences
│
├── ui/
│   └── main_window.py       # Tkinter UI, event loop, and canvas coordinate mapping
│
├── app.py                   # Main application entry point
└── README.md