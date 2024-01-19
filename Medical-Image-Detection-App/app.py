#import necessary modules
import streamlit as st
from pathlib import Path
import google.generativeai as genai
from api_key import api_key

#configure genai with api key
genai.configure(api_key=api_key)

# Set up the model
generation_config = {
  "temperature": 0.4,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 4096,
}

#apply safety settings
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

system_prompt = """

As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the images. Your responsibilities include:

Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings.
Findings: Document all observed anomalies or signs of diseases. Clearly articulate these findings in a structured format.
Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including further tests or treatments as applicable.
Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

Important Notes:
Scope of Response: Only respond if the image pertains to human health issues.
Clarity of Images: In cases where the image quality impedes clear analysis, note that certain aspects are unable to be determined based on the provided image. Avoid making assumptions or unclear analysis if the image is not clear.
Disclaimer: Accompany your analysis with a disclaimer advising consultation with a doctor before making any decisions.

Your insights are valuable in guiding clinical decisions. Please proceed with the analysis, adhering to the structured approach outlined above. This system prompt aims to train our model according to our specific scenario, ensuring accuracy, clarity, and relevance in the analysis.
please provide the output response with these 4 headings : Detailed Analysis, Recommendations, Recommendations and Next Steps,Treatment Suggestions.
Add the  Disclaimer also
make everything very readable and very good response with best fonts.
"""
#model configuration
model = genai.GenerativeModel(model_name="gemini-pro-vision",
                              generation_config=generation_config,
                              safety_settings=safety_settings)




#set the page configuration
st.set_page_config(page_title="MediMind AI", page_icon="robot:")

#Set the logo
st.image("MediMind-AI-logo.png", width=150)

#Set the title
st.title("⚕️ MediMind AI Image Analytics 🩺")

# set the subtile
st.subheader("An Application that help the users to identify medical images")

uploaded_file = st.file_uploader("Upload the medical image for Analysis", type=["png", "jpg","jpeg"])
if uploaded_file:
    st.image(uploaded_file, width=250, caption= "Uploaded Medical Image")

submit_button = st.button("Generate the Analysis")

if submit_button:
    #process the uploaded image
    image_data = uploaded_file.getvalue()

    #making our image ready
    image_parts = [
        {
            "mime_type": "image/jpeg",
            "data": image_data
        },
    ]
    #making the prompt ready
    prompt_parts = [
        "What is going on this particular image?",
        image_parts[0],
        system_prompt
    ]

    
    #geneate the response based on prompt and image

    response = model.generate_content(prompt_parts)
    if response:
        st.title("Here is the analysis based on the image:")
        st.write(response.text)

