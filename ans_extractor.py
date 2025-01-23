import os
import logging
from PIL import Image
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import io

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Function to get the response from Gemini API
def get_gemini_response(input_prompt,image_data, context):
    if image_data is None:
        raise ValueError("No image data found.")

    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([input_prompt, image_data, context])
    return response.text

# Streamlit UI Setup
st.set_page_config(page_title="Real-Time Camera Input - AI Processor", layout="wide")
st.title("📸 Real-Time Camera Input Processor")
st.markdown("""
    This app captures a real-time image from your camera, processes it, and sends it to Gemini AI for analysis.
    Enter your question and get insights based on the captured image.
""")

# Camera capture section
st.subheader("1. Capture Image Using Camera 📷")
image_file = st.camera_input("Take a photo")

# Display captured image preview
if image_file:
    st.image(image_file, caption="Captured Image Preview", use_container_width=True)

# User input section for prompt
st.subheader("2. Enter Your Question 🧐")
input_prompt = st.text_input("Ask a question about the captured image:", key="input_prompt")

# Button to submit the question
submit = st.button("Process Image and Ask Gemini 🤖")

# Response section
if submit:
    if image_file:
        with st.spinner("Processing..."):
            try:
       # Convert image to bytes for processing
                image_bytes = image_file.getvalue()
                image_data = {"mime_type": "image/jpeg", "data": image_bytes}

                # Predefined context for Gemini
                context = """
                    You are an expert in understanding and analyzing images.
                    The input is a real-time captured image, and your task is to answer the provided question based on the image's content.
                    just give correct ans from the given options. Do not solve the question.
                """

                # Get response from Gemini
                response = get_gemini_response( input_prompt,image_data, context)

                st.subheader("Gemini's Response 🤖")
                st.write(response)
            except Exception as e:
                logging.error(f"Error generating response from Gemini: {e}")
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please capture an image and enter a question to proceed.")

# Footer
st.markdown("""
    ---  
            









    💬 Have questions? Reach out at: prakharsrivastava337@gmail.com
""", unsafe_allow_html=True)
