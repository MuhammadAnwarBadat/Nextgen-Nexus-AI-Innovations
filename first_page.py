import streamlit as st
from clarifai.client.auth import create_stub
from clarifai.client.auth.helper import ClarifaiAuthHelper
from clarifai.client.user import User
from clarifai.modules.css import ClarifaiStreamlitCSS
from google.protobuf import json_format, timestamp_pb2
from dotenv import load_dotenv
load_dotenv()
import os
clarifai_pat=os.getenv('CLARIFAI_PAT')
from clarifai.client.model import Model
from clarifai.client.input import Inputs
from PIL import Image
import io
import uuid

st.set_page_config(layout="wide")
ClarifaiStreamlitCSS.insert_default_css(st)

st.title("Eco Life 360")

def main():
  allowed_file_types = ["jpg", "jpeg", "png", "gif"]
  uploaded_file = st.file_uploader("Choose an image...", type=allowed_file_types)
  with st.sidebar:
    st.text('Add your Clarifai PAT')
    clarifai_pat = st.text_input('Clarifai PAT:',type='password')
  if not clarifai_pat:
    st.warning('Please enter your PAT to continue!',icon='⚠️')
  else:
    os.environ['CLARIFAI_PAT'] = clarifai_pat
    
    if uploaded_file is not None:
      # Display the uploaded image
      image = Image.open(uploaded_file)
      st.image(image, caption="Uploaded Image", use_column_width=True)
      filename = str(uuid.uuid4()) + "_" + uploaded_file.name
      # Save the uploaded file to a temporary directory
      temp_dir = "temp_images"
      os.makedirs(temp_dir, exist_ok=True)
      filepath = os.path.join(temp_dir, filename)
      with open(filepath, "rb") as f:
        file_bytes=(uploaded_file.read())
      #image_bytes1 = io.BytesIO()
      #image.save(image_bytes, format="PNG")  # You can choose a different format if needed
      #image_bytes1 = image_bytes1.getvalue()
      #with open(uploaded_file, "rb") as f:
        #file_bytes = f.read()
    
    prompt = "Generate me a nutrient chart of the following dish"# "What dish is this and also describe it's percentage of each ingredients used in it and also its health effects?"
    inference_params = dict(temperature=0.4, max_tokens=100)
    
    model_prediction = Model("https://clarifai.com/openai/chat-completion/models/openai-gpt-4-vision").predict(inputs = [Inputs.get_multimodal_input(input_id="", image_bytes = file_bytes, raw_text=prompt)], inference_params=inference_params)
    #print(model_prediction.outputs[0].data.text.raw)

    st.text(b'{model_prediction.outputs[0].data.text.raw}')

if __name__== '__main__':
  main()

