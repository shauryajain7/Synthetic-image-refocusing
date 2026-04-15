
import cv2 #OpenCV, used here to physically read the image file from your computer's hard drive
import numpy as np
from utils.helpers import resize_with_aspect #Brings in custom tool that shrinks images without making them look squished

class ImageProcessor:
    def __init__(self, depth_engine, blur_engine): #When the processor is created in app.py,it is handed the depth_engine and the blur_engine
        """
        The Processor acts as the orchestrator for the entire pipeline.
        It manages how data flows from the AI to the Rendering Engine.
        """
        self.depth_engine = depth_engine  #saves these engines inside itself so it can call them later
        self.blur_engine = blur_engine

    def run_inference(self, image_path):   #called when the user selects a photo. It receives the string image_path
        """Loads the image and generates the initial depth map."""
        raw_img = cv2.imread(image_path)
        if raw_img is None:
            return None, None
            
        # to standardize resolution for consistent performance
        processed_img = resize_with_aspect(raw_img, width=800)
        
        # call the AI Engine
        depth_map = self.depth_engine.estimate_depth(processed_img)
        
        return processed_img, depth_map

    def apply_defocus(self, image, depth_map, focal_depth, blur_radius, layers): #This is called whenever the user clicks the image or moves a slider
        """Triggers the complex layered rendering algorithm."""
        return self.blur_engine.apply_layered_defocus(
            image, depth_map, focal_depth, blur_radius, layers
        )

        #The processor doesn't do any math here. It just acts as a middleman 
        #It takes all the user's settings and passes them directly to the blur_engine
        #then hands the final beautiful result back to the UI