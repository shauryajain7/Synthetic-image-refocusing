import cv2           #OpenCV, Used here to fix colors and clean up the final image
import torch         #PyTorch, This is the massive AI framework ,It handles neural networks
import ssl           #Python sometimes blocks automatic downloads from the internet for security reasons,This helps bypass a specific error
import numpy as np   #to convert the AI's complex brain waves into standard math numbers

class DepthEstimator:
    def __init__(self, model_type="MiDaS_small"):                          #When this starts, it defaults to using MiDaS_small
        """
        Initializes the Depth Estimator by loading the MiDaS model.
        """
        # to fix certificate error during download
        ssl._create_default_https_context = ssl._create_unverified_context
        
        print(f"Initializing AI Engine: Loading {model_type}...")  #Prints a message to the terminal so the user knows the app hasn't frozen
        
        # to load the pre-trained model
        self.model = torch.hub.load("intel-isl/MiDaS", model_type) #It reaches out to the internet, downloads the pre-trained MiDaS AI model,and loads it into your computer's RAM
        self.model.eval() # Set to evaluation mode
        
        # to load transforms to format images for the model (The AI cannot look at standard JPEGs)
        midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
        self.transform = midas_transforms.small_transform

    def estimate_depth(self, image):       
        """
        Takes a BGR image, estimates depth, and applies bilateral 
        filtering for edge preservation.
        """
        # to cnvert BGR (OpenCV default) to RGB for the AI model
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # to apply required transformations
        input_batch = self.transform(img_rgb)
        
        # to predict depth without calculating gradients as saves memory/time
        with torch.no_grad(): #Calculating "gradients" is how AI learns. we tell PyTorch no_grad(). This saves massive amounts of memory and makes the software run 10x faster
            prediction = self.model(input_batch) #We feed the formatted image into the AI. The AI spits out a prediction (a rough, blocky 3D map)
            
            # to resize prediction back to original image resolution
            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=img_rgb.shape[:2],
                mode="bicubic",             #bicubic interpolation
                align_corners=False,
            ).squeeze()
        
        # to convert the PyTorch tensor to a standard numpy array
        depth_map = prediction.cpu().numpy() #The prediction is currently stuck inside PyTorch's specialized memory.this converts it into a standard NumPy array so OpenCV can use it
        
        # to normalize AI decimals to 0-255 for neat visual processing
        depth_map_normalized = cv2.normalize(
            depth_map, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U
        )
        
        # to apply bilateral filter to smooth depth while preserving sharp edges
        refined_depth_map = cv2.bilateralFilter(depth_map_normalized, d=9, sigmaColor=75, sigmaSpace=75)
        
        return refined_depth_map