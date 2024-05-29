import streamlit as st

def main():
    st.title("Conditional Button Example")

    # Create a text input box
    user_input = st.text_input("Enter some text:")

    # CSS to simulate a disabled button look
    st.markdown("""
        <style>
        .disabled-button {
            pointer-events: none;
            opacity: 0.65;
        }
        </style>
        """, unsafe_allow_html=True)

    # Logic to display the button or the disabled button look
    if user_input.strip():
        if st.button("Submit"):
            st.write("You entered:", user_input)
    else:
        st.button("Submit", key="disabled_button", help="Please enter some text to enable this button")
        st.markdown('<div class="disabled-button"><button>Submit</button></div>', unsafe_allow_html=True)
        st.write("Please enter some text to enable the submit button.")

if __name__ == "__main__":
    main()
