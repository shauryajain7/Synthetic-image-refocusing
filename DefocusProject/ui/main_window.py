
import tkinter as tk                       #python tool for building desktop windows
from tkinter import filedialog             #tool that opens the "Choose a File" pop-up window so the user can select a photo
import cv2                                 #OpenCV (used here to convert image colors)
from PIL import Image, ImageTk             #Tkinter cannot understand OpenCV images directly. PIL acts as a translator to convert the image so Tkinter can show it on the screen
import numpy as np                         #for basic math when calculating screen sizes
from config import Config                  #brings in your rulebook for colors and titles
from utils.helpers import create_heatmap, resize_with_aspect #brings in two of your custom helper tools to colorize the depth map and resize big images

class DefocusAppUI:
    def __init__(self, root, processor):                     #when the window is created, it takes root and processor
        self.root = root                                     #saves them so the whole class can use them
        self.processor = processor                           
        self.root.title(f"{Config.PROJECT_NAME} - V2.0")     #sets the text at the very top of the window bar
        self.root.geometry("1400x850")                       #sets the starting size of the window
        self.root.configure(bg=Config.BG_COLOR)              #paints the background

        self.original_img = None                             #empty placeholders
        self.depth_map = None
        self.processed_img = None
        self.focal_point = 128                               #sets the default focus exactly in the middle of the 3D space

        self.setup_ui()                                      #calls the next function to start drawing the buttons

    def setup_ui(self):
        # control Bar
        toolbar = tk.Frame(self.root, bg=Config.PANEL_COLOR, pady=20)    #horizontal bar at the top for controls
        toolbar.pack(side=tk.TOP, fill=tk.X) #sticks this bar to the yop of the window and stretches it across the X-axis

        tk.Button(toolbar, text="UPLOAD IMAGE", command=self.load_image, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=20) #Creates the Upload button
        
        # sliders
        # creates the two sliding bars for intensity and quality
        self.blur_slider = tk.Scale(toolbar, from_=5, to=80, orient=tk.HORIZONTAL, label="Blur Intensity", bg=Config.PANEL_COLOR, fg="white", highlightthickness=0, command=lambda _: self.reprocess())
        self.blur_slider.set(30)   #sets default to 30
        self.blur_slider.pack(side=tk.LEFT, padx=20)

        self.layer_slider = tk.Scale(toolbar, from_=3, to=30, orient=tk.HORIZONTAL, label="Render Quality (Layers)", length=200, bg=Config.PANEL_COLOR, fg="white", highlightthickness=0, command=lambda _: self.reprocess())
        self.layer_slider.set(12)
        self.layer_slider.pack(side=tk.LEFT, padx=20)

        tk.Button(toolbar, text="DOWNLOAD IMAGE", command=self.save_image, font=("Arial", 10, "bold"), bg=Config.SUCCESS_COLOR).pack(side=tk.RIGHT, padx=20) #Save button on the right side of toolbar

        # 3 panels
        workspace = tk.Frame(self.root, bg=Config.BG_COLOR) #creates a giant empty space below the toolbar to hold the images
        workspace.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        workspace.columnconfigure(0, weight=1, uniform="panel") #forces all 3 columns to share width equally
        workspace.columnconfigure(1, weight=1, uniform="panel")
        workspace.columnconfigure(2, weight=1, uniform="panel")
        workspace.rowconfigure(0, weight=1)

        # panel 1 Interactive
        self.canvas_orig = tk.Canvas(workspace, bg="black", highlightthickness=1, highlightbackground="white") #Panel 1 for the original image
        self.canvas_orig.grid(row=0, column=0, sticky="nsew", padx=5)
        self.canvas_orig.bind("<Button-1>", self.handle_click)  #tells if the user left-clicks inside Panel 1, instantly run the handle_click function
        self.canvas_orig.bind("<Configure>", self._on_resize) #re-renders images when panels are resized

        # panel 2 Depth View
        frame_depth = tk.Frame(workspace, bg="black")
        frame_depth.grid(row=0, column=1, sticky="nsew", padx=5)
        frame_depth.pack_propagate(False)  #prevents image content from resizing the panel
        self.lbl_depth = tk.Label(frame_depth, bg="black")
        self.lbl_depth.pack(fill=tk.BOTH, expand=True)
        frame_depth.bind("<Configure>", self._on_resize) #re-renders images when panels are resized

        # panel 3 Output View
        frame_final = tk.Frame(workspace, bg="black")
        frame_final.grid(row=0, column=2, sticky="nsew", padx=5)
        frame_final.pack_propagate(False)  #prevents image content from resizing the panel
        self.lbl_final = tk.Label(frame_final, bg="black")
        self.lbl_final.pack(fill=tk.BOTH, expand=True)
        frame_final.bind("<Configure>", self._on_resize) #re-renders images when panels are resized

    def load_image(self):
        path = filedialog.askopenfilename() #opens the file explorer. path stores the location of the selected image
        if not path: return
        
        # to load and set initial state
        self.original_img, self.depth_map = self.processor.run_inference(path) #Hands the file path to processor to run the AI 
                                                                               #It gets back the real image and the 3D map
        
        if self.original_img is not None:
            self.display_image(self.original_img, self.canvas_orig)              #function to actually paint the pictures onto the panels
            self.display_image(create_heatmap(self.depth_map), self.lbl_depth)
            self.reprocess()  #immediately applies the default blur

    def handle_click(self, event):
        """THIS IS THE FIX: Maps mouse click to image depth."""
        if self.depth_map is None: return
        
        # to get current size of the canvas window. Gets the width and height of the UI panel on your screen
        cw = self.canvas_orig.winfo_width()
        ch = self.canvas_orig.winfo_height()
        
        # to get actual image size
        ih, iw = self.original_img.shape[:2]

        # to calculate how the image is scaled on your screen
        scale = min(cw/iw, ch/ih)
        nw, nh = int(iw * scale), int(ih * scale)
        x_off, y_off = (cw - nw) // 2, (ch - nh) // 2

        # to map the click coordinates to image coordinates. translate your screen click (event.x) back to the exact pixel coordinate on the real photograph (tx, ty)
        tx = int((event.x - x_off) / scale)
        ty = int((event.y - y_off) / scale)

        # to check if click is inside the image and update
        if 0 <= tx < iw and 0 <= ty < ih:
            self.focal_point = self.depth_map[ty, tx]  #t sets this as the new focus 
            print(f"System: Focusing on depth {self.focal_point} at pixel ({tx}, {ty})")
            self.reprocess() #re-renders the blur with this new focus

    def reprocess(self): #tells the processor to run the complex blur math using the new focus, the blur slider value, and the layer slider value
        if self.original_img is None: return
        
        self.processed_img = self.processor.apply_defocus(
            self.original_img, self.depth_map, self.focal_point, 
            self.blur_slider.get(), self.layer_slider.get()
        )
        self.display_image(self.processed_img, self.lbl_final)

    def save_image(self):
        """Opens a save dialog and exports the processed image."""
        if self.processed_img is None:
            print("System: No processed image to save. Please load and process an image first.")
            return
        
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg *.jpeg"), ("All Files", "*.*")]
        )
        if not path: return  #user cancelled the dialog
        
        cv2.imwrite(path, self.processed_img)
        print(f"System: Image saved successfully to {path}")

    def display_image(self, cv_img, widget):
        rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB) #OpenCV reads colors backwards as Blue-Green-Red (BGR). Tkinter needs Standard Red-Green-Blue (RGB). This fixes it
        img = Image.fromarray(rgb) #Converts the math array into a PIL Image
        
        # to fit image to the panel size
        widget.update_idletasks()
        w = widget.winfo_width()
        h = widget.winfo_height()
        if w > 10: img.thumbnail((w, h), Image.Resampling.LANCZOS) #Shrinks the image so it perfectly fits inside its panel without stretching out of proportion
        
        photo = ImageTk.PhotoImage(img) #Final conversion into a format Tkinter can draw
        if isinstance(widget, tk.Canvas):
            widget.delete("all")
            widget.image = photo
            widget.create_image(w//2, h//2, image=photo, tag="img")
        else:
            widget.config(image=photo) #Paints it onto the screen
            widget.image = photo

    def _on_resize(self, event):
        """Re-renders all images when any panel is resized."""
        if self.original_img is None: return
        self.display_image(self.original_img, self.canvas_orig)
        if self.depth_map is not None:
            self.display_image(create_heatmap(self.depth_map), self.lbl_depth)
        if self.processed_img is not None:
            self.display_image(self.processed_img, self.lbl_final)