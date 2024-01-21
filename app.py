#pip install tk, python-dotenv

from dotenv import load_dotenv
load_dotenv()
import os
clarifai_pat = os.getenv('CLARIFAI_PAT')
from clarifai.client.model import Model
from clarifai.client.input import Inputs
import tkinter as tk
from tkinter import filedialog, simpledialog

def normalize_input(input_str):
    # Normalize input to lower case and strip spaces
    return [item.strip().lower() for item in input_str.split(',') if item.strip()]

def check_allergy(allergy, ingredients_list):
    # Additional check for common variations or synonyms of allergens
    allergy_variants = {
        'shrimp': ['shrimp', 'prawns'],
        # Add more allergens and their common variants here if needed
    }
    # Check for both the allergy and its variants
    variants = allergy_variants.get(allergy, [allergy])
    return any(variant in ingredients_list for variant in variants)

# Function to get user health information
def get_user_health_info():
    health_info = {}
    health_info['allergies'] = normalize_input(simpledialog.askstring("Health Information", "Do you have any food allergies? (Enter comma-separated list or 'None')"))
    health_info['dietary_restrictions'] = normalize_input(simpledialog.askstring("Health Information", "Any dietary restrictions? (e.g., vegetarian, gluten-free, etc. or 'None')"))
    health_info['health_conditions'] = normalize_input(simpledialog.askstring("Health Information", "Any health conditions to consider? (e.g., diabetes, hypertension, etc. or 'None')"))
    return health_info

# Function to analyze ingredients against user's health information
def analyze_ingredients(ingredients, health_info):
    advice = ""
    ingredients_list = normalize_input(ingredients)

    # Check for allergies
    for allergy in health_info['allergies']:
        if check_allergy(allergy, ingredients_list):
            advice += f"Warning: This dish contains {allergy}, which you are allergic to.\n"

    # Rest of the checks remain the same...

    return advice if advice else "This food is suitable for you."

root = tk.Tk()
root.withdraw()

# Simplified file dialog to choose an image file
file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.jpg"), ("Image files", "*.jpeg"), ("Image files", "*.png")])

# Check if a file was selected
if file_path:
    # Read the contents of the selected image file
    with open(file_path, "rb") as f:
        file_bytes = f.read()

    # Modified prompt to focus on identifying ingredients
    prompt = "Identify the ingredients in this dish."
    inference_params = dict(temperature=0.4, max_tokens=100)

    # Get model prediction
    model_prediction = Model("https://clarifai.com/openai/chat-completion/models/openai-gpt-4-vision").predict(inputs=[Inputs.get_multimodal_input(input_id="", image_bytes=file_bytes, raw_text=prompt)], inference_params=inference_params)
    ingredients = model_prediction.outputs[0].data.text.raw
    print("Identified Ingredients:", ingredients)

    # Get user health information
    user_health_info = get_user_health_info()

    # Analyze ingredients against user's health information
    advice = analyze_ingredients(ingredients, user_health_info)
    print(advice)
