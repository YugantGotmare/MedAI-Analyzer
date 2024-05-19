import streamlit as st  # Import Streamlit for creating the web application
from pathlib import Path  # Import Path from pathlib for handling file paths
import google.generativeai as genai  # Import the Google Generative AI library

from api_key import api_key  # Import the API key from a separate file for security

# Configure the Google Generative AI model with the provided API key
genai.configure(api_key=api_key)

# Model generation configuration parameters
generation_config = {
    "temperature": 0.4,  # Controls the randomness of the generated output
    "top_p": 1,  # Nucleus sampling parameter
    "top_k": 32,  # Limits the next token selection to the top K choices
    "max_output_tokens": 4096,  # Maximum number of tokens in the output
}

# Safety settings to ensure the generated content is appropriate
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# System prompt guiding the AI on how to analyze the medical images and format the response
system_prompt = """
As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the images.

Your Responsibilities:

1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal finding.
2. Findings Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured format.
3. Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including further tests or treatments as applicable.
4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

Important Notes:
1. Scope of Response: Only respond if the image pertains to human health issues.
2. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are 'Unable to be determined based on the provided images.'
3. Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Doctor before making any decision."
4. Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis, adhering to the structured approach outlined above.

Please provide an output response with these 4 headings: Detailed Analysis, Findings Report, Recommendations and Next Steps, Treatment Suggestions.
"""

# Initialize the Google Generative AI model with the specified model name and configurations
model = genai.GenerativeModel(
    model_name="gemini-pro-vision",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Streamlit UI setup
st.set_page_config(page_title="MedAI Analyzer", page_icon=":stethoscope:", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
        .main {
            background-color: #faf3e0;
            padding: 20px;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .stFileUploader {
            margin-top: 20px;
            margin-bottom: 20px;
        }
        h1, h2, h3, h4, h5, h6, p {
            color: #333333;  /* Darker text color for better contrast */
        }
        .uploaded-image {
            max-width: 100px;  /* Set maximum width for the uploaded image */
            margin: 20px auto;  /* Center the image and add margin */
            border-radius: 10px;  /* Add border radius for better aesthetics */
            display: block;  /* Ensure image is displayed as a block element */
        }
    </style>
""", unsafe_allow_html=True)

# Title and subtitle for the Streamlit application
st.title("MedAI Analyzer :stethoscope:")
st.subheader("Empowering Healthcare Professionals with Advanced Image Analysis")

# Description of the application
st.write("""
Welcome to **MedAI Analyzer**, an advanced application designed to assist healthcare professionals in analyzing medical images with precision and expertise. Upload your medical images to receive a detailed analysis, findings report, and tailored recommendations based on cutting-edge AI technology.
""")

# File uploader for users to upload their medical images
st.subheader("Upload Medical Image")
uploaded_file = st.file_uploader("Please upload a medical image (PNG, JPG, JPEG):", type=['png', 'jpg', 'jpeg'])

# Display the uploaded image if available
if uploaded_file:
    st.image(uploaded_file, caption='Uploaded Medical Image', width=250, use_column_width=False, output_format="auto")


# Button for generating the analysis report
submit_button = st.button("Generate Analysis")

# If the submit button is pressed and an image is uploaded
if submit_button and uploaded_file:
    # Read the image data from the uploaded file
    image_data = uploaded_file.getvalue()

    # Prepare the image parts for the API request
    image_parts = [
        {
            "mime_type": "image/jpeg",  # Specify the MIME type of the image
            "data": image_data  # Include the image data
        },
    ]

    # Combine the image parts and the system prompt
    prompt_parts = [
        image_parts[0],
        system_prompt,
    ]

    # Display a title for the analysis results
    st.subheader("Analysis Results")
    st.write("Here is the analysis based on your image:")

    # Generate content using the Google Generative AI model
    response = model.generate_content(prompt_parts)

    # Display the generated analysis report
    st.write(response.text)  # Ensure the correct response key is accessed

# Footer with additional information or disclaimer
st.markdown("""
---
**Disclaimer:** The analysis provided by MedAI Analyzer is intended to assist healthcare professionals and should not be used as the sole basis for medical decision-making. Always consult with a qualified medical professional before making any healthcare decisions.
""")
