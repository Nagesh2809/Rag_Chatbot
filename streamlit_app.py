

# streamlit run streamlit_app.py

import os
import base64
import streamlit as st
from nagesh import agent, generate_dynamic_suggestions
from tools1 import calculate_emi_tool



# Encode the image
try:
    with open("konu-1.png", "rb") as img_file:
        encoded_img = base64.b64encode(img_file.read()).decode()
except FileNotFoundError:
    encoded_img = ""  # Fallback if image not found

# Streamlit configuration
st.set_page_config(page_title="Konu Real Estate Assistant", layout="centered")

# Display header with logo
st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{encoded_img}" alt="KONU Logo" width="200">
        <h1 style="color: #F4004D; margin-top: 10px;">Real Estate Assistant</h1>
    </div>
    """,
    unsafe_allow_html=True,
)



# Chat Interface

def main_chat():
    # Initialize session state variables
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "suggestion_clicked" not in st.session_state:
        st.session_state.suggestion_clicked = False  # Track if a suggestion was clicked

    # Display past messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input field
    prompt = st.chat_input("Type your question here...")

    # Process input when user types a message
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.suggestion_clicked = False  # Reset flag on new input
        process_input(prompt)
        st.rerun()  # Refresh to update suggestions

    # Determine dynamic suggestions based on the latest user message
    last_user_message = next((m["content"] for m in reversed(st.session_state.messages) if m["role"] == "user"), None)

    # Show suggestions only if a user message exists
    if last_user_message:
        suggestions = generate_dynamic_suggestions(last_user_message)

        # Display suggestions
        st.subheader("Suggested Questions")
        cols = st.columns(2)  # Arrange buttons in 2 columns
        for i, question in enumerate(suggestions):
            if cols[i % 2].button(question, key=f"sugg_dynamic_{i}"):  # Unique keys for buttons
                st.session_state.messages.append({"role": "user", "content": question})
                st.session_state.suggestion_clicked = False  # Reset to allow new suggestions
                process_input(question)
                st.rerun()  # Refresh UI to show new suggestions

    # Clear button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.suggestion_clicked = False  # Reset to show suggestions again
        st.rerun()  # Refresh UI

def process_input(prompt):
    """Handles user input and generates a response."""
    with st.chat_message("user"):
        st.markdown(prompt)

    # if "emi" in prompt.lower():
    #     show_emi_calculator()
    # else:
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = agent.run(prompt)
            except Exception as e:
                response = f"An error occurred: {e}"
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

def show_emi_calculator():
    """Displays the EMI calculator when the user requests it."""
    st.subheader("EMI Calculator")
    loan_amount = st.number_input("Loan Amount (₹)", min_value=0)
    tenure_years = st.number_input("Tenure (Years)", min_value=0.0)
    annual_interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0)

    if st.button("Calculate EMI"):
        result = calculate_emi_tool(loan_amount, tenure_years, annual_interest_rate)  # Replace with actual function
        if isinstance(result, dict):
            emi = result.get("emi", "N/A")
            total_interest = result.get("total_interest", "N/A")
            st.markdown(f"### EMI: ₹{emi}")
            st.markdown(f"### Total Interest: ₹{total_interest}")
        else:
            st.error(result)

# Run the chat application
if __name__ == "__main__":
    main_chat()

