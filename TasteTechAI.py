import streamlit as st
import openai
import os
import requests
from streamlit_lottie import st_lottie

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set a default greeting message
default_greeting = "Hi! How can I help you today?"

# Initialize context with the default greeting and the existing system message
context = [
    {
        "role": "system",
        "content": """
        You are OrderBot, an automated service to collect orders for a pizza restaurant. \
        You first greet the customer, then collect the order, \
        and then ask if it's a pickup or delivery. \
        You wait to collect the entire order, then summarize it and check for a final \
        time if the customer wants to add anything else. \
        If it's a delivery, you ask for an address. \
        Finally, you collect the payment.\
        Make sure to clarify all options, extras, and sizes to uniquely \
        identify the item from the menu.\
        You respond in a short, very conversational friendly style. \
        The menu includes \
        pepperoni pizza 12.95, 10.00, 7.00 \
        cheese pizza 10.95, 9.25, 6.50 \
        eggplant pizza 11.95, 9.75, 6.75 \
        fries 4.50, 3.50 \
        greek salad 7.25 \
        Toppings: \
        extra cheese 2.00, \
        mushrooms 1.50 \
        sausage 3.00 \
        canadian bacon 3.50 \
        AI sauce 1.50 \
        peppers 1.00 \
        Drinks: \
        coke 3.00, 2.00, 1.00 \
        sprite 3.00, 2.00, 1.00 \
        bottled water 5.00 \
        """,
    }
]

# Check if 'conversation' is not in session state and initialize it
if "conversation" not in st.session_state:
    st.session_state.conversation = context.copy()


# Function to interact with OpenAI API
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]


# Function to collect and display user and assistant messages
def collect_messages(prompt):
    # Append user message to the context
    st.session_state.conversation.append({"role": "user", "content": f"{prompt}"})

    # Get assistant response from OpenAI API
    response = get_completion_from_messages(st.session_state.conversation)

    # Append assistant message to the context
    st.session_state.conversation.append(
        {"role": "assistant", "content": f"{response}"}
    )

    # Return the chat result as JSON
    return st.session_state.conversation


def main():
    st.set_page_config(
        page_title="Order Bot!",
        page_icon=":shallow_pan_of_food:",
        layout="wide",
    )

    with st.container():
        left_column, right_column = st.columns([2, 1])

        # Load Assets
        def load_lottieURL(url):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()

        lottie_coding = load_lottieURL(
            "https://lottie.host/93e5d938-fe5d-4777-afb9-94afc06b707d/UIyeVl4SRj.json"
        )

        with left_column:
            st.header("Welcome! I am Groovy :wave:")
            st.subheader("Order and Eat Delicious Food!")
            # Display default greeting
            st.write(default_greeting)

        with right_column:
            st_lottie(lottie_coding, height=150, key="food")
        st.write("---")

        # User Input Form
        with st.form("order_form"):
            user_input = st.text_input(
                "User Input:",
                value="",
                help="Place your order with OrderBot...",
                key="user_input",
            )

            # Collect and display messages on form submit
            submit_button = st.form_submit_button("Submit")

            # Trigger form submit on Enter key press
            st.markdown(
                """
                <script>
                    document.addEventListener('DOMContentLoaded', function() {
                        document.querySelector('input[data-baseweb="input"]').addEventListener('keyup', function(event) {
                            if (event.key === "Enter") {
                                document.querySelector('button[data-testid="stFormSubmit"]').click();
                            }
                        });
                    });
                </script>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """<style>
            .user-message {
                background-color: #21618C; 
                padding: 10px;
                border-radius: 10px;
                margin: 10px 0;
                max-width: 80%;
                align-self: flex-end;
            }
            .assistant-message {
                background-color: #148F77; 
                padding: 10px;
                border-radius: 10px;
                margin: 10px 0;
                max-width: 80%;
                align-self: flex-start;
            }
            </style>""",
                unsafe_allow_html=True,
            )

        # Display messages on form submit
        if submit_button:
            conversation = collect_messages(user_input)

            # Display conversation
            for message in conversation:
                if message["role"] == "user":
                    st.markdown(
                        f'<div class="user-message">User: {message["content"]}</div>',
                        unsafe_allow_html=True,
                    )
                elif message["role"] == "assistant":
                    st.markdown(
                        f'<div class="assistant-message">Assistant: {message["content"]}</div>',
                        unsafe_allow_html=True,
                    )

        hide_default_format = """
                <style>
                footer {visibility: hidden;}
                </style>
                """
        st.markdown(hide_default_format, unsafe_allow_html=True)


# MainMenu {visibility: hidden; }

if __name__ == "__main__":
    main()
