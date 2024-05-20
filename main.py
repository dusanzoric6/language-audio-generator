from deep_translator import GoogleTranslator
from pydub import AudioSegment
import re
from gtts import gTTS
import os
from langdetect import detect
from datetime import datetime


def read_text(input_text):
    if input_text == "":
        with open("text_to_translate.txt", 'r') as file:
            return file.read()
    return input_text


def extract_sentences_from_file(input_text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', read_text(input_text))
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences


def text_to_speech(text, file_name, language='en', slow=False):
    tts = gTTS(text=text, lang=language, slow=slow)
    tts.save(f"audio_files/{file_name}")


def mp3_join(addition, base, silence_length=0):
    sound1 = AudioSegment.from_mp3(f"audio_files/{base}")
    sound2 = AudioSegment.from_mp3(f"audio_files/{addition}")

    if silence_length != 0:
        silence = AudioSegment.silent(duration=silence_length * 1000)
        sound2 = sound2 + silence

    combined = sound1 + sound2
    combined.export(base, format="mp3")


def delete_files_except_base_title():
    files = os.listdir("audio_files")

    for file in files:
        if "_expendable" in file:
            os.remove(f"audio_files/{file}")


def detect_language(text):
    try:
        language = detect(text)
        return language
    except:
        return "Language detection failed."


def get_title(title):
    if title != "":
        return f"{title}.mp3"
    else:
        return datetime.now().strftime("%Y-%m-%d %Hh%Mm%Ss")


def get_audio_from_text(target_len, base_title="", is_slow_org=False, is_slow_tra=False, silence=0,
                        first_original=True, input_text=""):
    org_len = detect_language(read_text(input_text))
    # has mp3 in title
    base_title = f"{get_title(base_title)}"

    # get base mp3 file
    text_to_speech(text="a", file_name=base_title, language="en")
    sentences_org = extract_sentences_from_file(input_text)

    for index, s_org_text in enumerate(sentences_org):
        s_tra_text = GoogleTranslator(source='auto', target=target_len).translate(s_org_text)

        org_mp3_title = f"org_{index}_expendable.mp3"
        tra_mp3_title = f"tra_{index}_expendable.mp3"

        text_to_speech(s_org_text, org_mp3_title, org_len, is_slow_org)
        text_to_speech(s_tra_text, tra_mp3_title, target_len, is_slow_tra)

        if not first_original:
            temp = org_mp3_title
            org_mp3_title = tra_mp3_title
            tra_mp3_title = temp

        # add original mp3 to base
        mp3_join(org_mp3_title, base_title, silence_length=silence)  # added silence always goes after original audio
        # add translated mp3 to base
        mp3_join(tra_mp3_title, base_title)
        print(f"added {index + 1} sentence / {len(sentences_org)}")

    delete_files_except_base_title()
    print("------------------FINISHED---------------------")
