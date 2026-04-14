import tkinter as tk
import tkinter.messagebox
import turtle as trtl
import random
from PIL import Image
import io
import os

# --- CONFIGURATION ---
BLOCK_SIZE = 60
START_X = -250
START_Y = 180
message = "Hello Hello"

PETAL_COLORS = ["#FF69B4", "#BA55D3", "#9370DB", "#FFB6C1", "#E6E6FA", "#F08080"]

# --- DATA CONVERSION ---
characters_as_bits = ['{0:08b}'.format(ord(cha)) for cha in message]

# --- SETUP SCREEN FIRST, then create Turtle ---
screen = trtl.Screen()
screen.setup(800, 600)
screen.title("Flower Message Encoder")

painter = trtl.Turtle()
painter.speed(0)
screen.tracer(0)  # Turn off animation - draw everything instantly, no mid-draw interruptions


def draw_background():
    screen.bgcolor("#90EE90")
    painter.penup()
    painter.fillcolor("#7CCD7C")
    painter.goto(-500, -400)
    painter.begin_fill()
    painter.setheading(0)
    for _ in range(2):
        painter.forward(1000)
        painter.left(90)
        painter.forward(400)
    painter.end_fill()


def draw_data_flower(x, y, petal_color, center_color):
    painter.penup()
    painter.goto(x, y - 40)
    painter.color("#228B22")
    painter.pensize(4)
    painter.setheading(90)
    painter.pendown()
    painter.forward(30)
    painter.penup()

    painter.shape("circle")
    painter.turtlesize(1.2)
    painter.goto(x - 12, y)
    painter.color(petal_color)
    for _ in range(6):
        painter.right(60)
        painter.forward(18)
        painter.stamp()
    painter.goto(x, y - 10)
    painter.color(center_color)
    painter.stamp()


# --- DRAWING EXECUTION ---
draw_background()

painter.penup()
painter.goto(START_X - 60, START_Y + 40)
painter.shape("square")
painter.color("red")
painter.turtlesize(1)
painter.stamp()

for char_index, bit_string in enumerate(characters_as_bits):
    row_y = START_Y - (char_index * BLOCK_SIZE * 1.2)
    for bit_index, bit in enumerate(bit_string):
        pos_x = START_X + (bit_index * BLOCK_SIZE)
        random_petal = random.choice(PETAL_COLORS)
        bit_color = "orange" if bit == '1' else "yellow"
        draw_data_flower(pos_x, row_y, random_petal, bit_color)

# Render everything now that all drawing is done
screen.update()
painter.hideturtle()


def save_image():
    canvas = trtl.getcanvas()

    # Save canvas as EPS (always works, no Ghostscript needed)
    eps_path = "output.eps"
    canvas.postscript(file=eps_path, colormode='color')
    print(f"Saved {eps_path}")

    # Try converting EPS -> PNG (requires Ghostscript on Windows)
    png_path = "output.png"
    try:
        img = Image.open(eps_path)
        img = img.convert("RGB")
        img.save(png_path)
        print(f"Saved {png_path}  ({img.size[0]}x{img.size[1]} px)")
        os.remove(eps_path)
        result_file = png_path
    except Exception as e:
        print(f"PNG conversion failed (Ghostscript probably not installed): {e}")
        print(f"EPS file saved as '{eps_path}' - open in Inkscape or Word.")
        result_file = eps_path

    # Save layout metadata for the decoder
    with open("message_config.txt", "w") as f:
        f.write(f"START_X={START_X}\n")
        f.write(f"START_Y={START_Y}\n")
        f.write(f"BLOCK_SIZE={BLOCK_SIZE}\n")
        f.write(f"NUM_CHARS={len(characters_as_bits)}\n")
        f.write(f"CANVAS_WIDTH={canvas.winfo_width()}\n")
        f.write(f"CANVAS_HEIGHT={canvas.winfo_height()}\n")
    print("Saved message_config.txt")

    tkinter.messagebox.showinfo("Done", f"Saved: {result_file}\nand message_config.txt")


screen.ontimer(save_image, 500)
trtl.mainloop()