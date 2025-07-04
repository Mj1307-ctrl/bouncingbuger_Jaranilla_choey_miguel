import tkinter as tk
from PIL import Image, ImageTk
import os, random

# --- Configuration ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TOP_BUN_PATH = os.path.join("image", "top_buns.png")
BOTTOM_BUN_PATH = os.path.join("image", "bottom_buns.png")
FRAME_DELAY = 16  # ~60 FPS

class BouncingBurgerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Burger Bounce - Choey Miguel Jaranilla")
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="white")
        self.canvas.pack()

        self.load_and_combine_images()

        self.x = 200
        self.y = 200
        self.dx = 5
        self.dy = 4
        self.paused = False
        self.border_color = self.random_color()

        self.draw_burger()
        self.draw_status_text()

        self.root.bind("<space>", self.toggle_pause)
        self.animate()

    def load_and_combine_images(self):
        def trim_transparent(img):
            bbox = img.getbbox()
            return img.crop(bbox) if bbox else img

        # Load and trim images
        top = Image.open(TOP_BUN_PATH).convert("RGBA")
        bottom = Image.open(BOTTOM_BUN_PATH).convert("RGBA")
        top = trim_transparent(top)
        bottom = trim_transparent(bottom)

        # Layout settings
        self.gap_top = 10         # gap between top bun and name
        self.gap_bottom = 10      # gap between name and bottom bun
        self.text_height = 25     # estimated text height

        # Calculate final image dimensions
        self.burger_width = max(top.width, bottom.width)
        self.top_height = top.height
        self.bottom_height = bottom.height
        total_height = (
            self.top_height +
            self.gap_top +
            self.text_height +
            self.gap_bottom +
            self.bottom_height
        )
        self.burger_height = total_height

        # Create combined burger image (excluding name)
        self.burger_img_pil = Image.new("RGBA", (self.burger_width, total_height), (0, 0, 0, 0))

        # Paste top and bottom buns
        top_x = (self.burger_width - top.width) // 2
        bottom_x = (self.burger_width - bottom.width) // 2
        self.burger_img_pil.paste(top, (top_x, 0), top)
        bottom_y = self.top_height + self.gap_top + self.text_height + self.gap_bottom
        self.burger_img_pil.paste(bottom, (bottom_x, bottom_y), bottom)

        # Convert to Tk image
        self.burger_img_tk = ImageTk.PhotoImage(self.burger_img_pil)

        # Calculate name text Y offset (relative to image center)
        self.text_offset_y = (
            -self.burger_height // 2 +
            self.top_height +
            self.gap_top +
            self.text_height // 2
        )

    def draw_burger(self):
        pad_x = 20
        pad_y = 15

        self.oval_item = self.canvas.create_oval(
            self.x - self.burger_width // 2 - pad_x,
            self.y - self.burger_height // 2 - pad_y,
            self.x + self.burger_width // 2 + pad_x,
            self.y + self.burger_height // 2 + pad_y,
            outline=self.border_color,
            width=4
        )

        self.image_item = self.canvas.create_image(
            self.x, self.y, image=self.burger_img_tk
        )

        self.name_item = self.canvas.create_text(
            self.x,
            self.y + self.text_offset_y,
            text="Choey Miguel Jaranilla",
            fill=self.border_color,
            font=("Arial", 16, "bold")
        )

    def draw_status_text(self):
        self.status_item = self.canvas.create_text(
            WINDOW_WIDTH // 2,
            30,
            text="RUNNING",
            fill="gray20",
            font=("Arial", 14, "italic")
        )

    def update_status_text(self):
        status = "PAUSED" if self.paused else "RUNNING"
        self.canvas.itemconfig(self.status_item, text=status)

    def random_color(self):
        return "#%06x" % random.randint(0, 0xFFFFFF)

    def toggle_pause(self, event=None):
        self.paused = not self.paused
        self.update_status_text()

    def animate(self):
        if not self.paused:
            self.move_burger()
        self.root.after(FRAME_DELAY, self.animate)

    def move_burger(self):
        self.x += self.dx
        self.y += self.dy
        hit_edge = False

        # Calculate bounds
        if self.x <= self.burger_width // 2:
            self.x = self.burger_width // 2
            self.dx *= -1
            hit_edge = True
        elif self.x >= WINDOW_WIDTH - self.burger_width // 2:
            self.x = WINDOW_WIDTH - self.burger_width // 2
            self.dx *= -1
            hit_edge = True

        if self.y <= self.burger_height // 2:
            self.y = self.burger_height // 2
            self.dy *= -1
            hit_edge = True
        elif self.y >= WINDOW_HEIGHT - self.burger_height // 2:
            self.y = WINDOW_HEIGHT - self.burger_height // 2
            self.dy *= -1
            hit_edge = True

        if hit_edge:
            self.border_color = self.random_color()
            self.canvas.itemconfig(self.oval_item, outline=self.border_color)
            self.canvas.itemconfig(self.name_item, fill=self.border_color)

        # Update all canvas item positions
        pad_x = 20
        pad_y = 15
        self.canvas.coords(
            self.oval_item,
            self.x - self.burger_width // 2 - pad_x,
            self.y - self.burger_height // 2 - pad_y,
            self.x + self.burger_width // 2 + pad_x,
            self.y + self.burger_height // 2 + pad_y
        )
        self.canvas.coords(self.image_item, self.x, self.y)
        self.canvas.coords(self.name_item, self.x, self.y + self.text_offset_y)

# --- Run the app ---
if __name__ == "__main__":
    root = tk.Tk()
    app = BouncingBurgerApp(root)
    root.mainloop()
