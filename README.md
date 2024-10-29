# AI-Cooking-Assistant-chatbot
This repository contains an AI-powered Cooking Assistant chatbot, capable of generating recipes
and assisting with cooking-related tasks.

## You can try out the AI Mentor chatbot directly through this live app:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]( https://ai-cooking-assistant-chatbot.streamlit.app/)

Click the link above to access the app.

## Steps to run the AI Cooking Assistant locally:

1: **Set up API Key:**

   - Create a `.streamlit` folder in the root directory.
   - Inside the folder, create a file named secrets.toml with the following content:
     
     ```toml
     HUGGING_FACE_API_KEY = "<Enter_your_HuggingFace_Api_key>"
     ```
         
2: **Create a Conda Environment and Install Dependencies:**

   - Run the following command to install the required packages:
     
     ```cmd 
     pip install -r requirements.txt

3: **Run the App on Localhost:**

   - Start the application by running:
     
     ```cmd 
     streamlit run streamlit_bot_app.py
