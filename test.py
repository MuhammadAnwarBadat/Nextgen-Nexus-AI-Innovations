#pip install tk

from dotenv import load_dotenv
load_dotenv()
import os
clarifai_pat=os.getenv('CLARIFAI_PAT')
from clarifai.client.model import Model
from clarifai.client.input import Inputs
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

# Open a file dialog to choose an image file
file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.jpeg;*.jpg;*.png")])

# Check if a file was selected
if file_path:
    # Read the contents of the selected image file
    with open(file_path, "rb") as f:
        file_bytes = f.read()


prompt = "What dish is this and also its describe percentage of each ingredients used and also its health effects?"
inference_params = dict(temperature=0.4, max_tokens=100)

model_prediction = Model("https://clarifai.com/openai/chat-completion/models/openai-gpt-4-vision").predict(inputs = [Inputs.get_multimodal_input(input_id="", image_bytes = file_bytes, raw_text=prompt)], inference_params=inference_params)
print(model_prediction.outputs[0].data.text.raw)
