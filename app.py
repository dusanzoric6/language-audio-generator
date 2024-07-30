import streamlit as st

import languages
from main import get_audio_from_text

file_path = "audio_files/sample.mp3"

# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")

# ---- HEADER SECTION ----
with st.container():
    st.header("Duo language mp3 generator")

    # input text area
    input_text_col, select_is_slow_box_org_col = st.columns(2)
    with input_text_col:
        input_text = st.text_area("Enter original text:", height=200, value="Maybe we should go to the airport soon. What do you think?")
    with select_is_slow_box_org_col:
        org_select_is_slow_box = st.checkbox('Is original part pronounced slower?')

    st.markdown("""---""")

    # Create a dropdown language (select box) element
    select_language_tra_box_col, select_is_slow_box_tra_col = st.columns(2)
    with select_language_tra_box_col:
        selected_option = st.selectbox('Select an translation language:', languages.LANGUAGES.values())
    with select_is_slow_box_tra_col:
        tra_select_is_slow_box = st.checkbox('Is translated part pronounced slower?')

    pause_col, _ = st.columns(2)
    with pause_col:
        pause_seconds = float(st.text_input('Enter pause duration in seconds:', key='pause', max_chars=5, value=1))

    st.markdown("""---""")

    # title
    title_col, _ = st.columns(2)
    with title_col:
        placeholder_title = "_".join(input_text.strip().split(" ")[:3])
        title = st.text_input('Enter the title:', key='title', max_chars=100, placeholder=placeholder_title)

    # Disable the button if the input box is empty
    if input_text.strip():
        if st.button("Submit"):
            file_path = get_audio_from_text(
                base_title=placeholder_title if title == "" else title,
                input_text=input_text,
                target_lan=[k for k, v in languages.LANGUAGES.items() if v == selected_option][0],
                is_slow_org=org_select_is_slow_box,
                is_slow_tra=tra_select_is_slow_box,
                silence_seconds=pause_seconds,
                first_original=True
            )
            st.header(f"Done!")
    else:
        st.write("Please enter some text before clicking Submit.")

    # Read the MP3 file in binary mode
    with open(file_path, "rb") as file:
        mp3_data = file.read()

    # Create a download button
    st.download_button(
        label="Download MP3 file",
        data=mp3_data,
        file_name="your_file.mp3",
        mime="audio/mpeg"
    )

    # Additional content for the Streamlit app
    st.write("Click the button above to download the MP3 file.")
