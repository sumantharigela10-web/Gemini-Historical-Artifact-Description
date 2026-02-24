import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="Historical Vision AI", page_icon="🏛️")
st.title("🏛️ Historical Photo Analyzer")

# 2. Setup API
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.error("❌ API Key not found! Check your .env file.")

# 3. Sidebar for Image Upload
with st.sidebar:
    st.header("Upload Section")
    uploaded_file = st.file_uploader("Choose a historical photo...", type=["jpg", "jpeg", "png"])

# 4. Main Logic
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)
    
    if st.button("Analyze History"):
        # CHANGED: Using 'gemini-flash-latest' to avoid the 404 error
        model = genai.GenerativeModel('gemini-flash-latest')
        
        prompt = (
            "Identify what is in this image. Provide a detailed historical background, "
            "including the time period, significance, and interesting facts."
        )
        
        with st.spinner("📜 Researching archives..."):
            try:
                # This sends both the prompt and the image
                response = model.generate_content([prompt, image])
                st.success("Analysis Complete!")
                st.write("### 📜 Historical Record")
                st.write(response.text)
            except Exception as e:
                st.error(f"Analysis failed: {e}")
else:
    st.info("👈 Please upload a photo in the sidebar to begin.")