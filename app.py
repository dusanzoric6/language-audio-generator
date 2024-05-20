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
    file_title = user_input.split(".")[0].split(" ")[0]

    if user_input:
        get_audio_from_text(
            base_title=file_title,
            input_text=user_input,
            target_len="de",
            is_slow_org=False,
            is_slow_tra=False,
            silence=2,
            first_original=True
        )

        st.header(f" file title - {file_title}")
