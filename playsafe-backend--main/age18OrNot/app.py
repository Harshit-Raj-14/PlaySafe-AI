import streamlit as st
from PIL import Image
import os
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# Load the API key from the .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Check if the API key exists
if not GEMINI_API_KEY:
    raise ValueError("API key not found! Please add GEMINI_API_KEY to your .env file.")

# Authenticate with the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def analyze_image_with_gemini(image, prompt="Estimate my age from this image"):
    """Analyze the image and predict age. You need to predict age based on face features and you have to tell only the age number. Only return the age that too in number."""
    try:
        # Load the generative model
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
        
        # Generate content using the image and prompt
        response = model.generate_content([prompt, image], stream=True)
        
        # Collect the streamed response
        streamed_text = ""
        for message in response:
            streamed_text += message.text  # Accumulate the streamed response
        
        # Return the final accumulated response text
        return streamed_text
    except Exception as e:
        st.error(f"Error using Gemini API: {e}")
        return None

def main():
    st.title("PlaySafe AI Age Verification Step")
    st.write("Child Safety Mechanism for Online Gambling Prevention")

    # Use Streamlit's built-in camera input
    img_data = st.camera_input("Take a photo")

    if img_data:
        # Save and open the image using PIL
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"screenshot_{timestamp}.jpg"
        with open(screenshot_path, "wb") as f:
            f.write(img_data.getbuffer())
        # st.success(f"Screenshot saved as {screenshot_path}")

        # Open the saved image using PIL
        image = Image.open(screenshot_path)

        # Display the image in the app
        # st.image(image, caption="Your Screenshot", use_column_width=True)

        # Call the Gemini API to analyze the image
        st.write("Validating your age...")
        analysis_result = analyze_image_with_gemini(image)

        if analysis_result:
            # Extract the predicted age from the response (if possible)
            try:
                predicted_age = int("".join(filter(str.isdigit, analysis_result)))
                # st.write(f"Estimated Age: {predicted_age} years")

                if predicted_age > 18:
                    st.error("You are above 18. You can proceed.")
                else:
                    st.success("You are under 18. Access is restricted, and you cannot proceed.")
            except ValueError:
                st.error("Unable to extract age from Gemini API response.")
        else:
            st.error("Failed to analyze the image.")

if __name__ == "__main__":
    main()
