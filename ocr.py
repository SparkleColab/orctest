import google.generativeai as genai  
from PIL import Image  
import streamlit as st  
import os  

# Set the initial configuration for the Streamlit app
st.set_page_config(page_title="OCR App", initial_sidebar_state="expanded", layout="wide") 
st.title("Wall Defect Detection") 

# Fetch the Google API key from environment variables
google_genai_key = os.getenv("GOOGLE_API_KEY")

# Configure the Google Gemini API with the loaded API key
genai.configure(api_key=google_genai_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

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
                prompt = """Analyse the image provided and identify any wall defects. Describe the defects in detail including
                any potential root causes, and recommended corrections. In case the image does not have a wall, 
                describe the image and request another image that has a wall avaialable. 
                Present the extracted content in a well-organized Markdown format. 
                Ensure proper formatting by using headings, bullet points, numbered lists, 
                and code blocks where appropriate to enhance clarity and readability. """
                
                inputs = [prompt]
                inputs.append(image)
                response = model.generate_content(inputs)
                st.session_state['wall_defects'] = response.text
            except Exception as e:
                st.error(f"Error processing image: {str(e)}")

if 'ocr_extracted_text' in st.session_state:
    st.markdown(st.session_state['wall_defects'])  # Display the extracted text in Markdown format
else:
    st.info("Upload an image and press 'Extract Text'.") 
