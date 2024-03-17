from dotenv import load_dotenv
import anthropic
import streamlit as st

st.markdown("""
<link rel="stylesheet" type="text/css" href="style.css">
""", unsafe_allow_html=True)

load_dotenv()


def get_response(user_content = "Suggest a few insurance policies based on income and age of the user"):
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=500,
        system = user_content,
        messages=[{"role":"user", "content":"Insurance"}],
    )
    return response.content[0].text

user_content = {}

def gather_user_info():
    name = st.text_input("Enter your name:")
    phone_number = st.text_input("Enter your phone number:")
    email = st.text_input("Enter your email address:")
    age = st.number_input("Enter your age:", min_value=1, max_value=120)
    medical_condition = st.radio("Do you have any existing medical conditions?", ("Yes", "No"))
    return {
        "name": name,
        "phone_number": phone_number,
        "email": email,
        "age": age,
        "medical_condition": medical_condition == "Yes"
    }

def select_prompt(user_data):
    prompts = [
        "Suggest good policies for age greater than 50 and having past medical condition",
        "Suggest good policies for age greater than 50 and having no medical condition",
        "Suggest good policies for age less than 50 and having past medical condition",
        "Suggest good policies for age less than 50 and having no medical condition"
    ]

    if user_data["age"] >= 50 and user_data["medical_condition"]:
        return prompts[0]
    elif user_data["age"] >= 50 and user_data["medical_condition"] == False:
        return prompts[1]
    elif user_data["age"] < 50 and user_data["medical_condition"]:
        return prompts[2]
    else:
        return prompts[3]

st.title("Insurance Policy Suggestor")

# Collect user information
user_content = gather_user_info()


if st.button("Generate Prompt"):
    if not user_content:
        st.warning("No prompt added.") 
    prompt = select_prompt(user_content)
    generated_response = get_response(prompt)
    st.success("Sure")
    st.text_area("", value=generated_response, height=400)