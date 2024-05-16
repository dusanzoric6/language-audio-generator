from deep_translator import GoogleTranslator
from pydub import AudioSegment
import re
from gtts import gTTS
import os
from langdetect import detect


def read_text():
    with open("text_to_translate.txt", 'r') as file:
        return file.read()


def extract_sentences_from_file():
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', read_text())
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences


def text_to_speech(text, file_name, language='en', slow=False):
    tts = gTTS(text=text, lang=language, slow=slow)
    tts.save(file_name)


def join_mp3_to_base(file_path):
    sound1 = AudioSegment.from_mp3("base.mp3")
    sound2 = AudioSegment.from_mp3(file_path)

    combined = sound1 + sound2
    combined.export("base.mp3", format="mp3")


def delete_files_except_one():
    files = os.listdir()

    for file in files:
        if ".mp3" in file:
            if file != "base.mp3":
                os.remove(file)


def detect_language(text):
    try:
        language = detect(text)
        return language
    except:
        return "Language detection failed."


def get_audio_from_text(target_len, org_slow=False, tra_slow=False):
    text_to_speech("s.", "base.mp3", "en")
    lan_org = detect_language(read_text())
    sentences_org = extract_sentences_from_file()
    for index, s_org in enumerate(sentences_org):
        text_to_speech(s_org, f"org_{index}.mp3", lan_org, org_slow)
        join_mp3_to_base(f"org_{index}.mp3")

        s_tran = GoogleTranslator(source='auto', target=target_len).translate(s_org)
        text_to_speech(s_tran, f"tra_{index}.mp3", target_len, tra_slow)
        join_mp3_to_base(f"tra_{index}.mp3")
        print(f"added {index + 1} / {len(sentences_org)}")


get_audio_from_text(target_len="sr", org_slow=False, tra_slow=False)
delete_files_except_one()
