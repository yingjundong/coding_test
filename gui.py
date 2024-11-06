import PySimpleGUI as sg
import numpy as np
import io
from PIL import Image, ImageTk
from synthetic_img_gen import gen_syn_img

def convert_to_tk_image(pil_image):
    bio = io.BytesIO()
    pil_image.convert("RGB").save(bio, format="PNG")
    return ImageTk.PhotoImage(data=bio.getvalue())

# Define PySimpleGUI layout
layout = [
    [sg.Text("Width"), sg.Slider(range=(100, 1000), orientation="h", size=(20, 15), default_value=500, key="-WIDTH-")],
    [sg.Text("Height"), sg.Slider(range=(100, 1000), orientation="h", size=(20, 15), default_value=500, key="-HEIGHT-")],
    [sg.Text("Number of Cells"), sg.Slider(range=(1, 50), orientation="h", size=(20, 15), default_value=10, key="-NUM_CELLS-")],
    [sg.Text("Fluorescence Level"), sg.Slider(range=(0.1, 1.0), resolution=0.1, orientation="h", size=(20, 15), default_value=0.5, key="-FLUORESCENCE-")],
    [sg.Text("Cell Size"), sg.Slider(range=(5, 50), orientation="h", size=(20, 15), default_value=10, key="-SIZE-")],
    [sg.Text("Noise Level"), sg.Slider(range=(0, 50), orientation="h", size=(20, 15), default_value=5, key="-NOISE-")],
    [sg.Button("Generate Image"), sg.Button("Exit")],
    [sg.Text("Generated Fluorescence Image:"), sg.Image(key="-IMAGE-")],
    [sg.Text("Generated Labeled Image:"), sg.Image(key="-LABEL-")]
]

# Create the window
window = sg.Window("Synthetic Image Generator", layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    elif event == "Generate Image":
        # Get parameter values from the sliders
        width = int(values["-WIDTH-"])
        height = int(values["-HEIGHT-"])
        num_cells = int(values["-NUM_CELLS-"])
        fluore_level = float(values["-FLUORESCENCE-"])
        cell_size = int(values["-SIZE-"])
        shape = "circle"
        noise_level = float(values["-NOISE-"])

        # Generate images
        fluorescence_image, labeled_image = gen_syn_img(height, width, num_cells, fluore_level, cell_size, shape, noise_level)

        # Convert images to Tk format and update UI
        window["-IMAGE-"].update(data=convert_to_tk_image(fluorescence_image))
        window["-LABEL-"].update(data=convert_to_tk_image(labeled_image))

window.close()