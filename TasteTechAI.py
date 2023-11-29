import streamlit as st
import openai
import os
from streamlit_chat import message

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
        page_title="Order Bot!", page_icon=":shallow_pan_of_food:", layout="wide"
    )

    with st.container():
        st.header("Welcome! I am Groovy:wave:")
        st.subheader("Order and Eat Delicious Food!")
        st.write("---")
        # Display default greeting
        st.write(default_greeting)

        # User Input Form
        user_input = st.text_input(
            "User Input:",
            value="",
            help="Place your order with OrderBot...",
            key="user_input",
        )

        st.markdown(
            """<style>
            .css-1g6m9li {
                background-color: #f2f2f2; /* Light gray background */
                border: 1px solid #ccc; /* Gray border */
            }
            </style>""",
            unsafe_allow_html=True,
        )

        # Submit Button
        submit_button = st.button("Submit", key="submit_button")

        st.markdown(
            """<style>
            .css-2trqyj {
                background-color: #4CAF50; /* Green color */
                color: white;
            }
            </style>""",
            unsafe_allow_html=True,
        )
        # Collect and display messages on button click
        if submit_button:
            conversation = collect_messages(user_input)

            # Display conversation
            for message in conversation:
                if message["role"] == "user":
                    st.markdown(
                        f"**User:** {message['content']}", unsafe_allow_html=True
                    )
                elif message["role"] == "assistant":
                    st.markdown(
                        f"**Assistant:** {message['content']}", unsafe_allow_html=True
                    )


if __name__ == "__main__":
    main()
