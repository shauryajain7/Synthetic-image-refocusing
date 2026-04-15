
import cv2 #OpenCV, used here for its GaussianBlur tool
import numpy as np #image is just a giant grid of millions of numbers (pixels), NumPy allows us to do complex math on all those millions of numbers instantly

class BlurEngine:
    def __init__(self):
        pass #empty because this class doesn't need to download any AI models or set up windows. It just does math when asked

    def apply_layered_defocus(self, original_img, depth_map, focal_depth, max_blur_radius=25, num_layers=15, dof_thickness=20):
        # validation to prevent crashes if images missing
        if original_img is None or depth_map is None:
            return original_img
            
        depth_map_f = depth_map.astype(np.float32) #converts our 3D map into decimal numbers for high precision
        focal_depth_f = float(focal_depth)
        
        # slice the 3D space into discrete 15 layers
        bins = np.linspace(0, 255, num_layers)
        quantized_depth = np.digitize(depth_map_f, bins) #This looks at every single pixel and assigns it to one of the slices
        
        final_composite = np.zeros_like(original_img, dtype=np.float32)
        weight_sum = np.zeros_like(original_img, dtype=np.float32) #safety net to 
                                            #make sure our colors don't become overly bright when we stack layers together

        # process each depth layer (The Painter's Algorithm)
        for layer_idx in range(1, len(bins) + 1): #This starts a loop. We are going 1 layer at a time
            layer_depth = bins[layer_idx - 1] #Finds out exactly how deep this current slice is
            distance = abs(layer_depth - focal_depth_f) #Calculates how far this slice is from the user's chosen focus point
            
            # calculate dynamic blur based on distance if this slice is right next to the focus point, do not blur it at all
            if distance < (dof_thickness / 2):
                blur_radius = 0
            else:    #If it is far away, do math to figure out how much to blur. The further it is, the higher the blur_radius
                scale = (distance - (dof_thickness / 2)) / 255.0
                blur_radius = int(scale * max_blur_radius)
                
            # generate the blurred version for this layer
            if blur_radius > 0:
                k_size = max(3, blur_radius * 2 + 1)  #OpenCV's blur tool requires an odd number for its kernel size, 
                                                      #this ensures the number is always odd
                if k_size % 2 == 0: k_size += 1
                layer_img = cv2.GaussianBlur(original_img, (k_size, k_size), 0).astype(np.float32) #Applies the actual OpenCV blur to the entire image for this specific layer
            else:
                layer_img = original_img.astype(np.float32)
                
            # masking and stitching
            layer_mask = (quantized_depth == layer_idx).astype(np.float32) #Creates a stencil (mask). 
                                                            #It cuts out only the pixels that belong to this specific layer
            layer_mask = cv2.GaussianBlur(layer_mask, (5, 5), 0) # Smooth edges
            mask_3d = np.repeat(layer_mask[:, :, np.newaxis], 3, axis=2) #Converts the flat stencil into a 3-color (RGB) stencil 
                                                                         #so it matches our color photograph
            
            final_composite += (layer_img * mask_3d) #Paints this blurred, stenciled layer onto our blank canvas
            weight_sum += mask_3d
            
        # final Normalization and Output
        weight_sum[weight_sum == 0] = 1.0 #Prevents a "Divide by Zero" error, which crashes computers
        final_composite = final_composite / weight_sum #Normalizes the colors so the image looks natural
        return np.clip(final_composite, 0, 255).astype(np.uint8) #Makes sure no color values go below 0 or above 255