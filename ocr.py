import google.generativeai as genai  
from PIL import Image  
import streamlit as st  
import os  

# Set the initial configuration for the Streamlit app
st.set_page_config(page_title="OCR App", initial_sidebar_state="expanded", layout="wide") 
st.title("OCR Using Gemini Flash") 

# Fetch the Google API key from environment variables
google_genai_key = "AIzaSyAV60kxvHGel5ok_LwFLEOB05GaoHin1s8"

# Configure the Google Gemini API with the loaded API key
genai.configure(api_key=google_genai_key)
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

with st.sidebar:
    st.title("Select an image")  # Sidebar title
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])  
    if uploaded_file:
        image = Image.open(uploaded_file)  
        st.image(image, caption='Uploaded Image') 

if uploaded_file:
    if st.button("Extract Text", type="primary"):
        with st.spinner("Processing image..."):  # Show a spinner while processing
            try:
                prompt = """Analyze the image provided and extract all readable text.
                Present the extracted content in a well-organized Markdown format. 
                Ensure proper formatting by using headings, bullet points, numbered lists, 
                and code blocks where appropriate to enhance clarity and readability. 
                Retain the structure of the original content, ensuring that sections, titles, 
                and important details are clearly separated. If the image contains any tables or 
                code snippets, format them correctly to preserve their meaning. 
                The output should be clear, concise, and easy to interpret."""
                
                inputs = [prompt]
                inputs.append(image)
                response = model.generate_content(inputs)
                st.session_state['ocr_extracted_text'] = response.text
            except Exception as e:
                st.error(f"Error processing image: {str(e)}")

if 'ocr_extracted_text' in st.session_state:
    st.markdown(st.session_state['ocr_extracted_text'])  # Display the extracted text in Markdown format
else:
    st.info("Upload an image and press 'Extract Text'.") 
