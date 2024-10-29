from itertools import zip_longest
import streamlit as st
from streamlit_chat import message
from huggingface_hub import InferenceClient

# Initiaialiaze Hugging face Api key through Inference Client API
api_key =  st.secrets["HUGGING_FACE_API_KEY"]

# Set the page configuration
st.set_page_config(page_title="AI Cooking Assistant", page_icon="img.svg")
st.title("AI Cooking Assistant")


# Initialize the session state variable
if "entered_prompt" not in st.session_state:
    st.session_state["entered_prompt"] = ""  # User current Input

if "generated" not in st.session_state:
    st.session_state["generated"] = []  # AI generated output

if "past" not in st.session_state:
    st.session_state["past"] = []  # User past queries
    

def submit():
    # Set entered_prompt to the current value of prompt_input
    st.session_state.entered_prompt = st.session_state.prompt_input
    # Clear the user Input
    st.session_state.prompt_input = ""

# Initialize the Hugging Face Inference Client 
client = InferenceClient(api_key= api_key)

# create the Function build message List 
def build_message_list():
    """
    Build the list of system message , human_msg, and Ai_msg.
    """
    zipped_messages = [
        {
            "role":"system",
            "content":"""Your name is AI ChefMate. You are an AI Recipe and Cooking Assistant. Greet the user politely then ask the user name and then ask the user about the dish want to make what is the category of the dish , then generate the user desired Recipe by following the structure given below, or if the user doesnt tell what type of recipe they want to make or confuse which recipe user make it , then ask about the category of dish they want to make , then ask about the ingredients they have and also ask user preferences about the spice high , low or medium , then generate the recipe based on the category and the ingredients they have , follow the structure which is given below:
            1- If the user tell the ingredients which the user have so suggest the famous dishes recipe to the user :
                . And then then generate the recipe.
            2- If the user discuss any other Topic which is not related to cooking, respond the user politely:
                "I am an AI Cooking Assistant, Please ask me the questions related to cooking. "
            3- If the user discuss any sensitive topic like political or others, respond the user politely:
              "I am an AI Cooking Assistant, Please ask me the questions related to cooking. "
            4- Give the title of Recipe in Main Heading.
            5- Give the Heading List of Ingredients, then mention all the ingredients and also write the amount of each ingredient required.
            6- Explain the recipe step by step in points:
            7- Explain the recipe  in very simple English verbly in layman language for better understanding in a Paragraph format and donot give any heading to this paragraph.
            """
        }
    ]
    
    # Zip together the past and AI generated messages
    for human_msg, Ai_msg in zip_longest(st.session_state["past"],st.session_state["generated"]):
        if human_msg is not None:
            zipped_messages.append({"role":"user", "content":human_msg})
        if Ai_msg is not None:
            zipped_messages.append({"role":"assistant", "content":Ai_msg})
    return zipped_messages
# create the function to generate the response
def generate_response():
    """
        Generate AI response using Meta LLaMA Model.
    """
    messages = build_message_list()

    response = ""

    for message in client.chat_completion(
        model = "meta-llama/Llama-3.2-3B-Instruct",
        messages= messages,
        max_tokens=800,
        stream=True,
        temperature=0.5,
        top_p= 0.60
    ):
        if "choices" in message and len(message.choices) > 0:
            response += message.choices[0].delta.get("content", "")

    return response
# Create the Text Input Field
st.text_input("YOU:", key = "prompt_input", on_change=submit)

if st.session_state.entered_prompt != "":
    
    # Get user query 
    user_query = st.session_state.entered_prompt
    
    # Append user query to  Past queries 
    st.session_state.past.append(user_query)

    # Generate response function
    output = generate_response()
    
    # Append AI Response to generated responses
    st.session_state.generated.append(output)

# Display the chat History 
if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"])-1,-1,-1):
        # Display AI response 
        message(st.session_state["generated"][i], key = str(i))
        # Display User Message
        message(st.session_state["past"][i],is_user=True,  key = str(i)+ "_user")
