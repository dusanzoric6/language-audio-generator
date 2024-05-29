import streamlit as st

from main import get_audio_from_text

# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")

# ---- HEADER SECTION ----
with st.container():
    st.subheader("Hi, I am Sven :wave:")
    st.title("A Data Analyst From Germany")

    # Create a text input box
    user_input = st.text_area("Enter some text:", height=200, )  # height is in pixels

    file_title = "_".join(user_input.strip().split(" ")[:5])
    print(file_title)

    # Disable the button if the input box is empty
    if user_input.strip():
        if st.button("Submit"):
            title = get_audio_from_text(
                base_title=file_title,
                input_text=user_input,
                target_lan="de",
                is_slow_org=False,
                is_slow_tra=False,
                silence=1,
                first_original=True
            )

            st.header(f" file title - {file_title}")
    else:
        st.write("Please enter some text before clicking Submit.")
