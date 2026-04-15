#This file contains small, reusable helper functions
#it has a tool to safely shrink images, and a tool to add cool colors to your 3D depth map
import cv2

def resize_with_aspect(image, width=None, height=None):
    """Resizes image while maintaining the golden ratio of the photo."""
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

def create_heatmap(depth_map):
    """Converts raw depth data into academic visualization data."""
    return cv2.applyColorMap(depth_map, cv2.COLORMAP_INFERNO)