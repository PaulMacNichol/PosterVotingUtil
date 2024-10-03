import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class ImageVotingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Voting App")

        # Maximize the window
        self.master.state('zoomed')

        self.posters_dir = r'path/to/Posters'
        self.thumbs_up_dir = r'path/to/thumbs_up'

        self.images = self.load_images()
        self.current_image_index = 0

        # Create a frame for the canvas and scrollbars
        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas
        self.canvas = tk.Canvas(self.frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create scrollbars
        self.v_scrollbar = tk.Scrollbar(
            self.frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.h_scrollbar = tk.Scrollbar(
            master, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scrollbar.pack(fill=tk.X)

        # Configure the canvas to use the scrollbars
        self.canvas.configure(
            yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        # Create a frame inside the canvas to hold the image
        self.image_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.image_frame, anchor='nw')

        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(pady=20)

        self.file_label = tk.Label(self.image_frame)
        self.file_label.pack()

        # Swap the locations of thumbs up and thumbs down buttons
        self.thumbs_down_button = tk.Button(
            self.image_frame, text="Thumbs Down", command=self.vote_down)
        self.thumbs_down_button.pack(side=tk.LEFT, padx=10)

        self.thumbs_up_button = tk.Button(
            self.image_frame, text="Thumbs Up", command=self.vote_up)
        self.thumbs_up_button.pack(side=tk.RIGHT, padx=10)

        self.image_frame.bind("<Configure>", self.on_frame_configure)

        # Bind mouse wheel for scrolling
        self.master.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # Bind Q and E keys for navigation
        self.master.bind("<q>", self.vote_down)  # Q key for thumbs down
        self.master.bind("<e>", self.vote_up)     # E key for thumbs up

        self.show_image()

    def load_images(self):
        images = []
        for subdir, _, files in os.walk(self.posters_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    images.append(os.path.join(subdir, file))
        return images

    def show_image(self):
        if self.images:
            image_path = self.images[self.current_image_index]
            self.image = Image.open(image_path)

            # Resize image to fit the window
            self.resize_image()

            self.photo = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.photo)
            self.file_label.config(text=os.path.basename(image_path))
            self.update_scrollregion()
        else:
            messagebox.showinfo("Info", "No images found.")
            self.master.quit()

    def resize_image(self):
        # Get window dimensions
        window_width = self.master.winfo_width()
        window_height = self.master.winfo_height()

        # Ensure window dimensions are valid
        if window_width <= 0 or window_height <= 0:
            return

        aspect_ratio = self.image.width / self.image.height

        # Calculate new dimensions
        if window_width / window_height > aspect_ratio:
            new_width = int(window_height * aspect_ratio)
            new_height = window_height
        else:
            new_width = window_width
            new_height = int(window_width / aspect_ratio)

        # Ensure new dimensions are valid
        if new_width <= 0 or new_height <= 0:
            return

        # Resize the image
        self.image = self.image.resize((new_width, new_height), Image.LANCZOS)

    def vote_up(self, event=None):  # Added event parameter to support key binding
        self.copy_image_to_thumbs_up()
        self.next_image()

    def vote_down(self, event=None):  # Added event parameter to support key binding
        self.next_image()

    def next_image(self):
        self.current_image_index += 1
        if self.current_image_index < len(self.images):
            self.show_image()
        else:
            messagebox.showinfo("Info", "No more images to display.")
            self.master.quit()

    def copy_image_to_thumbs_up(self):
        if not os.path.exists(self.thumbs_up_dir):
            os.makedirs(self.thumbs_up_dir)
        thumbs_up_image_path = self.images[self.current_image_index]
        filename = os.path.basename(thumbs_up_image_path)
        new_path = os.path.join(self.thumbs_up_dir, filename)
        with open(thumbs_up_image_path, 'rb') as fsrc:
            with open(new_path, 'wb') as fdst:
                fdst.write(fsrc.read())

    def update_scrollregion(self):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_frame_configure(self, event):
        # Update the scrollbars when the image frame changes size
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event):
        # Scroll the canvas based on mouse wheel movement
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageVotingApp(root)
    root.mainloop()
