import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


# Define paths
source_folder = filedialog.askdirectory(
    title="Select Source Folder"
)  # Folder containing images
destination_folder = filedialog.askdirectory(
    title="Select Destination Folder"
)  # Folder to save cropped images


# Get all image files from source folder
image_files = [
    f for f in os.listdir(source_folder) if f.lower().endswith(("png", "jpg", "jpeg"))
]
current_index = 0


# Create a window
root = tk.Tk()
root.title("Image Cropper")


# Load first image
img = None
tk_img = None  # Keep a reference to the image
canvas = tk.Canvas(root)
canvas.pack(fill=tk.BOTH, expand=True)


# Selection rectangle
start_x, start_y, rect_id = None, None, None


def load_image():
    """Load and display the current image."""
    global img, tk_img, canvas, current_index
 
    if current_index >= len(image_files):
        print("All images processed!")
        root.quit()
        return
    image_path = os.path.join(source_folder, image_files[current_index])
    img = Image.open(image_path)
    img.thumbnail((800, 800))  # Resize for display
    tk_img = ImageTk.PhotoImage(img)
 
    canvas.config(width=tk_img.width(), height=tk_img.height())
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)
 
    # ✅ Prevent garbage collection
    canvas.image = tk_img  # Keep reference to prevent deletion


def on_mouse_down(event):
    """Start selection."""
    global start_x, start_y, rect_id
    start_x, start_y = event.x, event.y
    if rect_id:
        canvas.delete(rect_id)  # Remove previous rectangle
    rect_id = canvas.create_rectangle(
        start_x, start_y, start_x, start_y, outline="red", width=2
    )


def on_mouse_drag(event):
    """Draw selection rectangle while dragging."""
    global rect_id
    canvas.coords(rect_id, start_x, start_y, event.x, event.y)


def on_mouse_up(event):
    """Finalize selection and save cropped image."""
    global current_index

    end_x, end_y = event.x, event.y

    if start_x and start_y and end_x and end_y:
        # Ensure coordinates are correct (top-left to bottom-right)
        left, upper, right, lower = (
            min(start_x, end_x),
            min(start_y, end_y),
            max(start_x, end_x),
            max(start_y, end_y),
        )

        cropped_img = img.crop((left, upper, right, lower))

        # Generate a unique filename
        filename = f"cropped_{current_index+1}.jpg"
        save_path = os.path.join(destination_folder, filename)
        cropped_img.save(save_path, "JPEG")

        print(f"Saved: {save_path}")

        # Move to the next image
        current_index += 1
        load_image()


# Bind mouse events
canvas.bind("<ButtonPress-1>", on_mouse_down)
canvas.bind("<B1-Motion>", on_mouse_drag)
canvas.bind("<ButtonRelease-1>", on_mouse_up)


# Load the first image
load_image()


# Run the app
root.mainloop()
