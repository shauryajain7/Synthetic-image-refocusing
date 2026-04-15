
"""
Central Configuration Module for Synthetic Image Defocusing
Author: Shaurya Jain
Project: B.Tech Final Year Capstone - Computer Vision & Image Processing
Institution: Manipal Institute of Technology (MIT)
"""

class Config:                     #container (a class) named Config
    # Project Metadata 
    PROJECT_NAME = "Synthetic Image Defocusing"
    VERSION = "2.0.0"
    DEPARTMENT = "Computer Science and Engineering"
    INSTITUTION = "Manipal Institute of Technology"
    
    # AI Model Configuration 
    # Using MiDaS Small for optimized performance on MacBook Air hardware
    MODEL_TYPE = "MiDaS_small"     #tells the AI to use the "small" version of the MiDaS model
    MODEL_REPO = "intel-isl/MiDaS" #exact internet location (repository) where PyTorch will download the AI from
    TRANSFORM_TYPE = "transforms"  #helper tool that resizes user images so the AI can understand them
    
    # Rendering Pipeline Settings 
    # These constants define the computational complexity of the layered stitching
    DEFAULT_LAYERS = 15      # it creates 15 layers by default. This balances a good-looking blur with fast processing time
    MIN_LAYERS = 3           # sets the safety limits for the UI sliders so the user can't select 0 layers or 1000 layers
    MAX_LAYERS = 40          
    
    DEFAULT_BLUR = 35        # starting strength of the background blur
    FOCAL_PLANE_DEFAULT = 128 # depth map uses shades from 0 (black/far) to 255 (white/near). 128 is the exact middle point
    
    # Image Processing Constraints 
    # Prevents memory overflows (RAM spikes) when loading 4K or ultra-high-res photos
    MAX_IMAGE_WIDTH = 1080 
    
    # UI Design System (Visual Identity) 
    # Dark Mode Palette for a professional, academic "Dashboard" aesthetic
    BG_COLOR = "#1e272e"      # Deep matte background
    PANEL_COLOR = "#2f3640"   # Secondary grey for widgets
    ACCENT_COLOR = "#00a8ff"  # Technical blue for sliders/highlights
    SUCCESS_COLOR = "#4cd137" # Green for export/save buttons
    WARNING_COLOR = "#fbc531" # Yellow for status updates
    TEXT_COLOR = "#ffffff"    # High-contrast white text
    
    # Pathing & Logging 
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" #rule for how error messages should look if something breaks
    EXPORT_QUALITY = 95       # JPEG/PNG compression quality (0-100)