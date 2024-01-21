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
from io import BytesIO
import base64
import uuid

st.set_page_config(layout="wide")
ClarifaiStreamlitCSS.insert_default_css(st)

st.title("Eco Life 360")




def main():
    allowed_file_types = ["jpg", "jpeg", "png", "gif"]
    uploaded_file = st.file_uploader("Choose an image...", type=allowed_file_types)

    with st.sidebar:
        st.text('Add your Clarifai PAT')
        clarifai_pat = st.text_input('Clarifai PAT:', type='password')
    
    if not clarifai_pat:
        st.warning('Please enter your PAT to continue!', icon='⚠️')
    elif uploaded_file is None:
        st.warning('Please upload an image to proceed.', icon='⚠️')
    else:
        os.environ['CLARIFAI_PAT'] = clarifai_pat

        if uploaded_file is not None:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Save the uploaded file to a temporary directory
            temp_dir = "temp_images"
            os.makedirs(temp_dir, exist_ok=True)
            filename = str(uuid.uuid4()) + "_" + uploaded_file.name
            filepath = os.path.join(temp_dir, filename)
            
            with open(filepath, "wb") as f:
                f.write(uploaded_file.read())
            
            # Convert image to base64 for Clarifai API
            base64_image = encode_image(filepath)
            
            # Clarifai API call
            prompt = "Generate me a nutrient chart of the following dish"
            inference_params = dict(temperature=0.4, image_base64=base64_image, max_tokens=100)
            inputs_dict = {
                "data": {
                    "image": {
                        "base64": base64_image
                    },
                    "text": {
                        "raw": prompt
                    }
                }
            }
            
            model_prediction = Model("https://clarifai.com/openai/chat-completion/models/openai-gpt-4-vision").predict(
                inputs=[inputs_dict],
                inference_params=inference_params
            )
            
            # Display the result
            st.text(model_prediction.outputs[0].data.text.raw)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
if __name__== '__main__':
  main()

