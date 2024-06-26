import streamlit as st

import languages
from main import get_audio_from_text

# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")

# ---- HEADER SECTION ----
with st.container():
    st.title("Duo language mp3 generator")

    # text area
    user_input = st.text_area("Enter some text:", height=200, value="Maybe we should go to the airport soon. What do you think?")  # height is in pixels

    # title text input
    placeholder_title = "_".join(user_input.strip().split(" ")[:3])
    title = st.text_input('Enter the title:', key='title', max_chars=100, placeholder=placeholder_title)

    # Create a dropdown (select box) element
    selected_option = st.selectbox('Select an language:', languages.LANGUAGES.values())

    pause_seconds = float(st.text_input('Enter pause duration in seconds:', key='pause', max_chars=5, value=1))

    # Disable the button if the input box is empty
    if user_input.strip():
        if st.button("Submit"):
            title = get_audio_from_text(
                base_title=placeholder_title if title == "" else title,
                input_text=user_input,
                target_lan=[k for k, v in languages.LANGUAGES.items() if v == selected_option][0],
                is_slow_org=False,
                is_slow_tra=False,
                silence_seconds=pause_seconds,
                first_original=True
            )

            st.header(f" file title - {title}")
    else:
        st.write("Please enter some text before clicking Submit.")
